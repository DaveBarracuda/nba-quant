"""CLASE 4 — MarketInefficienciesEngine (spec 3 fase 1.8).

Cada ineficiencia es una señal numérica por equipo-partido. Su efecto en puntos se estima
con una regresión Ridge *centrada en priors* sobre el residuo ATS histórico:
    β = argmin ||y − Xβ||² + λ||β − β_prior||²  =  (XᵀX + λI)⁻¹ (Xᵀy + λ β_prior)
de forma que con poca historia el motor usa los priors y, partido tras partido, se
auto-calibra hacia lo que el mercado realmente ha dejado de descontar.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from nba_quant.logging_utils import get_logger
from nba_quant.teams import HIGH_ALTITUDE_FT, altitude_ft, tz_offset

log = get_logger("inefficiencies")

# Prior de efecto (puntos de margen por unidad de señal) y fuerza del prior.
SIGNAL_PRIORS: dict[str, float] = {
    "letdown": -1.0,
    "lookahead": -0.8,
    "sharp_move": 0.35,  # por punto de movimiento de línea a favor
    "public_fade": 0.5,
    "jet_lag": -0.35,  # por hora de huso horario cruzada con <=1 día de descanso
    "altitude_b2b": -1.2,
    "bounce_back": 0.8,
}
PRIOR_STRENGTH = 200.0
ELITE_RANK = 5
LETDOWN_TOP_RANK = 8
BLOWOUT_LOSS = 20
REF_PACE_SENSITIVITY = 0.015  # φ_context por desviación típica de faltas del trío arbitral
GARBAGE_RELAX_SPREAD = 10.0


@dataclass(frozen=True)
class RefereeProfile:
    fouls_per_game_z: float
    fta_per_game_z: float
    n_games: int


class MarketInefficienciesEngine:
    def __init__(self) -> None:
        self.coef = dict(SIGNAL_PRIORS)

    # ------------------------------------------------------------------ señales
    @staticmethod
    def build_signals(sched: pd.DataFrame, strength_rank: pd.Series | None = None) -> pd.DataFrame:
        """`sched`: una fila por equipo-partido ordenada con columnas team, opponent, game_date,
        is_home, rest_days, margin (si jugado), went_ot, ats_residual, home_team (sede),
        spread_open/spread_close (óptica del equipo), ticket_pct (opcional)."""
        s = sched.sort_values(["team", "game_date"]).copy()
        keys = ["season", "team"] if "season" in s.columns else ["team"]  # las rachas no cruzan temporadas
        rank = strength_rank if strength_rank is not None else pd.Series(dtype=float)
        s["opp_rank"] = s["opponent"].map(rank).fillna(15)
        s["team_rank"] = s["team"].map(rank).fillna(15)
        g = s.groupby(keys)
        prev_margin, prev_ot, prev_rank = g["margin"].shift(1), g["went_ot"].shift(1), g["opp_rank"].shift(1)
        # Letdown: viene de ganar en prórroga o de ganar ajustado a un top-8.
        s["letdown"] = (((prev_ot == 1) & (prev_margin > 0))
                        | ((prev_margin > 0) & (prev_margin <= 5) & (prev_rank <= LETDOWN_TOP_RANK))).astype(float)
        # Lookahead: rival actual débil y al día siguiente un rival élite.
        next_rank, next_date = g["opp_rank"].shift(-1), g["game_date"].shift(-1)
        s["lookahead"] = ((next_rank <= ELITE_RANK) & ((next_date - s["game_date"]).dt.days <= 1)
                          & (s["opp_rank"] > 15)).astype(float)
        # Sharp vs public: movimiento de línea a favor del equipo (pts) y fade del público.
        move = (s.get("spread_open", np.nan) - s.get("spread_close", np.nan))
        s["sharp_move"] = pd.Series(move, index=s.index).fillna(0).clip(-4, 4)
        if "ticket_pct" in s.columns:
            s["public_fade"] = ((s["ticket_pct"] < 0.40) & (s["sharp_move"] > 0)).astype(float)
        else:
            s["public_fade"] = 0.0
        # Jet-lag: horas de huso cruzadas desde la sede del partido anterior, con <=1 día de descanso.
        venue_tz = s["home_team"].map(tz_offset)
        prev_tz = g["home_team"].shift(1).map(tz_offset)
        s["jet_lag"] = ((venue_tz - prev_tz).abs().fillna(0) * (s["rest_days"] <= 1)).astype(float)
        s["altitude_b2b"] = ((s["home_team"].map(altitude_ft) >= HIGH_ALTITUDE_FT) & (s["is_home"] == 0)
                             & (s["rest_days"] == 0)).astype(float)
        # Bounce-back: 2 derrotas ATS seguidas o paliza recibida, en equipo de talento (top-15).
        ats_prev = g["ats_residual"].shift(1)
        ats_prev2 = g["ats_residual"].shift(2)
        s["bounce_back"] = ((((ats_prev < 0) & (ats_prev2 < 0)) | (prev_margin <= -BLOWOUT_LOSS))
                            & (s["team_rank"] <= 15)).astype(float)
        return s

    # ------------------------------------------------------------------ calibración
    def calibrate(self, signals: pd.DataFrame, target_col: str = "ats_residual") -> dict[str, float]:
        """Ridge centrada en priors sobre el residuo ATS (auto-calibración incremental)."""
        names = list(SIGNAL_PRIORS)
        d = signals.dropna(subset=[target_col])
        if d.empty:
            return self.coef
        x = d[names].to_numpy(float)
        y = d[target_col].to_numpy(float)
        prior = np.array([SIGNAL_PRIORS[n] for n in names])
        lam = PRIOR_STRENGTH
        beta = np.linalg.solve(x.T @ x + lam * np.eye(len(names)), x.T @ y + lam * prior)
        self.coef = dict(zip(names, beta.round(3).tolist()))
        log.debug("Ineficiencias calibradas con %d obs: %s", len(d), self.coef)  # 1 vez por fecha en backtest
        return self.coef

    def effect_points(self, row: pd.Series) -> dict[str, float]:
        """Efecto en puntos de margen de cada señal activa para un equipo-partido."""
        return {n: float(self.coef[n] * row.get(n, 0.0)) for n in SIGNAL_PRIORS if row.get(n, 0.0)}

    # ------------------------------------------------------------------ árbitros
    @staticmethod
    def referee_profiles(officials: pd.DataFrame, game_fouls: pd.DataFrame) -> pd.DataFrame:
        """Faltas y TL por partido de cada árbitro (z-score vs liga). `game_fouls`: game_id, fouls, fta."""
        m = officials.merge(game_fouls, on="game_id", how="inner")
        prof = m.groupby("official").agg(n_games=("game_id", "nunique"), fouls=("fouls", "mean"), fta=("fta", "mean"))
        for c in ("fouls", "fta"):
            prof[f"{c}_z"] = (prof[c] - game_fouls[c].mean()) / (game_fouls[c].std() or 1.0)
        return prof.reset_index()

    @staticmethod
    def crew_context(crew: list[str], profiles: pd.DataFrame, team_ftr_z: tuple[float, float]) -> dict[str, float]:
        """φ_context de ritmo (más faltas -> más paradas -> menos posesiones) y modulación de
        viajes a la línea según el estilo de cada equipo (ataque a la pintura = FTr alto)."""
        p = profiles[profiles["official"].isin(crew)]
        if p.empty:
            return {"phi_context": 1.0, "ft_mod_home": 1.0, "ft_mod_away": 1.0, "crew_n": 0}
        w = p["n_games"].clip(upper=60)
        fz = float(np.average(p["fouls_z"], weights=w))
        ftz = float(np.average(p["fta_z"], weights=w))
        shrink = float(w.sum() / (w.sum() + 40.0))
        return {
            "phi_context": 1.0 - REF_PACE_SENSITIVITY * fz * shrink,
            "ft_mod_home": 1.0 + 0.03 * ftz * shrink * (1 + 0.5 * team_ftr_z[0]),
            "ft_mod_away": 1.0 + 0.03 * ftz * shrink * (1 + 0.5 * team_ftr_z[1]),
            "crew_n": int(p["n_games"].sum()),
        }

    # ------------------------------------------------------------------ garbage time
    @staticmethod
    def garbage_relax(margin: np.ndarray, threshold: float, factor: float) -> np.ndarray:
        """Relajación del favorito y entrada de suplentes: el exceso de margen por encima del
        umbral se comprime (los backdoor covers hacen más probable que el perrito recorte)."""
        excess = np.abs(margin) - threshold
        comp = np.where(excess > 0, np.sign(margin) * (threshold + excess * factor), margin)
        return np.rint(comp).astype(margin.dtype)
