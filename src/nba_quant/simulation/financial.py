"""CLASE 7 — FinancialMarketAnalyzer (spec 3 fase 4): densidad global, desvigado Shin/Power,
Edge ajustado por riesgo (RAE) y Tear Sheet cuantitativo.

  p_modelo   = Σ_{s,t} w_fav(s)·w_dog(t)·p_(s,t)          (pesos Mejor/Normal/Peor = 20/60/20)
  p_LB       = límite inferior Wilson 95% con n = simulaciones efectivas de la mezcla
  p_shin     = probabilidad implícita pura del cierre (método de Shin)
  factor_vol = 1 / (1 + k·σ_bloques)   σ_bloques = dispersión de p entre los 7 bloques dirigidos
  RAE        = (p_LB − p_shin) / p_shin · factor_vol
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from nba_quant.config import MarketConfig, SimulationConfig
from nba_quant.models.devig import american_to_decimal, devig_power, devig_shin
from nba_quant.simulation.monte_carlo import STATES3, MonteCarloOutput

PUSH_EPS = 1e-12


def wilson_lower_bound(p: float, n: int, z: float) -> float:
    if n <= 0:
        return 0.0
    denom = 1 + z**2 / n
    centre = p + z**2 / (2 * n)
    margin = z * np.sqrt(p * (1 - p) / n + z**2 / (4 * n**2))
    return float((centre - margin) / denom)


@dataclass(frozen=True)
class MarketQuote:
    """Un mercado de dos vías: selección evaluada (side) y su contraparte."""

    market: str  # 'moneyline' | 'spread' | 'total'
    side: str  # p.ej. 'BOS', 'BOS -4.5', 'Over 229.5'
    odds_side: float  # americana
    odds_other: float
    line: float | None = None


@dataclass
class EdgeResult:
    quote: MarketQuote
    p_model: float
    p_lb: float
    p_shin: float
    p_power: float
    shin_z: float
    block_sd: float
    vol_factor: float
    rae: float
    breakeven: float
    ev_per_unit: float
    kelly_stake: float
    exploitable: bool


class FinancialMarketAnalyzer:
    def __init__(self, sim_cfg: SimulationConfig, mkt_cfg: MarketConfig) -> None:
        self.sim_cfg = sim_cfg
        self.cfg = mkt_cfg

    # ------------------------------------------------------------------ probabilidad por mercado
    @staticmethod
    def _prob(sim, quote: MarketQuote, home: str, away: str) -> float:
        """P(gana la apuesta | no push) para una simulación."""
        if quote.market == "moneyline":
            p = sim.home_win_prob()
            return p if quote.side.startswith(home) else 1 - p
        if quote.market == "spread":
            is_home = quote.side.startswith(home)
            line = quote.line if quote.line is not None else 0.0
            margin = sim.margin if is_home else -sim.margin
            win, push = float((margin + line > 0).mean()), float((margin + line == 0).mean())
            return win / max(1 - push, PUSH_EPS)
        if quote.market == "total":
            over = quote.side.lower().startswith("over")
            win_o, push = sim.over_prob(quote.line)
            win = win_o if over else 1 - win_o - push
            return win / max(1 - push, PUSH_EPS)
        raise ValueError(f"Mercado desconocido: {quote.market}")

    def density_probability(self, mc: MonteCarloOutput, quote: MarketQuote) -> float:
        w = dict(zip(STATES3, self.sim_cfg.scenario_weights))
        return float(sum(w[f] * w[d] * self._prob(sim, quote, mc.home, mc.away) for (f, d), sim in mc.grid.items()))

    def margin_density(self, mc: MonteCarloOutput) -> pd.Series:
        """Curva de densidad global del margen local (mezcla ponderada de la rejilla 3×3)."""
        w = dict(zip(STATES3, self.sim_cfg.scenario_weights))
        acc: dict[int, float] = {}
        for (f, d), sim in mc.grid.items():
            for k, p in sim.margin_pmf().items():
                acc[k] = acc.get(k, 0.0) + w[f] * w[d] * p
        return pd.Series(acc).sort_index()

    # ------------------------------------------------------------------ edge
    def evaluate(self, mc: MonteCarloOutput, quote: MarketQuote) -> EdgeResult:
        p_model = self.density_probability(mc, quote)
        n_eff = self.sim_cfg.n_sims_block * len(mc.grid)
        p_lb = wilson_lower_bound(p_model, n_eff, self.cfg.ci_z)
        dec = np.array([american_to_decimal(quote.odds_side), american_to_decimal(quote.odds_other)])
        shin, z = devig_shin(dec)
        power, _ = devig_power(dec)
        block_p = np.array([self._prob(b.sim, quote, mc.home, mc.away) for b in mc.blocks.values()])
        block_sd = float(block_p.std())
        vol = 1.0 / (1.0 + self.cfg.volatility_k * block_sd)
        rae = (p_lb - shin[0]) / shin[0] * vol
        breakeven = 1.0 / dec[0]
        ev = p_lb * (dec[0] - 1) - (1 - p_lb)
        b = dec[0] - 1
        kelly = max(0.0, (b * p_lb - (1 - p_lb)) / b) * self.cfg.kelly_fraction
        return EdgeResult(quote, p_model, p_lb, float(shin[0]), float(power[0]), z, block_sd, vol, float(rae),
                          breakeven, float(ev), float(kelly),
                          bool(rae >= self.cfg.min_edge_to_bet and p_lb > breakeven))

    def drawdown_matrix(self, mc: MonteCarloOutput) -> pd.DataFrame:
        """Asimetría de riesgo: distribución del margen del FAVORITO por escenario (B3)."""
        rows = []
        for fs in STATES3:
            sim = mc.grid[(fs, "normal")]
            m = sim.margin if mc.favorite == mc.home else -sim.margin
            rows.append({"escenario_fav": fs, "p_gana": float((m > 0).mean()), "margen_medio": float(m.mean()),
                         "p5_margen": float(np.percentile(m, 5)), "p95_margen": float(np.percentile(m, 95)),
                         "total_medio": float(sim.total.mean())})
        return pd.DataFrame(rows)

    # ------------------------------------------------------------------ reporte
    def tear_sheet(self, mc: MonteCarloOutput, edges: list[EdgeResult]) -> str:
        nn = mc.grid[("normal", "normal")]
        dens = self.margin_density(mc)
        lines = [
            "=" * 78,
            f"TEAR SHEET CUANTITATIVO  {mc.away} @ {mc.home}   (favorito: {mc.favorite})",
            "=" * 78,
            f"Ritmo λ (posesiones/equipo): {nn.meta['lambda_pace']:.1f}   "
            f"PPP objetivo local/visit.: {nn.meta['home_target_ppp']:.3f} / {nn.meta['away_target_ppp']:.3f}",
            f"P(gana local) densidad global: {float(dens[dens.index > 0].sum()):.3f}   "
            f"margen modal (N/N): {nn.modal_margin():+d}   marcador más probable: "
            f"{nn.most_likely_score()[0]}-{nn.most_likely_score()[1]} ({100 * nn.most_likely_score()[2]:.2f}%)",
            "Masa en márgenes clave (N/N): " + ", ".join(f"{k} {v:.3f}" for k, v in nn.critical_margin_mass().items()),
            "",
            "Bloques dirigidos (7 × %d sims):" % self.sim_cfg.n_sims_block,
        ]
        for b in mc.blocks.values():
            fav_m = b.sim.margin if mc.favorite == mc.home else -b.sim.margin
            lines.append(f"  {b.name:10s} {b.description:34s} P(fav gana)={float((fav_m > 0).mean()):.3f} "
                         f"margen fav={fav_m.mean():+6.2f} total={b.sim.total.mean():6.1f}")
        lines += ["", "Matriz de asimetría de riesgo (Fav escenario vs Dog base):",
                  self.drawdown_matrix(mc).round(3).to_string(index=False), "", "Mercados:"]
        for e in edges:
            verdict = "EXPLOTABLE" if e.exploitable else "sin ventaja"
            lines.append(
                f"  {e.quote.market:9s} {e.quote.side:18s} {e.quote.odds_side:+5.0f} | p_mod={e.p_model:.3f} "
                f"p_LB={e.p_lb:.3f} p_shin={e.p_shin:.3f} (z={e.shin_z:.3f}) p_pow={e.p_power:.3f} | "
                f"σ_bloq={e.block_sd:.3f} RAE={100 * e.rae:+.2f}% EV={100 * e.ev_per_unit:+.2f}% "
                f"break-even={e.breakeven:.3f} kelly¼={100 * e.kelly_stake:.2f}% -> {verdict}")
        lines.append("=" * 78)
        return "\n".join(lines)
