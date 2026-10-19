"""Motor discreto de cadenas de Markov a nivel posesión + Monte Carlo (spec 4).

Capa 1 — Transición de posesiones. Cada *segmento* (inicio de posesión o tras rebote ofensivo)
termina en un estado de S:
    3PT(3) 2PT(2) AND1_MADE(3) AND1_MISS(2) FT1 FT2 FT3 (Binomial(n, FT%)) TOV(0) MISS_DREB(0)
    OREB (transitorio: re-posesión)
Como OREB re-inicia el mismo proceso, la distribución terminal de la posesión es exactamente
p_abs / (1 − p_OREB) (probabilidad de absorción de una cadena geométrica): se muestrea en un
paso, vectorizado, sin pérdida de exactitud.

Combinación ataque A × defensa B (log5 multinomial):  p_i ∝ o_i · d_i / l_i
Calibración al estado latente (Kalman): inclinación exponencial (logit multinomial)
    p_i(β) ∝ p_i · exp(β·v_i)   con β tal que E[puntos/posesión] = (μ + off_A + def_B ± h/2)/100.

Capa 2 — Longitud: N_poss ~ Conway-Maxwell-Poisson(λ_pace, ν) (sub-disperso, ν>1);
λ_pace = φ_context / (w_A/Pace_A + w_B/Pace_B), pesos = frecuencia de transición normalizada.
Prórroga: 5 minutos (~λ·5/48 posesiones) vectorizada mientras persista el empate.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from scipy.optimize import brentq
from scipy.special import gammaln

from nba_quant.config import SimulationConfig

STATES = ("3PT", "2PT", "AND1_MADE", "AND1_MISS", "FT1", "FT2", "FT3", "TOV", "MISS_DREB")
BASE_POINTS = np.array([3, 2, 3, 2, 0, 0, 0, 0, 0], dtype=np.int16)
FT_ATTEMPTS = np.array([0, 0, 0, 0, 1, 2, 3, 0, 0], dtype=np.int16)
LEAGUE_SEGMENT_PROBS = {  # referencia NBA 2025-26 (por segmento) para log5 cuando falta liga
    "3PT": 0.126, "2PT": 0.221, "AND1_MADE": 0.018, "AND1_MISS": 0.005, "FT1": 0.002, "FT2": 0.089,
    "FT3": 0.003, "TOV": 0.119, "MISS_DREB": 0.295, "OREB": 0.122,
}
CMP_HALF_WIDTH = 70


@dataclass(frozen=True)
class TeamProfile:
    """Perfil de un equipo para el motor: probabilidades de segmento en ataque y permitidas."""

    team: str
    pace: float
    transition_freq: float
    ft_pct: float
    off_probs: dict[str, float]
    def_probs: dict[str, float]
    off_rating: float  # pts/100 esperados del ataque (sin rival): μ + θ_off
    def_rating: float  # pts/100 que permite la defensa: μ + θ_def


@dataclass(frozen=True)
class MatchupParams:
    home_abs: np.ndarray  # distribución terminal por posesión (local ataca)
    away_abs: np.ndarray
    home_ft: float
    away_ft: float
    lam: float
    home_target_ppp: float
    away_target_ppp: float


def _vec(probs: dict[str, float]) -> tuple[np.ndarray, float]:
    v = np.array([max(probs.get(s, LEAGUE_SEGMENT_PROBS[s]), 1e-6) for s in STATES])
    return v, max(probs.get("OREB", LEAGUE_SEGMENT_PROBS["OREB"]), 1e-6)


def expected_points_vector(ft_pct: float) -> np.ndarray:
    return BASE_POINTS + FT_ATTEMPTS * ft_pct


def combine_log5(off: dict[str, float], dfn: dict[str, float], league: dict[str, float]) -> tuple[np.ndarray, float]:
    """Log5 multinomial: devuelve (absorción normalizada, p_OREB por segmento)."""
    o, o_or = _vec(off)
    d, d_or = _vec(dfn)
    l, l_or = _vec(league)
    seg = np.append(o * d / l, o_or * d_or / l_or)
    seg = seg / seg.sum()
    p_oreb = float(seg[-1])
    absorb = seg[:-1] / (1.0 - p_oreb)
    return absorb / absorb.sum(), p_oreb


def tilt_to_target(absorb: np.ndarray, ft_pct: float, target_ppp: float) -> np.ndarray:
    """Inclinación exponencial (logit multinomial) para que E[pts/posesión] = target."""
    v = expected_points_vector(ft_pct)
    lo_ppp, hi_ppp = 0.2, float(v.max()) * 0.95
    target = float(np.clip(target_ppp, lo_ppp, hi_ppp))

    def ppp(beta: float) -> float:
        w = absorb * np.exp(beta * v)
        return float((w / w.sum()) @ v)

    beta = brentq(lambda b: ppp(b) - target, -8.0, 8.0)
    w = absorb * np.exp(beta * v)
    return w / w.sum()


def matchup_pace(home: TeamProfile, away: TeamProfile, phi_context: float = 1.0) -> float:
    tf = np.array([max(home.transition_freq, 1e-3), max(away.transition_freq, 1e-3)])
    w = tf / tf.sum()
    return phi_context / (w[0] / home.pace + w[1] / away.pace)


def build_matchup(home: TeamProfile, away: TeamProfile, league: dict[str, float] | None = None,
                  league_ortg: float = 114.5, hca_per100: float = 2.4, phi_context: float = 1.0,
                  home_mult: float = 1.0, away_mult: float = 1.0,
                  cross_mods: dict[str, dict[str, float]] | None = None) -> MatchupParams:
    """Construye los parámetros de la cadena para ambos ataques.

    `home_mult` / `away_mult` escalan los pts/100 esperados (escenarios Mejor/Normal/Peor).
    `cross_mods` = {'home': {'3PT': 1.03, '2PT': 0.98}, 'away': {...}} (cruces asimétricos)."""
    league = league or LEAGUE_SEGMENT_PROBS
    cross_mods = cross_mods or {}
    out = {}
    for side, att, dfn, sign, mult in (("home", home, away, +1, home_mult), ("away", away, home, -1, away_mult)):
        absorb, _ = combine_log5(att.off_probs, dfn.def_probs, league)
        for state, factor in cross_mods.get(side, {}).items():
            absorb[STATES.index(state)] *= factor
        absorb = absorb / absorb.sum()
        rating = att.off_rating + dfn.def_rating - league_ortg + sign * hca_per100 / 2
        target = mult * rating / 100.0
        out[side] = (tilt_to_target(absorb, att.ft_pct, target), target)
    return MatchupParams(out["home"][0], out["away"][0], home.ft_pct, away.ft_pct,
                         matchup_pace(home, away, phi_context), out["home"][1], out["away"][1])


def cmp_pmf(lam: float, nu: float) -> tuple[np.ndarray, np.ndarray]:
    """PMF de Conway-Maxwell-Poisson con media ≈ lam (se resuelve la tasa) en soporte acotado."""
    support = np.arange(max(1, int(lam) - CMP_HALF_WIDTH), int(lam) + CMP_HALF_WIDTH)

    def pmf_for(log_rate: float) -> np.ndarray:
        logp = support * log_rate - nu * gammaln(support + 1)
        logp -= logp.max()
        p = np.exp(logp)
        return p / p.sum()

    log_rate = brentq(lambda lr: pmf_for(lr) @ support - lam, 0.0, nu * np.log(lam + CMP_HALF_WIDTH) + 5)
    return support, pmf_for(log_rate)


@dataclass
class SimulationResult:
    """Puntos simulados y estadísticos del margen (ΔY = Y_H − Y_A)."""

    home_pts: np.ndarray
    away_pts: np.ndarray
    overtime: np.ndarray
    meta: dict = field(default_factory=dict)

    @property
    def margin(self) -> np.ndarray:
        return self.home_pts.astype(np.int32) - self.away_pts.astype(np.int32)

    @property
    def total(self) -> np.ndarray:
        return self.home_pts.astype(np.int32) + self.away_pts.astype(np.int32)

    def home_win_prob(self) -> float:
        return float((self.margin > 0).mean())

    def margin_pmf(self) -> dict[int, float]:
        vals, counts = np.unique(self.margin, return_counts=True)
        return dict(zip(vals.tolist(), (counts / counts.sum()).tolist()))

    def modal_margin(self) -> int:
        vals, counts = np.unique(self.margin, return_counts=True)
        return int(vals[np.argmax(counts)])

    def critical_margin_mass(self) -> dict[str, float]:
        """Masa en márgenes clave del GANADOR probable (k = margen de victoria > 0)."""
        m = self.margin if self.home_win_prob() >= 0.5 else -self.margin
        return {
            "k=1": float((m == 1).mean()), "k in [2,3]": float(((m >= 2) & (m <= 3)).mean()),
            "k in [4,5]": float(((m >= 4) & (m <= 5)).mean()), "k in [6,7]": float(((m >= 6) & (m <= 7)).mean()),
            "k>=8": float((m >= 8).mean()), "pierde": float((m < 0).mean()),
        }

    def most_likely_score(self) -> tuple[int, int, float]:
        key = self.home_pts.astype(np.int64) * 1000 + self.away_pts.astype(np.int64)
        vals, counts = np.unique(key, return_counts=True)
        i = int(np.argmax(counts))
        return int(vals[i] // 1000), int(vals[i] % 1000), float(counts[i] / counts.sum())

    def cover_prob(self, home_spread: float) -> tuple[float, float]:
        """(P(local cubre), P(push)) para un spread desde la óptica local (p.ej. −4.5)."""
        adj = self.margin + home_spread
        return float((adj > 0).mean()), float((adj == 0).mean())

    def over_prob(self, total_line: float) -> tuple[float, float]:
        return float((self.total > total_line).mean()), float((self.total == total_line).mean())


class PossessionMarkovEngine:
    """Simulación Monte Carlo 100% vectorizada (sin bucles por simulación)."""

    def __init__(self, cfg: SimulationConfig) -> None:
        self.cfg = cfg

    def _points(self, rng: np.random.Generator, absorb: np.ndarray, ft_pct: float,
                n_poss: np.ndarray) -> np.ndarray:
        n_max = int(n_poss.max()) if n_poss.size else 0
        if n_max == 0:
            return np.zeros(n_poss.shape, dtype=np.int32)
        cum = np.cumsum(absorb)
        cum[-1] = 1.0
        states = np.searchsorted(cum, rng.random((n_poss.size, n_max)), side="right")
        active = np.arange(n_max)[None, :] < n_poss[:, None]
        base = np.where(active, BASE_POINTS[states], 0)
        ft_n = np.where(active, FT_ATTEMPTS[states], 0)
        ft_made = rng.binomial(ft_n, ft_pct)
        return (base + ft_made).sum(axis=1).astype(np.int32)

    def _draw_possessions(self, rng: np.random.Generator, lam: float, size: int) -> tuple[np.ndarray, np.ndarray]:
        support, pmf = cmp_pmf(lam, self.cfg.cmp_nu)
        n_home = rng.choice(support, size=size, p=pmf)
        # El otro equipo tiene la misma cantidad ±1 según quién abre/cierra cada periodo.
        n_away = np.clip(n_home + rng.choice([-1, 0, 1], size=size, p=[0.25, 0.5, 0.25]), 1, None)
        return n_home, n_away

    def simulate(self, params: MatchupParams, n_sims: int | None = None, seed: int | None = None) -> SimulationResult:
        n_sims = n_sims or self.cfg.n_sims_markov
        rng = np.random.default_rng(self.cfg.seed if seed is None else seed)
        home_parts, away_parts, ot_parts = [], [], []
        for start in range(0, n_sims, self.cfg.chunk_size):
            size = min(self.cfg.chunk_size, n_sims - start)
            n_h, n_a = self._draw_possessions(rng, params.lam, size)
            h = self._points(rng, params.home_abs, params.home_ft, n_h)
            a = self._points(rng, params.away_abs, params.away_ft, n_a)
            ot = np.zeros(size, dtype=np.int8)
            lam_ot = params.lam * self.cfg.ot_possession_fraction
            for _ in range(self.cfg.max_overtimes):
                tied = np.flatnonzero(h == a)
                if tied.size == 0:
                    break
                n_ot = rng.poisson(lam_ot, size=tied.size).clip(min=1)
                h[tied] += self._points(rng, params.home_abs, params.home_ft, n_ot)
                a[tied] += self._points(rng, params.away_abs, params.away_ft, n_ot)
                ot[tied] += 1
            # Desempate final determinista-aleatorio si persiste tras max_overtimes (muy raro).
            still = np.flatnonzero(h == a)
            if still.size:
                coin = rng.random(still.size) < 0.5
                h[still[coin]] += 1
                a[still[~coin]] += 1
            home_parts.append(h)
            away_parts.append(a)
            ot_parts.append(ot)
        return SimulationResult(np.concatenate(home_parts), np.concatenate(away_parts), np.concatenate(ot_parts),
                                {"lambda_pace": params.lam, "home_target_ppp": params.home_target_ppp,
                                 "away_target_ppp": params.away_target_ppp})
