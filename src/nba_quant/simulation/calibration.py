"""Calibración out-of-sample de la pila de contexto: rejilla de `scenario_shift` y de las
constantes de encogimiento de patrones históricos (SHRINK_K), con split temporal
(primera mitad de partidos = train, segunda = test) y objetivo = log-loss de spread.

Cada partido se construye UNA vez (estado point-in-time de su fecha) y se evalúa con todas
las configuraciones usando las mismas semillas (números aleatorios comunes), de forma que
las diferencias entre configuraciones no son ruido de Monte Carlo.
"""

from __future__ import annotations

import os
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, replace

import numpy as np
import pandas as pd

from nba_quant.logging_utils import get_logger
from nba_quant.simulation.context import SHRINK_K, DynamicModifierEngine
from nba_quant.simulation.evaluation import game_seed, mixture_summary, score, score_market
from nba_quant.simulation.monte_carlo import MonteCarloVectorizedCore
from nba_quant.simulation.slate import SlateSimulator

log = get_logger("calibration")

GRID_SIMS = 1_000  # por celda de la rejilla 3×3
SHIFT_GRID = (0.05, 0.10, 0.15, 0.20)
SHRINK_MULTIPLIERS = (0.5, 1.0, 2.0, 4.0, float("inf"))  # inf = patrones históricos apagados
OBJECTIVE = "log_loss_spread"
# Centro de la rejilla: constantes originales (los defaults actuales tienen k = inf).
GRID_CENTER_K: dict[str, float] = {"hist_h2h": 30.0, "hist_venue": 40.0, "hist_rest": 60.0, "hist_role": 80.0}


@dataclass(frozen=True)
class ContextConfig:
    scenario_shift: float
    shrink_k: tuple[tuple[str, float], ...]

    @property
    def k(self) -> dict[str, float]:
        return dict(self.shrink_k)

    @property
    def label(self) -> str:
        ks = ",".join(f"{n.removeprefix('hist_')}={v:g}" for n, v in self.shrink_k)
        return f"shift={self.scenario_shift:.2f}|{ks}"

    @staticmethod
    def make(shift: float, k: dict[str, float]) -> "ContextConfig":
        return ContextConfig(shift, tuple((n, float(k[n])) for n in SHRINK_K))


def multiplier_grid(shifts: tuple[float, ...] = SHIFT_GRID,
                    multipliers: tuple[float, ...] = SHRINK_MULTIPLIERS) -> list[ContextConfig]:
    """Pasada 1: shift × multiplicador común de las cuatro k."""
    return [ContextConfig.make(s, {n: v * m for n, v in GRID_CENTER_K.items()}) for s in shifts for m in multipliers]


def coordinate_grid(best: ContextConfig, multipliers: tuple[float, ...] = SHRINK_MULTIPLIERS) -> list[ContextConfig]:
    """Pasada 2: cada k por separado (las demás fijas en `best`), con el shift de `best`."""
    out = {best}
    for name, k0 in GRID_CENTER_K.items():
        for m in multipliers:
            out.add(ContextConfig.make(best.scenario_shift, {**best.k, name: k0 * m}))
    return sorted(out, key=lambda c: c.label)


# ------------------------------------------------------------------------------ evaluación
_SIM: SlateSimulator | None = None


def _init_worker(sim: SlateSimulator) -> None:
    global _SIM
    _SIM = sim


def evaluate_games(sim: SlateSimulator, game_ids: list[str], configs: list[ContextConfig], n_sims: int,
                   min_games_played: int = 10) -> pd.DataFrame:
    """Una fila por (partido, configuración) con las probabilidades de la mezcla 3×3."""
    hca = sim.cfg.decay.home_court_pts_per100
    odds_tbl = sim._first_odds()
    engines = {c.scenario_shift: DynamicModifierEngine(replace(sim.cfg.sim, scenario_shift=c.scenario_shift))
               for c in configs}
    sim_cfg = replace(sim.cfg.sim, n_sims_block=n_sims)
    rows, state, state_date = [], None, None
    for rh, _ in sim.backtest_pairs(min_games_played, game_ids):
        if rh["game_date"] != state_date:
            state, state_date = sim.context_state(before=rh["game_date"]), rh["game_date"]
        ctx = sim.game_context(rh["game_id"], state=state, odds_tbl=odds_tbl)
        core = MonteCarloVectorizedCore(sim_cfg, ctx.mu, hca, ctx.league)
        seed = game_seed(sim_cfg.seed, rh["game_id"])
        for c in configs:
            sh, sa = sim.scenarios(ctx, engines[c.scenario_shift], c.k)
            grid = core.scenario_grid(ctx.home, ctx.away, sh, sa, ctx.phi, ctx.cross, seed=seed)
            rows.append({"game_id": rh["game_id"], "config": c.label, "scenario_shift": c.scenario_shift,
                         **{f"k_{n.removeprefix('hist_')}": v for n, v in c.shrink_k},
                         **mixture_summary(grid, sim_cfg.scenario_weights, ctx.spread_home)})
    return pd.DataFrame(rows)


def _eval_chunk(args: tuple[list[str], list[ContextConfig], int, int]) -> pd.DataFrame:
    if _SIM is None:
        raise RuntimeError("Worker de calibración sin inicializar")
    return evaluate_games(_SIM, *args)


