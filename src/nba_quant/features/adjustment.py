"""Ajuste por rival (Ridge) y decaimiento exponencial temporal (spec 1 §G, spec 2 §B).

Decaimiento: todas las métricas son cocientes de sumas, así que se decaen las SUMAS
(media exponencial de los conteos de partidos previos) y luego se recalculan los ratios.
Esto pondera cada partido por su volumen real (posesiones, tiros) y no por igual.

Ridge (Regularized APM a nivel equipo): para cada fecha, con los partidos ANTERIORES,
    y_(t,o) = μ + off_t + def_o + h·home  + ε,   peso = posesiones · decaimiento
resuelve a la vez la calidad ofensiva y defensiva de las 30 franquicias.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge

from nba_quant.logging_utils import get_logger

log = get_logger("adjustment")

PRIOR_PSEUDO_GAMES = 5.0
PRIOR_RETENTION = 0.70
AVG_DAYS_BETWEEN_GAMES = 2.1

# Métricas para Ridge: nombre -> (numerador, denominador, escala)
RIDGE_TARGETS: dict[str, tuple[str, str, float]] = {
    "rtg": ("pts", "poss", 100.0),
    "efg": ("efg_num", "fga", 1.0),
    "tov_pct": ("tov", "poss", 1.0),
    "oreb_pct": ("oreb", "oreb_chances", 1.0),
    "ftr": ("fta", "fga", 1.0),
}


def decay_alpha(half_life_games: float) -> float:
    return 1.0 - 0.5 ** (1.0 / half_life_games)


def pregame_decayed_means(game_sums: pd.DataFrame, cols: list[str], half_life_games: float) -> pd.DataFrame:
    """Media exponencial de partidos PREVIOS (shift 1) por (season, team).

    Devuelve las mismas columnas `cols` + `games_played` (nº de partidos previos)."""
    df = game_sums.sort_values(["season", "team", "game_date", "game_id"]).reset_index(drop=True)
    alpha = decay_alpha(half_life_games)
    grp = df.groupby(["season", "team"], sort=False)
    ewm = grp[cols].transform(lambda s: s.ewm(alpha=alpha, adjust=True, ignore_na=True).mean().shift(1))
    out = df[["season", "game_date", "game_id", "team", "opponent", "is_home"]].copy()
    out[cols] = ewm
    out["games_played"] = grp.cumcount()
    return out


def season_end_priors(game_sums: pd.DataFrame, cols: list[str], half_life_games: float) -> pd.DataFrame:
    """Prior de la temporada siguiente: estado decaído final de cada equipo, regresado
    un (1-retención) hacia la media de liga (spec 4: retención 70%)."""
    df = game_sums.sort_values(["season", "team", "game_date"])
    alpha = decay_alpha(half_life_games)
    final = df.groupby(["season", "team"])[cols].agg(lambda s: s.ewm(alpha=alpha, adjust=True).mean().iloc[-1])
    league = final.groupby(level="season").transform("mean")
    prior = PRIOR_RETENTION * final + (1 - PRIOR_RETENTION) * league
    prior = prior.reset_index()
    prior["season"] = prior["season"] + 1  # se aplica a la temporada siguiente
    return prior


def point_in_time_reference(df: pd.DataFrame, cols: list[str], how: str = "median") -> tuple[pd.DataFrame, pd.Series]:
    """Referencia de liga por fila usando SÓLO fechas <= la del partido.

    Agrega por fecha (`how` sobre valores pre-partido, legítimos el mismo día), arrastra hacia
    delante el último valor conocido y, sólo para el arranque del dataset sin ningún pasado,
    rellena hacia atrás. Devuelve (referencia alineada con df, máscara de filas 'cold' que
    necesitaron ese relleno hacia atrás). Sustituye a las medianas globales, que filtraban futuro."""
    dates = pd.to_datetime(df["game_date"])
    daily = df.assign(game_date=dates).groupby("game_date")[cols].agg(how).sort_index().ffill()
    cold_daily = daily.isna()
    ref = daily.bfill().reindex(dates)
    ref.index = df.index
    cold = cold_daily.reindex(dates)
    cold.index = df.index
    return ref, (df[cols].isna() & cold).any(axis=1)


def shrink_to_prior(pregame: pd.DataFrame, priors: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    """Mezcla bayesiana con pseudo-partidos: x = (g·x̂ + k·prior)/(g + k).
    Sin prior del equipo se usa la media de liga a la fecha (point-in-time)."""
    df = pregame.merge(priors, on=["season", "team"], how="left", suffixes=("", "_prior"))
    g = df["games_played"].astype(float)
    k = PRIOR_PSEUDO_GAMES
    league_date, _ = point_in_time_reference(pregame, cols, how="mean")
    league_date.index = df.index
    for c in cols:
        prior = df[f"{c}_prior"] if f"{c}_prior" in df.columns else pd.Series(np.nan, index=df.index)
        prior = prior.fillna(league_date[c])
        cur = df[c]
        df[c] = np.where(cur.isna(), prior, (g * cur + k * prior) / (g + k))
    return df.drop(columns=[c for c in df.columns if c.endswith("_prior")])


def _ridge_one_date(train: pd.DataFrame, teams: list[str], num: str, den: str, scale: float,
                    alpha: float, ref_date: pd.Timestamp, half_life_games: float) -> tuple[dict, dict, float, float]:
    y_rate = scale * train[num] / train[den].replace(0, np.nan)
    ok = y_rate.notna() & np.isfinite(y_rate)
    tr = train[ok]
    y_rate = y_rate[ok]
    mu = float(np.average(y_rate, weights=tr[den]))
    idx = {t: i for i, t in enumerate(teams)}
    n = len(teams)
    x = np.zeros((len(tr), 2 * n + 1))
    rows = np.arange(len(tr))
    x[rows, tr["team"].map(idx).to_numpy()] = 1.0
    x[rows, n + tr["opponent"].map(idx).to_numpy()] = 1.0
    x[:, 2 * n] = np.where(tr["is_home"].to_numpy() == 1, 1.0, -1.0)
    days = (ref_date - tr["game_date"]).dt.days.to_numpy(float)
    decay = 0.5 ** (days / (half_life_games * AVG_DAYS_BETWEEN_GAMES))
    w = tr[den].to_numpy(float) * decay
    model = Ridge(alpha=alpha, fit_intercept=False).fit(x, (y_rate - mu).to_numpy(), sample_weight=w)
    coef = model.coef_
    off = {t: coef[i] for t, i in idx.items()}
    dfn = {t: coef[n + i] for t, i in idx.items()}
    return off, dfn, float(coef[2 * n]), mu


def ridge_opponent_adjustment(game_sums: pd.DataFrame, alpha: float, half_life_games: float,
                              min_games: int = 3) -> pd.DataFrame:
    """Ratings ajustados por rival point-in-time para cada (season, game_date, team) que juega.

    Columnas: adj_off_<m>, adj_def_<m> (desviación vs liga; def = lo que el equipo PERMITE),
    adj_<m>_hca (ventaja local estimada) y adj_net_rtg."""
    gs = game_sums.copy()
    gs["efg_num"] = gs["fgm"] + 0.5 * gs["fg3m"]
    gs["oreb_chances"] = gs["oreb"] + gs["st_MISS_DREB"]
    out = []
    for season, sdf in gs.groupby("season"):
        teams = sorted(set(sdf["team"]) | set(sdf["opponent"]))
        for d in sorted(sdf["game_date"].unique()):
            train = sdf[sdf["game_date"] < d]
            playing = sdf.loc[sdf["game_date"] == d, ["game_id", "team"]]
            row = playing.assign(season=season, game_date=d)
            if train.groupby("team").size().min() < min_games or train["team"].nunique() < len(teams):
                out.append(row)
                continue
            for name, (num, den, scale) in RIDGE_TARGETS.items():
                off, dfn, hca, mu = _ridge_one_date(train, teams, num, den, scale, alpha, d, half_life_games)
                row[f"adj_off_{name}"] = row["team"].map(off)
                row[f"adj_def_{name}"] = row["team"].map(dfn)
                row[f"adj_{name}_hca"] = hca
                row[f"league_{name}"] = mu
            out.append(row)
    res = pd.concat(out, ignore_index=True)
    if "adj_off_rtg" in res.columns:
        res["adj_net_rtg"] = res["adj_off_rtg"] - res["adj_def_rtg"]
        res["adj_ortg"] = res["league_rtg"] + res["adj_off_rtg"]
        res["adj_drtg"] = res["league_rtg"] + res["adj_def_rtg"]
    log.info("Ridge opponent adjustment: %d filas, %.1f%% con ajuste", len(res),
             100 * res.get("adj_off_rtg", pd.Series(dtype=float)).notna().mean() if len(res) else 0)
    return res
