"""Clases 2, 3 y 5 del spec 3: limpieza estadística L5, patrones históricos estructurales y
modificadores dinámicos + generador de escenarios.

Convención: todos los ajustes se expresan en **puntos por 100 posesiones** del equipo, y se
aplican sobre el rating ofensivo esperado antes de entrar al motor de Markov. Cada patrón
histórico se *encoge* hacia 0 con n/(n+k) para que muestras pequeñas no dominen.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from nba_quant.config import CleansingConfig, SimulationConfig
from nba_quant.logging_utils import get_logger

log = get_logger("context")

# Pseudo-partidos de encogimiento hacia 0. Son altos a propósito: el residuo ya está medido
# contra un rating que incorpora esos mismos partidos, así que el patrón es mayormente ruido.
# Calibrado out-of-sample 2025-26 (data/reports/context_calibration_report.md): sólo h2h aporta
# algo; venue/rest/role empeoraban el log-loss de spread en train y se apagan (k = inf -> 0).
# Valores previos: h2h=30, venue=40, rest=60, role=80.
SHRINK_K_H2H = 60.0
SHRINK_K_VENUE = float("inf")
SHRINK_K_REST = float("inf")
SHRINK_K_ROLE = float("inf")
SHRINK_K: dict[str, float] = {"hist_h2h": SHRINK_K_H2H, "hist_venue": SHRINK_K_VENUE,
                              "hist_rest": SHRINK_K_REST, "hist_role": SHRINK_K_ROLE}
MAX_PATTERN_ADJ = 1.5  # tope por patrón (pts/100)
MAX_TOTAL_HIST_ADJ = 2.5  # tope de la suma de patrones históricos (pts/100)
STREAK_REVERSION = 0.15
FATIGUE_MIN_BASELINE = 34.0  # minutos/partido de un titular "normal"
FATIGUE_PER_MIN = 0.08  # pts/100 por minuto/partido de exceso en los últimos 7 días
STAR_MATCHUP_MIN_N = 3
STAR_MATCHUP_BOOST = (0.05, 0.08)


# ======================================================================================
# CLASE 2 — StatisticalCleansingLayer
# ======================================================================================
class StatisticalCleansingLayer:
    """Línea base real L5 con pesos [0.35, 0.25, 0.20, 0.15, 0.05] y taxonomía de sesgos:
    Dominancia/Blowout 1.0 · Clutch 0.95 · Suerte/Varianza de triple 0.85 (pesos de confianza)."""

    def __init__(self, cfg: CleansingConfig) -> None:
        self.cfg = cfg

    def bias_weight(self, margin: float, three_luck: float, three_luck_sd: float) -> float:
        c = self.cfg
        if three_luck_sd > 0 and abs(three_luck) / three_luck_sd > c.luck_three_pct_z:
            return c.weight_luck
        if abs(margin) >= c.blowout_margin:
            return c.weight_blowout
        if abs(margin) <= c.clutch_margin:
            return c.weight_clutch
        return 1.0

    def l5_baseline(self, game_rates: pd.DataFrame, team: str, before: pd.Timestamp,
                    season: int | None = None) -> dict[str, float]:
        """ORtg/DRtg/pace L5 ponderados (más reciente primero) antes de `before`, sólo de la
        temporada en curso (los playoffs/temporada anterior no son "forma actual")."""
        tg = game_rates[(game_rates["team"] == team) & (game_rates["game_date"] < before)]
        if season is not None and "season" in tg.columns:
            tg = tg[tg["season"] == season]
        last = tg.sort_values("game_date", ascending=False).head(len(self.cfg.l5_weights))
        if last.empty:
            return {}
        luck = (last["three_luck_off"].fillna(0) - last["three_luck_def"].fillna(0))
        luck_sd = float(game_rates["three_luck_off"].std() or 0.05)
        w = np.array(self.cfg.l5_weights[: len(last)]) * np.array(
            [self.bias_weight(m, lk, luck_sd) for m, lk in zip(last["net_margin"], luck)])
        w = w / w.sum()
        return {
            "l5_ortg": float(w @ last["ortg"].to_numpy()),
            "l5_drtg": float(w @ last["drtg"].to_numpy()),
            "l5_pace": float(w @ last["pace"].to_numpy()),
            "l5_games": int(len(last)),
        }


# ======================================================================================
# CLASE 3 — DeepHistoricalPatternEngine
# ======================================================================================
def _shrunk_mean(values: pd.Series, k: float) -> tuple[float, int]:
    n = int(values.notna().sum())
    if n == 0:
        return 0.0, 0
    return float(values.mean() * n / (n + k)), n


def _raw_mean(values: pd.Series) -> tuple[float, int]:
    n = int(values.notna().sum())
    return (float(values.mean()), n) if n else (0.0, 0)


class DeepHistoricalPatternEngine:
    """Patrones estructurales sobre el residuo del partido (margen real − margen esperado/línea).

    `history` = una fila por equipo-partido con: team, opponent, is_home, game_date, venue,
    rest_days, is_b2b, is_3in4, residual (pts), is_favorite (bool, opcional).
    `shrink_k` sobrescribe los pseudo-partidos de encogimiento por patrón (claves de SHRINK_K)."""

    def __init__(self, history: pd.DataFrame, shrink_k: dict[str, float] | None = None) -> None:
        self.h = history
        self.k = {**SHRINK_K, **(shrink_k or {})}

    # Residuos de la muestra relevante para cada patrón.
    def _h2h_res(self, team: str, opponent: str) -> pd.Series:
        return self.h.loc[(self.h["team"] == team) & (self.h["opponent"] == opponent), "residual"]

    def _venue_res(self, team: str, venue: str | None) -> pd.Series:
        if not venue:
            return pd.Series(dtype=float)
        return self.h.loc[(self.h["team"] == team) & (self.h["venue"] == venue), "residual"]

    def _rest_res(self, team: str, is_b2b: int, is_3in4: int, rest_days: float) -> pd.Series:
        t = self.h[self.h["team"] == team]
        if is_b2b:
            m = t[t["is_b2b"] == 1]
        elif is_3in4:
            m = t[t["is_3in4"] == 1]
        else:
            m = t[t["rest_days"] >= 2] if rest_days >= 2 else t[t["rest_days"] == 1]
        return m["residual"]

    def _role_res(self, team: str, is_favorite: bool) -> pd.Series:
        if "is_favorite" not in self.h.columns:
            return pd.Series(dtype=float)
        return self.h.loc[(self.h["team"] == team) & (self.h["is_favorite"] == is_favorite), "residual"]

    def h2h(self, team: str, opponent: str) -> tuple[float, int]:
        return _shrunk_mean(self._h2h_res(team, opponent), self.k["hist_h2h"])

    def venue(self, team: str, venue: str | None) -> tuple[float, int]:
        return _shrunk_mean(self._venue_res(team, venue), self.k["hist_venue"])

    def rest(self, team: str, is_b2b: int, is_3in4: int, rest_days: float) -> tuple[float, int]:
        return _shrunk_mean(self._rest_res(team, is_b2b, is_3in4, rest_days), self.k["hist_rest"])

    def role(self, team: str, is_favorite: bool) -> tuple[float, int]:
        return _shrunk_mean(self._role_res(team, is_favorite), self.k["hist_role"])

    def raw_parts(self, team: str, opponent: str, venue: str | None, is_b2b: int, is_3in4: int,
                  rest_days: float, is_favorite: bool) -> dict[str, tuple[float, int]]:
        """(residuo medio SIN encoger, n) por patrón: permite re-encoger con otras k sin re-filtrar."""
        return {
            "hist_h2h": _raw_mean(self._h2h_res(team, opponent)),
            "hist_venue": _raw_mean(self._venue_res(team, venue)),
            "hist_rest": _raw_mean(self._rest_res(team, is_b2b, is_3in4, rest_days)),
            "hist_role": _raw_mean(self._role_res(team, is_favorite)),
        }

    @staticmethod
    def shrink_parts(parts: dict[str, tuple[float, int]], poss: float,
                     shrink_k: dict[str, float]) -> dict[str, float]:
        """Encoge n/(n+k), pasa a pts/100 y aplica los topes por patrón y total."""
        scale = 100.0 / max(poss, 1.0)
        out = {}
        for name, (mean, n) in parts.items():
            k = shrink_k[name]
            shrunk = mean * n / (n + k) if n and np.isfinite(k) else 0.0
            out[name] = float(np.clip(shrunk * scale / 2, -MAX_PATTERN_ADJ, MAX_PATTERN_ADJ))
        total = sum(out.values())
        if abs(total) > MAX_TOTAL_HIST_ADJ:
            out = {k: v * MAX_TOTAL_HIST_ADJ / abs(total) for k, v in out.items()}
        return out

    def team_adjustment(self, team: str, opponent: str, venue: str | None, is_b2b: int, is_3in4: int,
                        rest_days: float, is_favorite: bool, poss: float) -> dict[str, float]:
        """Ajustes en pts/100 (residuo por partido convertido con las posesiones esperadas)."""
        parts = self.raw_parts(team, opponent, venue, is_b2b, is_3in4, rest_days, is_favorite)
        out = self.shrink_parts(parts, poss, self.k)
        out.update({f"{k}_n": v[1] for k, v in parts.items()})
        return out


# ======================================================================================
# CLASE 5 — DynamicModifierEngine
# ======================================================================================
@dataclass
class Scenario:
    """Pts/100 esperados del ataque de un equipo en cada estado."""

    team: str
    base_ortg: float
    best: float
    normal: float
    worst: float
    components: dict[str, float] = field(default_factory=dict)


class DynamicModifierEngine:
    """Integra base + históricos + ineficiencias + factores dinámicos y genera la matriz
    Mejor/Normal/Peor (±shift) de pts/100 por equipo."""

    def __init__(self, sim_cfg: SimulationConfig) -> None:
        self.cfg = sim_cfg

    @staticmethod
    def streak_reversion(recent_residuals: pd.Series) -> float:
        """Reversión a la media de rachas ATS (L5): -15% del residuo medio reciente."""
        if recent_residuals.empty:
            return 0.0
        return float(-STREAK_REVERSION * recent_residuals.tail(5).mean())

    @staticmethod
    def fatigue(player_minutes_7d: pd.DataFrame) -> float:
        """Carga de los 3 jugadores con más minutos en la última semana vs un titular normal."""
        if player_minutes_7d.empty:
            return 0.0
        top = player_minutes_7d.groupby("player_id")["minutes"].agg(["sum", "count"]).nlargest(3, "sum")
        excess = (top["sum"] / top["count"].clip(lower=1) - FATIGUE_MIN_BASELINE).clip(lower=0)
        load = (top["count"] / 3.5).clip(lower=1)  # >3.5 partidos/7 días multiplica la carga
        return float(-(excess * load).sum() * FATIGUE_PER_MIN)

    @staticmethod
    def star_matchup_factor(star_history_vs_opp: pd.Series, star_season_avg: float, star_sd: float,
                            star_share: float) -> float:
        """n<3 -> 1.0. n>=3 -> boost/fricción de 5-8% sobre la PARTE del ataque que genera la
        estrella (su cuota de puntos), según el z-score de su rendimiento vs esta franquicia."""
        n = int(star_history_vs_opp.notna().sum())
        if n < STAR_MATCHUP_MIN_N or star_sd <= 0:
            return 1.0
        z = (star_history_vs_opp.mean() - star_season_avg) / (star_sd / np.sqrt(n))
        lo, hi = STAR_MATCHUP_BOOST
        mag = float(np.clip(lo + (abs(z) - 1.0) * (hi - lo), lo, hi)) if abs(z) >= 1.0 else 0.0
        return 1.0 + np.sign(z) * mag * star_share

    def build_scenario(self, team: str, base_ortg: float, adjustments: dict[str, float],
                       star_factor: float = 1.0) -> Scenario:
        normal = (base_ortg + sum(adjustments.values())) * star_factor
        s = self.cfg.scenario_shift
        return Scenario(team, base_ortg, normal * (1 + s), normal, normal * (1 - s),
                        {**adjustments, "star_factor": star_factor})