def evaluate_parallel(sim: SlateSimulator, game_ids: list[str], configs: list[ContextConfig],
                      n_sims: int = GRID_SIMS, min_games_played: int = 10,
                      workers: int | None = None) -> pd.DataFrame:
    """Reparte fechas completas entre procesos (el estado point-in-time se construye por fecha)."""
    workers = workers or max(1, (os.cpu_count() or 2) - 2)
    dates = sim.f.drop_duplicates("game_id").set_index("game_id")["game_date"].reindex(game_ids)
    by_date = [list(g.index) for _, g in dates.groupby(dates)]
    n_chunks = workers * 4
    chunks = [sum(by_date[i::n_chunks], []) for i in range(n_chunks)]
    tasks = [(c, configs, n_sims, min_games_played) for c in chunks if c]
    if workers == 1:
        _init_worker(sim)
        return pd.concat([_eval_chunk(t) for t in tasks], ignore_index=True)
    with ProcessPoolExecutor(workers, initializer=_init_worker, initargs=(sim,)) as pool:
        return pd.concat(list(pool.map(_eval_chunk, tasks)), ignore_index=True)


# ------------------------------------------------------------------------------ resumen
def time_split(bt: pd.DataFrame) -> pd.Timestamp:
    """Fecha de corte: train = partidos con fecha < corte (primera mitad cronológica)."""
    dates = bt.sort_values(["game_date", "game_id"])["game_date"].reset_index(drop=True)
    return pd.Timestamp(dates.iloc[len(dates) // 2])


def _half(df: pd.DataFrame, half: str, split: pd.Timestamp) -> pd.DataFrame:
    if half == "all":
        return df
    return df[df["game_date"] < split] if half == "train" else df[df["game_date"] >= split]


def score_table(preds: pd.DataFrame, base_bt: pd.DataFrame, split: pd.Timestamp) -> pd.DataFrame:
    """Métricas por configuración y mitad. `base_bt` aporta reales y mercado (del backtest base)."""
    ref = base_bt[["game_id", "game_date", "actual_margin", "actual_total", "market_spread"]]
    d = preds.merge(ref, on="game_id", how="inner")
    meta_cols = ["scenario_shift"] + [c for c in d.columns if c.startswith("k_")]
    rows = []
    for half in ("train", "test", "all"):
        for label, g in _half(d, half, split).groupby("config", sort=False):
            rows.append({"half": half, "config": label, **g.iloc[0][meta_cols].to_dict(), **score(g)})
    return pd.DataFrame(rows)


def reference_table(base_bt: pd.DataFrame, ctx_bt: pd.DataFrame | None, split: pd.Timestamp) -> pd.DataFrame:
    """Base, contexto con defaults y cierre de mercado, por mitad (mismos partidos)."""
    rows = []
    for half in ("train", "test", "all"):
        rows.append({"half": half, "model": "base (ratings only)", **score(_half(base_bt, half, split))})
        if ctx_bt is not None and not ctx_bt.empty:
            rows.append({"half": half, "model": "context (current defaults)", **score(_half(ctx_bt, half, split))})
        rows.append({"half": half, "model": "market close", **score_market(_half(base_bt, half, split))})
    return pd.DataFrame(rows)


def pick_best(table: pd.DataFrame, half: str = "train", objective: str = OBJECTIVE) -> str:
    t = table[(table["half"] == half) & table[objective].notna()]
    return str(t.sort_values([objective, "brier"]).iloc[0]["config"])


def to_markdown(df: pd.DataFrame, cols: list[str], digits: int = 4) -> str:
    """Tabla markdown sin depender de `tabulate`."""
    head = "| " + " | ".join(cols) + " |\n|" + "|".join("---" for _ in cols) + "|\n"
    body = []
    for _, r in df[cols].iterrows():
        cells = [f"{v:.{digits}f}" if isinstance(v, (float, np.floating)) else str(v) for v in r]
        body.append("| " + " | ".join(cells) + " |")
    return head + "\n".join(body)


DIAGNOSTIC_SHIFTS = (0.0,)  # fuera del rango pedido: sólo como referencia, nunca se recomienda


def _in_range(table: pd.DataFrame) -> pd.DataFrame:
    return table[table["scenario_shift"].between(min(SHIFT_GRID), max(SHIFT_GRID))]


def run_calibration(sim: SlateSimulator, min_games_played: int = 10, grid_sims: int = GRID_SIMS,
                    context_sims: int | None = None, workers: int | None = None) -> dict[str, object]:
    """Backtest base + contexto (defaults) + rejilla en dos pasadas. Elige en train y sólo
    informa test (la recomendación nunca mira la mitad de test)."""
    base_bt = sim.backtest(min_games_played)
    ctx_bt = sim.backtest(min_games_played, context_sims, mode="context")
    split = time_split(base_bt)
    ids = base_bt["game_id"].tolist()
    configs1 = multiplier_grid() + multiplier_grid(DIAGNOSTIC_SHIFTS, (1.0, float("inf")))
    pass1 = score_table(evaluate_parallel(sim, ids, configs1, grid_sims, min_games_played, workers), base_bt, split)
    best1 = next(c for c in configs1 if c.label == pick_best(_in_range(pass1)))
    configs2 = [c for c in coordinate_grid(best1) if c.label not in set(pass1["config"])]
    pass2 = (score_table(evaluate_parallel(sim, ids, configs2, grid_sims, min_games_played, workers), base_bt, split)
             if configs2 else pass1.iloc[0:0])
    scores = pd.concat([pass1.assign(grid_pass=1), pass2.assign(grid_pass=2)], ignore_index=True)
    best = pick_best(_in_range(scores))
    log.info("Mejor configuración en train: %s", best)
    return {"base_bt": base_bt, "context_bt": ctx_bt, "split": split, "scores": scores, "best": best,
            "reference": reference_table(base_bt, ctx_bt, split)}
