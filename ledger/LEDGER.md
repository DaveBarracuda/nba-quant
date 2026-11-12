# Ledger de picks del modelo
_Actualizado: 2026-11-12 19:36 UTC · un pick por partido y mercado (primer snapshot del modelo, con la línea del NBA Odds Tracker en ese momento)._

Picks del workflow de GitHub *Ejecutar modelo* (líneas de ESPN): [github/LEDGER.md](github/LEDGER.md)

**Mercado vs modelo:** ▲ *a favor* = la línea de cierre se movió hacia el número del modelo (CLV positivo); ▼ *en contra* = se alejó; umbral 0.25 pts en spread/total y 0.5 pp de probabilidad en ML. CLV en puntos (spread/total) o en pp de probabilidad sin vig (ML). Spread y total se califican contra la línea del pick a −110; ML al precio del pick.

## Récord

| Grupo | Valor | Picks | Calificados | Récord | WR | Unidades | ROI | CLV medio |
|---|---|---|---|---|---|---|---|---|
| GENERAL | todos | 483 | 483 | 235-248-0 | 48.7% | -38.55 | -8.0% | +0.391 |
| mercado | ml | 161 | 161 | 62-99-0 | 38.5% | -46.86 | -29.1% | +0.005 |
| mercado | spread | 161 | 161 | 82-79-0 | 50.9% | -4.43 | -2.8% | +0.472 |
| mercado | total | 161 | 161 | 91-70-0 | 56.5% | +12.74 | +7.9% | +0.694 |
| movimiento | a favor | 50 | 50 | 30-20-0 | 60.0% | +6.86 | +13.7% | +1.332 |
| movimiento | en contra | 27 | 27 | 12-15-0 | 44.4% | -3.22 | -11.9% | -0.904 |
| movimiento | pendiente | 375 | 375 | 178-197-0 | 47.5% | -39.72 | -10.6% | — |
| movimiento | sin movimiento | 31 | 31 | 15-16-0 | 48.4% | -2.48 | -8.0% | +0.000 |
| mercado × movimiento | ml · a favor | 17 | 17 | 9-8-0 | 52.9% | -0.33 | -1.9% | +0.035 |
| mercado × movimiento | ml · en contra | 13 | 13 | 4-9-0 | 30.8% | -4.61 | -35.5% | -0.031 |
| mercado × movimiento | ml · pendiente | 125 | 125 | 49-76-0 | 39.2% | -35.92 | -28.7% | — |
| mercado × movimiento | ml · sin movimiento | 6 | 6 | 0-6-0 | 0.0% | -6.00 | -100.0% | +0.000 |
| mercado × movimiento | spread · a favor | 16 | 16 | 10-6-0 | 62.5% | +3.27 | +20.4% | +1.812 |
| mercado × movimiento | spread · en contra | 6 | 6 | 2-4-0 | 33.3% | -2.18 | -36.3% | -2.000 |
| mercado × movimiento | spread · pendiente | 125 | 125 | 60-65-0 | 48.0% | -10.58 | -8.5% | — |
| mercado × movimiento | spread · sin movimiento | 14 | 14 | 10-4-0 | 71.4% | +5.06 | +36.1% | +0.000 |
| mercado × movimiento | total · a favor | 17 | 17 | 11-6-0 | 64.7% | +3.92 | +23.1% | +2.176 |
| mercado × movimiento | total · en contra | 8 | 8 | 6-2-0 | 75.0% | +3.57 | +44.6% | -1.500 |
| mercado × movimiento | total · pendiente | 125 | 125 | 69-56-0 | 55.2% | +6.78 | +5.4% | — |
| mercado × movimiento | total · sin movimiento | 11 | 11 | 5-6-0 | 45.5% | -1.53 | -13.9% | +0.000 |

## CLV y movimiento del mercado hacia el modelo

_% hacia el modelo = picks en que la línea se movió a favor ÷ picks con movimiento (sin contar "sin movimiento"); 50% es lo esperado por azar y `p (azar)` es la probabilidad de ver ese % o más si la línea se moviera al azar. CLV medio por pick con cierre conocido, con su intervalo de confianza del 95%: si el intervalo no incluye 0, el CLV es distinguible del azar._

| Mercado | Con cierre | ▲ a favor | ▼ en contra | % hacia el modelo | p (azar) | CLV medio | IC 95% |
|---|---|---|---|---|---|---|---|
| Spread | 36 | 16 | 6 | 72.7% | 0.026 | +0.47 pts | [-0.07, +1.01] |
| Total | 36 | 17 | 8 | 68.0% | 0.054 | +0.69 pts | [+0.13, +1.26] |
| ML | 36 | 17 | 13 | 56.7% | 0.292 | +0.50 pp | [-0.73, +1.72] |
| **Todos** | 108 | 50 | 27 | 64.9% | 0.006 | — | — |

## Picks

| Fecha | Partido | Mercado | Pick | Línea pick | Cierre | Mercado vs modelo | CLV | Alertas | % público en pick | Resultado | Unidades |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-11-11 | OKC @ POR | ML | OKC ML | 54.6% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-11 | OKC @ POR | Spread | OKC -2.5 | -2.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-11 | OKC @ POR | Total | Under 225.5 | 225.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-11 | GS @ HOU | ML | HOU ML | 62.8% | — | … pendiente | — | — | — | ✅ W | +0.53 |
| 2026-11-11 | GS @ HOU | Spread | HOU -5.5 | -5.5 | — | … pendiente | — | — | — | ✅ W | +0.91 |
| 2026-11-11 | GS @ HOU | Total | Over 222.5 | 222.5 | — | … pendiente | — | — | — | ✅ W | +0.91 |
| 2026-11-11 | ORL @ UTAH | ML | UTAH ML | 38.4% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-11 | ORL @ UTAH | Spread | UTAH +4.5 | +4.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-11 | ORL @ UTAH | Total | Over 214.5 | 214.5 | — | … pendiente | — | — | — | ✅ W | +0.91 |
| 2026-11-11 | BKN @ NO | ML | NO ML | 60.0% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-11 | BKN @ NO | Spread | NO -4.5 | -4.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-11 | BKN @ NO | Total | Under 230.5 | 230.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-11 | DEN @ MEM | ML | DEN ML | 59.9% | — | … pendiente | — | — | — | ✅ W | +0.60 |
| 2026-11-11 | DEN @ MEM | Spread | DEN -3.5 | -3.5 | — | … pendiente | — | — | — | ✅ W | +0.87 |
| 2026-11-11 | DEN @ MEM | Total | Over 229.5 | 229.5 | — | … pendiente | — | — | — | ✅ W | +0.93 |
| 2026-11-11 | LAL @ MIL | ML | MIL ML | 14.7% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-11 | LAL @ MIL | Spread | LAL -14.5 | -14.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-11 | LAL @ MIL | Total | Over 228.5 | 228.5 | — | … pendiente | — | — | — | ✅ W | +0.89 |
| 2026-11-11 | SA @ CHI | ML | SA ML | 83.8% | — | … pendiente | — | — | — | ✅ W | +0.15 |
| 2026-11-11 | SA @ CHI | Spread | SA -15.5 | -15.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-11 | SA @ CHI | Total | Under 238.5 | 238.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-11 | BOS @ TOR | ML | TOR ML | 33.8% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-11 | BOS @ TOR | Spread | TOR +5.5 | +5.5 | — | … pendiente | — | — | — | ✅ W | +0.93 |
| 2026-11-11 | BOS @ TOR | Total | Over 215.5 | 215.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-11 | CLE @ NY | ML | NY ML | 61.6% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-11 | CLE @ NY | Spread | NY -3.5 | -3.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-11 | CLE @ NY | Total | Over 221.5 | 221.5 | — | … pendiente | — | — | — | ✅ W | +0.89 |
| 2026-11-11 | WSH @ IND | ML | IND ML | 59.1% | — | … pendiente | — | — | — | ✅ W | +0.62 |
| 2026-11-11 | WSH @ IND | Spread | IND -4.5 | -4.5 | — | … pendiente | — | — | — | ✅ W | +0.95 |
| 2026-11-11 | WSH @ IND | Total | Under 226.5 | 226.5 | — | … pendiente | — | — | — | ✅ W | +0.94 |
| 2026-11-10 | OKC @ POR | ML | OKC ML | 52.7% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-10 | OKC @ POR | Spread | OKC -1.5 | -1.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-10 | OKC @ POR | Total | Under 226.5 | 226.5 | — | … pendiente | — | — | — | ✅ W | +0.88 |
| 2026-11-10 | ORL @ SAC | ML | SAC ML | 37.3% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-10 | ORL @ SAC | Spread | SAC +5.5 | +5.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-10 | ORL @ SAC | Total | Over 221.5 | 221.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-10 | LAC @ PHX | ML | LAC ML | 39.2% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-10 | LAC @ PHX | Spread | LAC +3.5 | +3.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-10 | LAC @ PHX | Total | Over 224.5 | 224.5 | — | … pendiente | — | — | — | ✅ W | +0.93 |
| 2026-11-10 | MIA @ UTAH | ML | UTAH ML | 25.0% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-10 | MIA @ UTAH | Spread | UTAH +10.5 | +10.5 | — | … pendiente | — | — | — | ✅ W | +0.91 |
| 2026-11-10 | MIA @ UTAH | Total | Under 227.5 | 227.5 | — | … pendiente | — | — | — | ✅ W | +0.91 |
| 2026-11-10 | BOS @ PHI | ML | PHI ML | 50.0% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-10 | BOS @ PHI | Spread | BOS +1.5 | +1.5 | — | … pendiente | — | — | — | ✅ W | +0.83 |
| 2026-11-10 | BOS @ PHI | Total | Over 215.5 | 215.5 | — | … pendiente | — | — | — | ✅ W | +0.88 |
| 2026-11-10 | MIL @ NY | ML | NY ML | 88.1% | — | … pendiente | — | — | — | ✅ W | +0.09 |
| 2026-11-10 | MIL @ NY | Spread | NY -15.5 | -15.5 | — | … pendiente | — | — | — | ✅ W | +0.91 |
| 2026-11-10 | MIL @ NY | Total | Over 219.5 | 219.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-09 | NO @ GS | ML | NO ML | 18.3% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-09 | NO @ GS | Spread | NO +11.5 | +11.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-09 | NO @ GS | Total | Over 228.5 | 228.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-09 | SA @ PHX | ML | SA ML | 70.9% | — | … pendiente | — | — | — | ✅ W | +0.36 |
| 2026-11-09 | SA @ PHX | Spread | SA -8.5 | -8.5 | — | … pendiente | — | — | — | ✅ W | +0.91 |
| 2026-11-09 | SA @ PHX | Total | Under 226.5 | 226.5 | — | … pendiente | — | — | — | ✅ W | +0.91 |
| 2026-11-09 | DEN @ HOU | ML | DEN ML | 40.1% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-09 | DEN @ HOU | Spread | DEN +4.5 | +4.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-09 | DEN @ HOU | Total | Over 222.5 | 222.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-09 | IND @ DAL | ML | DAL ML | 63.1% | — | … pendiente | — | — | — | ✅ W | +0.52 |
| 2026-11-09 | IND @ DAL | Spread | DAL -4.5 | -4.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-09 | IND @ DAL | Total | Under 227.5 | 227.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-08 | MIA @ SAC | ML | SAC ML | 26.8% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-08 | MIA @ SAC | Spread | SAC +8.5 | +8.5 | — | … pendiente | — | — | — | ✅ W | +0.88 |
| 2026-11-08 | MIA @ SAC | Total | Under 238.5 | 238.5 | — | … pendiente | — | — | — | ✅ W | +0.88 |
| 2026-11-08 | NO @ LAC | ML | LAC ML | 47.8% | — | … pendiente | — | — | — | ✅ W | +1.01 |
| 2026-11-08 | NO @ LAC | Spread | LAC +1.5 | +1.5 | — | … pendiente | — | — | — | ✅ W | +0.91 |
| 2026-11-08 | NO @ LAC | Total | Under 229.5 | 229.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-08 | BOS @ MIL | ML | MIL ML | 16.8% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-08 | BOS @ MIL | Spread | BOS -12.5 | -12.5 | — | … pendiente | — | — | — | ✅ W | +0.91 |
| 2026-11-08 | BOS @ MIL | Total | Over 222.5 | 222.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-08 | BKN @ DAL | ML | BKN ML | 26.5% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-08 | BKN @ DAL | Spread | BKN +8.5 | +8.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-08 | BKN @ DAL | Total | Under 219.5 | 219.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-08 | UTAH @ MIN | ML | MIN ML | 81.7% | — | … pendiente | — | — | — | ✅ W | +0.18 |
| 2026-11-08 | UTAH @ MIN | Spread | MIN -11.5 | -11.5 | — | … pendiente | — | — | — | ✅ W | +0.88 |
| 2026-11-08 | UTAH @ MIN | Total | Under 222.5 | 222.5 | — | … pendiente | — | — | — | ✅ W | +0.94 |
| 2026-11-08 | LAL @ DET | ML | LAL ML | 37.7% | — | … pendiente | — | — | — | ✅ W | +1.55 |
| 2026-11-08 | LAL @ DET | Spread | LAL +4.5 | +4.5 | — | … pendiente | — | — | — | ✅ W | +0.91 |
| 2026-11-08 | LAL @ DET | Total | Under 222.5 | 222.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-08 | PHI @ CHI | ML | CHI ML | 25.0% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-08 | PHI @ CHI | Spread | CHI +8.5 | +8.5 | — | … pendiente | — | — | — | ✅ W | +0.94 |
| 2026-11-08 | PHI @ CHI | Total | Under 238.5 | 238.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-07 | SA @ POR | ML | POR ML | 34.3% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-07 | SA @ POR | Spread | SA -5.5 | -5.5 | — | … pendiente | — | — | — | ✅ W | +0.89 |
| 2026-11-07 | SA @ POR | Total | Over 226.5 | 226.5 | — | … pendiente | — | — | — | ✅ W | +0.89 |
| 2026-11-07 | HOU @ PHX | ML | PHX ML | 29.0% | — | … pendiente | — | — | — | ✅ W | +2.31 |
| 2026-11-07 | HOU @ PHX | Spread | PHX +6.5 | +6.5 | — | … pendiente | — | — | — | ✅ W | +0.95 |
| 2026-11-07 | HOU @ PHX | Total | Over 224.5 | 224.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-07 | ORL @ GS | ML | ORL ML | 34.3% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-07 | ORL @ GS | Spread | ORL +5.5 | +5.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-07 | ORL @ GS | Total | Over 222.5 | 222.5 | — | … pendiente | — | — | — | ✅ W | +0.91 |
| 2026-11-07 | NY @ CLE | ML | CLE ML | 36.9% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-07 | NY @ CLE | Spread | CLE +4.5 | +4.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-07 | NY @ CLE | Total | Over 224.5 | 224.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-07 | WSH @ OKC | ML | OKC ML | 81.2% | — | … pendiente | — | — | — | ✅ W | +0.18 |
| 2026-11-07 | WSH @ OKC | Spread | OKC -11.5 | -11.5 | — | … pendiente | — | — | — | ✅ W | +0.87 |
| 2026-11-07 | WSH @ OKC | Total | Over 222.5 | 222.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-07 | BKN @ ATL | ML | ATL ML | 70.1% | — | … pendiente | — | — | — | ✅ W | +0.37 |
| 2026-11-07 | BKN @ ATL | Spread | ATL -6.5 | -6.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-07 | BKN @ ATL | Total | Under 226.5 | 226.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-07 | DEN @ IND | ML | DEN ML | 70.0% | — | … pendiente | — | — | — | ✅ W | +0.37 |
| 2026-11-07 | DEN @ IND | Spread | DEN -7.5 | -7.5 | — | … pendiente | — | — | — | ✅ W | +0.94 |
| 2026-11-07 | DEN @ IND | Total | Over 229.5 | 229.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-06 | POR @ LAL | ML | POR ML | 41.7% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-06 | POR @ LAL | Spread | POR +3.5 | +3.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-06 | POR @ LAL | Total | Under 238.5 | 238.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-06 | SA @ SAC | ML | SAC ML | 13.5% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-06 | SA @ SAC | Spread | SA -15.5 | -15.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-06 | SA @ SAC | Total | Over 228.5 | 228.5 | — | … pendiente | — | — | — | ✅ W | +0.91 |
| 2026-11-06 | MIN @ NO | ML | NO ML | 37.3% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-06 | MIN @ NO | Spread | NO +5.5 | +5.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-06 | MIN @ NO | Total | Under 229.5 | 229.5 | — | … pendiente | — | — | — | ✅ W | +0.87 |
| 2026-11-06 | OKC @ MEM | ML | OKC ML | 61.7% | — | … pendiente | — | — | — | ✅ W | +0.56 |
| 2026-11-06 | OKC @ MEM | Spread | OKC -4.5 | -4.5 | — | … pendiente | — | — | — | ✅ W | +0.96 |
| 2026-11-06 | OKC @ MEM | Total | Over 224.5 | 224.5 | — | … pendiente | — | — | — | ✅ W | +0.95 |
| 2026-11-06 | TOR @ MIL | ML | TOR ML | 66.6% | — | … pendiente | — | — | — | ✅ W | +0.44 |
| 2026-11-06 | TOR @ MIL | Spread | TOR -6.5 | -6.5 | — | … pendiente | — | — | — | ✅ W | +0.86 |
| 2026-11-06 | TOR @ MIL | Total | Under 231.5 | 231.5 | — | … pendiente | — | — | — | ✅ W | +0.91 |
| 2026-11-06 | UTAH @ DAL | ML | UTAH ML | 30.9% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-06 | UTAH @ DAL | Spread | DAL -6.5 | -6.5 | — | … pendiente | — | — | — | ✅ W | +0.89 |
| 2026-11-06 | UTAH @ DAL | Total | Under 225.5 | 225.5 | — | … pendiente | — | — | — | ✅ W | +0.91 |
| 2026-11-06 | PHI @ CLE | ML | CLE ML | 52.2% | — | … pendiente | — | — | — | ✅ W | +0.83 |
| 2026-11-06 | PHI @ CLE | Spread | CLE -1.5 | -1.5 | — | … pendiente | — | — | — | ✅ W | +0.91 |
| 2026-11-06 | PHI @ CLE | Total | Under 234.5 | 234.5 | — | … pendiente | — | — | — | ✅ W | +0.87 |
| 2026-11-06 | BOS @ CHA | ML | CHA ML | 22.3% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-06 | BOS @ CHA | Spread | CHA +10.5 | +10.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-06 | BOS @ CHA | Total | Over 207.5 | 207.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-06 | WSH @ ATL | ML | ATL ML | 72.6% | — | … pendiente | — | — | — | ✅ W | +0.32 |
| 2026-11-06 | WSH @ ATL | Spread | ATL -8.5 | -8.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-06 | WSH @ ATL | Total | Under 227.5 | 227.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-05 | MIA @ GS | ML | MIA ML | 40.7% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-05 | MIA @ GS | Spread | MIA +3.5 | +3.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-05 | MIA @ GS | Total | Over 235.5 | 235.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-05 | ORL @ PHX | ML | PHX ML | 51.8% | — | … pendiente | — | — | — | ✅ W | +0.85 |
| 2026-11-05 | ORL @ PHX | Spread | PHX -1.5 | -1.5 | — | … pendiente | — | — | — | ✅ W | +0.98 |
| 2026-11-05 | ORL @ PHX | Total | Over 222.5 | 222.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-04 | MIA @ LAC | ML | LAC ML | 34.3% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-04 | MIA @ LAC | Spread | LAC +5.5 | +5.5 | — | … pendiente | — | — | — | ✅ W | +0.95 |
| 2026-11-04 | MIA @ LAC | Total | Over 233.5 | 233.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-04 | LAL @ SAC | ML | SAC ML | 17.9% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-04 | LAL @ SAC | Spread | LAL -11.5 | -11.5 | — | … pendiente | — | — | — | ✅ W | +0.92 |
| 2026-11-04 | LAL @ SAC | Total | Under 238.5 | 238.5 | — | … pendiente | — | — | — | ✅ W | +0.87 |
| 2026-11-04 | DAL @ SA | ML | SA ML | 80.8% | — | … pendiente | — | — | — | ✅ W | +0.19 |
| 2026-11-04 | DAL @ SA | Spread | SA -11.5 | -11.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-04 | DAL @ SA | Total | Under 227.5 | 227.5 | — | … pendiente | — | — | — | ✅ W | +0.91 |
| 2026-11-04 | POR @ PHX | ML | PHX ML | 42.8% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-04 | POR @ PHX | Spread | PHX +3.5 | +3.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-04 | POR @ PHX | Total | Under 227.5 | 227.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-04 | TOR @ DEN | ML | TOR ML | 35.6% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-04 | TOR @ DEN | Spread | TOR +4.5 | +4.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-04 | TOR @ DEN | Total | Over 231.5 | 231.5 | — | … pendiente | — | — | — | ✅ W | +0.91 |
| 2026-11-04 | MIN @ HOU | ML | MIN ML | 28.2% | — | … pendiente | — | — | — | ✅ W | +2.41 |
| 2026-11-04 | MIN @ HOU | Spread | MIN +8.5 | +8.5 | — | … pendiente | — | — | — | ✅ W | +0.86 |
| 2026-11-04 | MIN @ HOU | Total | Over 219.5 | 219.5 | — | … pendiente | — | — | — | ✅ W | +0.87 |
| 2026-11-04 | CLE @ OKC | ML | OKC ML | 52.3% | — | … pendiente | — | — | — | ✅ W | +0.83 |
| 2026-11-04 | CLE @ OKC | Spread | OKC -1.5 | -1.5 | — | … pendiente | — | — | — | ✅ W | +0.87 |
| 2026-11-04 | CLE @ OKC | Total | Under 227.5 | 227.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-04 | CHA @ BKN | ML | BKN ML | 42.9% | — | … pendiente | — | — | 46 | ✅ W | +1.24 |
| 2026-11-04 | CHA @ BKN | Spread | BKN +3.5 | +3.5 | — | … pendiente | — | — | 73 | ✅ W | +0.88 |
| 2026-11-04 | CHA @ BKN | Total | Under 212.5 | 212.5 | — | … pendiente | — | — | 23 | ❌ L | -1.00 |
| 2026-11-04 | CHI @ NY | ML | NY ML | 82.3% | — | … pendiente | — | — | — | ✅ W | +0.17 |
| 2026-11-04 | CHI @ NY | Spread | NY -12.5 | -12.5 | — | … pendiente | — | — | — | ✅ W | +0.91 |
| 2026-11-04 | CHI @ NY | Total | Under 232.5 | 232.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-04 | MIL @ BOS | ML | MIL ML | 19.6% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-04 | MIL @ BOS | Spread | BOS -11.5 | -11.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-04 | MIL @ BOS | Total | Over 223.5 | 223.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-04 | ATL @ WSH | ML | ATL ML | 52.9% | — | … pendiente | — | — | — | ✅ W | +0.81 |
| 2026-11-04 | ATL @ WSH | Spread | ATL -1.5 | -1.5 | — | … pendiente | — | — | — | ✅ W | +0.88 |
| 2026-11-04 | ATL @ WSH | Total | Under 233.5 | 233.5 | — | … pendiente | — | — | — | ✅ W | +0.91 |
| 2026-11-04 | PHI @ DET | ML | DET ML | 53.2% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-04 | PHI @ DET | Spread | DET -2.5 | -2.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-04 | PHI @ DET | Total | Under 217.5 | 217.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-02 | MIA @ LAL | ML | LAL ML | 55.1% | — | … pendiente | — | — | — | ✅ W | +0.74 |
| 2026-11-02 | MIA @ LAL | Spread | LAL -2.5 | -2.5 | — | … pendiente | — | — | — | ✅ W | +0.93 |
| 2026-11-02 | MIA @ LAL | Total | Over 236.5 | 236.5 | — | … pendiente | — | — | — | ✅ W | +0.91 |
| 2026-11-02 | PHX @ GS | ML | PHX ML | 43.7% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-02 | PHX @ GS | Spread | PHX +2.5 | +2.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-02 | PHX @ GS | Total | Over 227.5 | 227.5 | — | … pendiente | — | — | — | ✅ W | +0.94 |
| 2026-11-02 | TOR @ LAC | ML | TOR ML | 61.7% | — | … pendiente | — | — | — | ✅ W | +0.56 |
| 2026-11-02 | TOR @ LAC | Spread | TOR -4.5 | -4.5 | — | … pendiente | — | — | — | ✅ W | +0.94 |
| 2026-11-02 | TOR @ LAC | Total | Over 219.5 | 219.5 | — | … pendiente | — | — | — | ✅ W | +0.91 |
| 2026-11-02 | POR @ DEN | ML | POR ML | 39.0% | — | … pendiente | — | — | — | ✅ W | +1.46 |
| 2026-11-02 | POR @ DEN | Spread | POR +4.5 | +4.5 | — | … pendiente | — | — | — | ✅ W | +0.86 |
| 2026-11-02 | POR @ DEN | Total | Under 231.5 | 231.5 | — | … pendiente | — | — | — | ✅ W | +0.88 |
| 2026-11-02 | BOS @ HOU | ML | BOS ML | 36.9% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-02 | BOS @ HOU | Spread | BOS +4.5 | +4.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-02 | BOS @ HOU | Total | Over 215.5 | 215.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-02 | UTAH @ SA | ML | SA ML | 88.6% | — | … pendiente | — | — | — | ✅ W | +0.08 |
| 2026-11-02 | UTAH @ SA | Spread | SA -16.5 | -16.5 | — | … pendiente | — | — | — | ✅ W | +0.93 |
| 2026-11-02 | UTAH @ SA | Total | Under 227.5 | 227.5 | — | … pendiente | — | — | — | ✅ W | +0.95 |
| 2026-11-02 | MIL @ MIN | ML | MIN ML | 77.7% | — | … pendiente | — | — | — | ✅ W | +0.24 |
| 2026-11-02 | MIL @ MIN | Spread | MIN -10.5 | -10.5 | — | … pendiente | — | — | — | ✅ W | +0.87 |
| 2026-11-02 | MIL @ MIN | Total | Under 230.5 | 230.5 | — | … pendiente | — | — | — | ✅ W | +0.93 |
| 2026-11-02 | NO @ MEM | ML | NO ML | 35.7% | — | … pendiente | — | — | — | ✅ W | +1.69 |
| 2026-11-02 | NO @ MEM | Spread | NO +5.5 | +5.5 | — | … pendiente | — | — | — | ✅ W | +0.95 |
| 2026-11-02 | NO @ MEM | Total | Over 232.5 | 232.5 | — | … pendiente | — | — | — | ✅ W | +0.94 |
| 2026-11-02 | SAC @ DAL | ML | SAC ML | 25.6% | — | … pendiente | — | — | — | ✅ W | +2.76 |
| 2026-11-02 | SAC @ DAL | Spread | SAC +8.5 | +8.5 | — | … pendiente | — | — | — | ✅ W | +0.88 |
| 2026-11-02 | SAC @ DAL | Total | Under 231.5 | 231.5 | — | … pendiente | — | — | — | ✅ W | +0.91 |
| 2026-11-02 | ATL @ IND | ML | IND ML | 22.3% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-02 | ATL @ IND | Spread | IND +10.5 | +10.5 | — | … pendiente | — | — | — | ✅ W | +0.88 |
| 2026-11-02 | ATL @ IND | Total | Over 229.5 | 229.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-02 | BKN @ NY | ML | BKN ML | 12.5% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-02 | BKN @ NY | Spread | NY -14.5 | -14.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-02 | BKN @ NY | Total | Under 218.5 | 218.5 | — | … pendiente | — | — | — | ✅ W | +0.93 |
| 2026-11-02 | CHI @ PHI | ML | CHI ML | 19.4% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-02 | CHI @ PHI | Spread | PHI -9.5 | -9.5 | — | … pendiente | — | — | — | ✅ W | +0.88 |
| 2026-11-02 | CHI @ PHI | Total | Under 238.5 | 238.5 | — | … pendiente | — | — | — | ✅ W | +0.93 |
| 2026-11-02 | DET @ CHA | ML | CHA ML | 33.2% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-02 | DET @ CHA | Spread | CHA +5.5 | +5.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-02 | DET @ CHA | Total | Under 209.5 | 209.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-02 | WSH @ ORL | ML | ORL ML | 58.4% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-02 | WSH @ ORL | Spread | ORL -3.5 | -3.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-02 | WSH @ ORL | Total | Under 224.5 | 224.5 | — | … pendiente | — | — | — | ✅ W | +0.91 |
| 2026-11-02 | OKC @ CLE | ML | OKC ML | 39.6% | — | … pendiente | — | — | — | ✅ W | +1.42 |
| 2026-11-02 | OKC @ CLE | Spread | OKC +4.5 | +4.5 | — | … pendiente | — | — | — | ✅ W | +0.86 |
| 2026-11-02 | OKC @ CLE | Total | Under 229.5 | 229.5 | — | … pendiente | — | — | — | ✅ W | +0.91 |
| 2026-11-01 | TOR @ LAL | ML | TOR ML | 42.8% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-01 | TOR @ LAL | Spread | TOR +2.5 | +2.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-01 | TOR @ LAL | Total | Under 225.5 | 225.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-01 | LAC @ GS | ML | GS ML | 55.1% | — | … pendiente | — | — | — | ✅ W | +0.74 |
| 2026-11-01 | LAC @ GS | Spread | GS -2.5 | -2.5 | — | … pendiente | — | — | — | ✅ W | +0.95 |
| 2026-11-01 | LAC @ GS | Total | Over 221.5 | 221.5 | — | … pendiente | — | — | — | ✅ W | +0.87 |
| 2026-11-01 | BKN @ IND | ML | IND ML | 60.4% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-01 | BKN @ IND | Spread | IND -3.5 | -3.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-01 | BKN @ IND | Total | Under 231.5 | 231.5 | — | … pendiente | — | — | — | ✅ W | +0.91 |
| 2026-11-01 | BOS @ ORL | ML | ORL ML | 30.9% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-01 | BOS @ ORL | Spread | ORL +6.5 | +6.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-11-01 | BOS @ ORL | Total | Over 220.5 | 220.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-31 | OKC @ HOU | ML | OKC ML | 43.7% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-31 | OKC @ HOU | Spread | OKC +2.5 | +2.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-31 | OKC @ HOU | Total | Under 218.5 | 218.5 | — | … pendiente | — | — | — | ✅ W | +0.91 |
| 2026-10-31 | CLE @ MIL | ML | CLE ML | 75.1% | — | … pendiente | — | — | — | ✅ W | +0.28 |
| 2026-10-31 | CLE @ MIL | Spread | CLE -9.5 | -9.5 | — | … pendiente | — | — | — | ✅ W | +0.95 |
| 2026-10-31 | CLE @ MIL | Total | Under 236.5 | 236.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-31 | MIN @ SA | ML | MIN ML | 19.6% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-31 | MIN @ SA | Spread | MIN +11.5 | +11.5 | — | … pendiente | — | — | — | ✅ W | +0.95 |
| 2026-10-31 | MIN @ SA | Total | Under 227.5 | 227.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-31 | SAC @ MEM | ML | SAC ML | 21.8% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-31 | SAC @ MEM | Spread | SAC +10.5 | +10.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-31 | SAC @ MEM | Total | Over 233.5 | 233.5 | — | … pendiente | — | — | — | ✅ W | +0.91 |
| 2026-10-31 | ATL @ NO | ML | NO ML | 39.6% | — | … pendiente | — | — | — | ✅ W | +1.42 |
| 2026-10-31 | ATL @ NO | Spread | NO +4.5 | +4.5 | — | … pendiente | — | — | — | ✅ W | +0.87 |
| 2026-10-31 | ATL @ NO | Total | Under 239.5 | 239.5 | — | … pendiente | — | — | — | ✅ W | +0.95 |
| 2026-10-31 | PHI @ CHA | ML | CHA ML | 47.8% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-31 | PHI @ CHA | Spread | CHA +1.5 | +1.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-31 | PHI @ CHA | Total | Under 216.5 | 216.5 | — | … pendiente | — | — | — | ✅ W | +0.95 |
| 2026-10-31 | POR @ UTAH | ML | POR ML | 66.4% | — | … pendiente | — | — | — | ✅ W | +0.44 |
| 2026-10-31 | POR @ UTAH | Spread | POR -6.5 | -6.5 | — | … pendiente | — | — | — | ✅ W | +0.91 |
| 2026-10-31 | POR @ UTAH | Total | Under 231.5 | 231.5 | — | … pendiente | — | — | — | ✅ W | +0.95 |
| 2026-10-30 | DEN @ PHX | ML | PHX ML | 45.7% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-30 | DEN @ PHX | Spread | PHX +2.5 | +2.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-30 | DEN @ PHX | Total | Under 233.5 | 233.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-30 | LAL @ GS | ML | LAL ML | 51.1% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-30 | LAL @ GS | Spread | LAL -1.5 | -1.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-30 | LAL @ GS | Total | Under 236.5 | 236.5 | — | … pendiente | — | — | — | ✅ W | +0.91 |
| 2026-10-30 | HOU @ DAL | ML | HOU ML | 62.2% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-30 | HOU @ DAL | Spread | HOU -5.5 | -5.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-30 | HOU @ DAL | Total | Over 227.5 | 227.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-30 | IND @ MIA | ML | MIA ML | 57.2% | — | … pendiente | — | — | — | ✅ W | +0.68 |
| 2026-10-30 | IND @ MIA | Spread | MIA -3.5 | -3.5 | — | … pendiente | — | — | — | ✅ W | +0.91 |
| 2026-10-30 | IND @ MIA | Total | Under 241.5 | 241.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-30 | LAC @ MIN | ML | LAC ML | 25.9% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-30 | LAC @ MIN | Spread | LAC +9.5 | +9.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-30 | LAC @ MIN | Total | Under 230.5 | 230.5 | — | … pendiente | — | — | — | ✅ W | +0.91 |
| 2026-10-30 | CHI @ BOS | ML | CHI ML | 14.8% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-30 | CHI @ BOS | Spread | BOS -15.5 | -15.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-30 | CHI @ BOS | Total | Over 230.5 | 230.5 | — | … pendiente | — | — | — | ✅ W | +0.91 |
| 2026-10-30 | DET @ BKN | ML | BKN ML | 25.2% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-30 | DET @ BKN | Spread | BKN +8.5 | +8.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-30 | DET @ BKN | Total | Under 227.5 | 227.5 | — | … pendiente | — | — | — | ✅ W | +0.91 |
| 2026-10-30 | NY @ PHI | ML | NY ML | 50.4% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-30 | NY @ PHI | Spread | NY -1.5 | -1.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-30 | NY @ PHI | Total | Under 230.5 | 230.5 | — | … pendiente | — | — | — | ✅ W | +0.91 |
| 2026-10-30 | ORL @ TOR | ML | TOR ML | 60.9% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-30 | ORL @ TOR | Spread | TOR -4.5 | -4.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-30 | ORL @ TOR | Total | Under 222.5 | 222.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-30 | CHA @ WSH | ML | CHA ML | 51.1% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-30 | CHA @ WSH | Spread | CHA -1.5 | -1.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-30 | CHA @ WSH | Total | Under 223.5 | 223.5 | — | … pendiente | — | — | — | ✅ W | +0.91 |
| 2026-10-29 | MEM @ POR | ML | POR ML | 71.4% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-29 | MEM @ POR | Spread | POR -7.5 | -7.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-29 | MEM @ POR | Total | Under 232.5 | 232.5 | — | … pendiente | — | — | — | ✅ W | +0.95 |
| 2026-10-29 | CLE @ ATL | ML | ATL ML | 51.1% | — | … pendiente | — | — | — | ✅ W | +0.87 |
| 2026-10-29 | CLE @ ATL | Spread | ATL -1.5 | -1.5 | — | … pendiente | — | — | — | ✅ W | +0.95 |
| 2026-10-29 | CLE @ ATL | Total | Under 237.5 | 237.5 | — | … pendiente | — | — | — | ✅ W | +0.95 |
| 2026-10-29 | SAC @ NO | ML | SAC ML | 32.5% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-29 | SAC @ NO | Spread | NO -5.5 | -5.5 | — | … pendiente | — | — | — | ✅ W | +0.85 |
| 2026-10-29 | SAC @ NO | Total | Under 236.5 | 236.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-28 | LAL @ LAC | ML | LAL ML | 64.5% | — | … pendiente | — | — | — | ✅ W | +0.49 |
| 2026-10-28 | LAL @ LAC | Spread | LAL -5.5 | -5.5 | — | … pendiente | — | — | — | ✅ W | +0.95 |
| 2026-10-28 | LAL @ LAC | Total | Under 228.5 | 228.5 | — | … pendiente | — | — | — | ✅ W | +0.87 |
| 2026-10-28 | OKC @ DAL | ML | OKC ML | 64.5% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-28 | OKC @ DAL | Spread | OKC -5.5 | -5.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-28 | OKC @ DAL | Total | Under 230.5 | 230.5 | — | … pendiente | — | — | — | ✅ W | +0.91 |
| 2026-10-28 | SA @ UTAH | ML | UTAH ML | 18.3% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-28 | SA @ UTAH | Spread | UTAH +12.5 | +12.5 | — | … pendiente | — | — | — | ✅ W | +0.91 |
| 2026-10-28 | SA @ UTAH | Total | Under 234.5 | 234.5 | — | … pendiente | — | — | — | ✅ W | +0.87 |
| 2026-10-28 | DEN @ NO | ML | NO ML | 37.8% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-28 | DEN @ NO | Spread | NO +4.5 | +4.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-28 | DEN @ NO | Total | Under 238.5 | 238.5 | — | … pendiente | — | — | — | ✅ W | +0.95 |
| 2026-10-28 | GS @ MIN | ML | MIN ML | 58.3% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-28 | GS @ MIN | Spread | MIN -3.5 | -3.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-28 | GS @ MIN | Total | Over 225.5 | 225.5 | — | … pendiente | — | — | — | ✅ W | +0.91 |
| 2026-10-28 | HOU @ MIL | ML | HOU ML | 72.6% | — | … pendiente | — | — | — | ✅ W | +0.32 |
| 2026-10-28 | HOU @ MIL | Spread | HOU -8.5 | -8.5 | — | … pendiente | — | — | — | ✅ W | +0.91 |
| 2026-10-28 | HOU @ MIL | Total | Over 227.5 | 227.5 | — | … pendiente | — | — | — | ✅ W | +0.87 |
| 2026-10-28 | NY @ CHI | ML | NY ML | 70.0% | — | … pendiente | — | — | — | ✅ W | +0.37 |
| 2026-10-28 | NY @ CHI | Spread | NY -7.5 | -7.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-28 | NY @ CHI | Total | Under 234.5 | 234.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-28 | ORL @ TOR | ML | TOR ML | 60.9% | — | … pendiente | — | — | — | ✅ W | +0.57 |
| 2026-10-28 | ORL @ TOR | Spread | TOR -4.5 | -4.5 | — | … pendiente | — | — | — | ✅ W | +0.91 |
| 2026-10-28 | ORL @ TOR | Total | Under 223.5 | 223.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-28 | CHA @ DET | ML | CHA ML | 28.6% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-28 | CHA @ DET | Spread | CHA +7.5 | +7.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-28 | CHA @ DET | Total | Under 216.5 | 216.5 | — | … pendiente | — | — | — | ✅ W | +0.87 |
| 2026-10-28 | MIA @ ATL | ML | ATL ML | 59.3% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-28 | MIA @ ATL | Spread | ATL -3.5 | -3.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-28 | MIA @ ATL | Total | Under 239.5 | 239.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-28 | PHI @ IND | ML | IND ML | 40.0% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-28 | PHI @ IND | Spread | IND +4.5 | +4.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-28 | PHI @ IND | Total | Under 237.5 | 237.5 | — | … pendiente | — | — | — | ✅ W | +0.91 |
| 2026-10-28 | WSH @ CLE | ML | WSH ML | 23.4% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-28 | WSH @ CLE | Spread | CLE -10.5 | -10.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-28 | WSH @ CLE | Total | Under 239.5 | 239.5 | — | … pendiente | — | — | — | ✅ W | +0.91 |
| 2026-10-27 | POR @ LAL | ML | LAL ML | 53.2% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-27 | POR @ LAL | Spread | LAL -1.5 | -1.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-27 | POR @ LAL | Total | Under 233.5 | 233.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-26 | GS @ DEN | ML | GS ML | 28.6% | — | … pendiente | — | — | — | ✅ W | +2.35 |
| 2026-10-26 | GS @ DEN | Spread | GS +7.5 | +7.5 | — | … pendiente | — | — | — | ✅ W | +0.91 |
| 2026-10-26 | GS @ DEN | Total | Under 235.5 | 235.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-26 | MEM @ UTAH | ML | UTAH ML | 49.6% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-26 | MEM @ UTAH | Spread | UTAH +1.5 | +1.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-26 | MEM @ UTAH | Total | Over 237.5 | 237.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-26 | ATL @ HOU | ML | ATL ML | 34.3% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-26 | ATL @ HOU | Spread | ATL +5.5 | +5.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-26 | ATL @ HOU | Total | Under 229.5 | 229.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-26 | IND @ MIL | ML | IND ML | 60.0% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-26 | IND @ MIL | Spread | IND -4.5 | -4.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-26 | IND @ MIL | Total | Over 238.5 | 238.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-26 | PHX @ OKC | ML | OKC ML | 77.2% | — | … pendiente | — | — | — | ✅ W | +0.24 |
| 2026-10-26 | PHX @ OKC | Spread | OKC -10.5 | -10.5 | — | … pendiente | — | — | — | ✅ W | +0.91 |
| 2026-10-26 | PHX @ OKC | Total | Under 220.5 | 220.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-26 | CHI @ BOS | ML | CHI ML | 14.2% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-26 | CHI @ BOS | Spread | CHI +13.5 | +13.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-26 | CHI @ BOS | Total | Under 233.5 | 233.5 | — | … pendiente | — | — | — | ✅ W | +0.91 |
| 2026-10-26 | DAL @ MIA | ML | DAL ML | 28.6% | — | … pendiente | — | — | — | ✅ W | +2.35 |
| 2026-10-26 | DAL @ MIA | Spread | DAL +7.5 | +7.5 | — | … pendiente | — | — | — | ✅ W | +0.91 |
| 2026-10-26 | DAL @ MIA | Total | Over 235.5 | 235.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-26 | MIN @ CLE | ML | MIN ML | 38.4% | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-26 | MIN @ CLE | Spread | MIN +4.5 | +4.5 | — | … pendiente | — | — | — | ✅ W | +0.87 |
| 2026-10-26 | MIN @ CLE | Total | Under 233.5 | 233.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-26 | WSH @ CHA | ML | CHA ML | 56.3% | — | … pendiente | — | — | — | ✅ W | +0.70 |
| 2026-10-26 | WSH @ CHA | Spread | CHA -2.5 | -2.5 | — | … pendiente | — | — | — | ✅ W | +0.87 |
| 2026-10-26 | WSH @ CHA | Total | Under 228.5 | 228.5 | — | … pendiente | — | — | — | ✅ W | +0.91 |
| 2026-10-25 | MEM @ SAC | ML | SAC ML | 40.0% | — | … pendiente | — | — | 22 | ❌ L | -1.00 |
| 2026-10-25 | MEM @ SAC | Spread | SAC +3.5 | +3.5 | — | … pendiente | — | — | — | ❌ L | -1.00 |
| 2026-10-25 | MEM @ SAC | Total | Over 234.5 | 234.5 | — | … pendiente | — | — | 75 | ✅ W | +0.91 |
| 2026-10-25 | DET @ PHI | ML | DET ML | 49.6% | — | … pendiente | — | — | — | ✅ W | +0.93 |
| 2026-10-25 | DET @ PHI | Spread | DET -1.5 | -1.5 | — | … pendiente | — | — | — | ✅ W | +0.98 |
| 2026-10-25 | DET @ PHI | Total | Under 227.5 | 227.5 | — | … pendiente | — | — | — | ✅ W | +0.95 |
| 2026-10-25 | LAC @ OKC | ML | LAC ML | 10.7% | — | … pendiente | — | — | 5 | ❌ L | -1.00 |
| 2026-10-25 | LAC @ OKC | Spread | LAC +16.5 | +16.5 | — | … pendiente | — | — | 18 | ✅ W | +0.87 |
| 2026-10-25 | LAC @ OKC | Total | Under 224.5 | 224.5 | — | … pendiente | — | — | 17 | ✅ W | +0.89 |
| 2026-10-25 | ORL @ NY | ML | NY ML | 71.8% | — | … pendiente | — | — | 92 | ❌ L | -1.00 |
| 2026-10-25 | ORL @ NY | Spread | NY -7.5 | -7.5 | — | … pendiente | — | — | 63 | ❌ L | -1.00 |
| 2026-10-25 | ORL @ NY | Total | Under 224.5 | 224.5 | — | … pendiente | — | — | 16 | ✅ W | +0.87 |
| 2026-10-25 | TOR @ MIN | ML | MIN ML | 51.1% | — | … pendiente | — | — | 80 | ✅ W | +0.87 |
| 2026-10-25 | TOR @ MIN | Spread | TOR +1.5 | +1.5 | — | … pendiente | — | — | 28 | ❌ L | -1.00 |
| 2026-10-25 | TOR @ MIN | Total | Under 229.5 | 229.5 | — | … pendiente | — | — | 24 | ✅ W | +0.93 |
| 2026-10-25 | IND @ BKN | ML | BKN ML | 29.5% | — | … pendiente | — | — | 12 | ❌ L | -1.00 |
| 2026-10-25 | IND @ BKN | Spread | BKN +7.5 | +7.5 | — | … pendiente | — | — | 24 | ❌ L | -1.00 |
| 2026-10-25 | IND @ BKN | Total | Under 231.5 | 231.5 | — | … pendiente | — | — | 29 | ❌ L | -1.00 |
| 2026-10-25 | LAL @ UTAH | ML | UTAH ML | 31.9% | — | … pendiente | — | — | 8 | ❌ L | -1.00 |
| 2026-10-25 | LAL @ UTAH | Spread | LAL -6.5 | -6.5 | — | … pendiente | — | — | 82 | ✅ W | +0.93 |
| 2026-10-25 | LAL @ UTAH | Total | Under 237.5 | 237.5 | — | … pendiente | — | — | 23 | ❌ L | -1.00 |
| 2026-10-24 | GS @ PHX | ML | GS ML | 24.3% | 22.8% | ▼ en contra | -1.43 | — | 22 | ❌ L | -1.00 |
| 2026-10-24 | GS @ PHX | Spread | GS +9.5 | +9.5 | +9.5 | = sin mov. | -0.00 | — | 68 | ✅ W | +0.89 |
| 2026-10-24 | GS @ PHX | Total | Over 221.5 | 221.5 | 221.5 | = sin mov. | +0.00 | RLM | 72 | ✅ W | +0.87 |
| 2026-10-24 | NO @ DEN | ML | NO ML | 20.4% | 20.4% | = sin mov. | -0.00 | — | 4 | ❌ L | -1.00 |
| 2026-10-24 | NO @ DEN | Spread | NO +11.5 | +11.5 | +11.5 | = sin mov. | -0.00 | — | 47 | ✅ W | +0.87 |
| 2026-10-24 | NO @ DEN | Total | Under 239.5 | 239.5 | 239.5 | = sin mov. | -0.00 | — | 47 | ❌ L | -1.00 |
| 2026-10-24 | HOU @ ATL | ML | ATL ML | 51.1% | 49.6% | ▼ en contra | -1.52 | — | 49 | ❌ L | -1.00 |
| 2026-10-24 | HOU @ ATL | Spread | ATL -1.5 | -1.5 | +1.5 | ▼ en contra | -3.00 | INFO | 37 | ❌ L | -1.00 |
| 2026-10-24 | HOU @ ATL | Total | Under 227.5 | 227.5 | 227.5 | = sin mov. | -0.00 | — | 31 | ❌ L | -1.00 |
| 2026-10-24 | SA @ DAL | ML | DAL ML | 17.8% | 13.7% | ▼ en contra | -4.07 | INFO | 10 | ❌ L | -1.00 |
| 2026-10-24 | SA @ DAL | Spread | DAL +12.5 | +12.5 | +14.5 | ▼ en contra | -2.00 | INFO,STEAM | 56 | ❌ L | -1.00 |
| 2026-10-24 | SA @ DAL | Total | Under 232.5 | 232.5 | 229.5 | ▲ a favor | +3.00 | INFO,RLM | 31 | ✅ W | +0.89 |
| 2026-10-24 | WSH @ CHI | ML | CHI ML | 52.6% | 53.2% | ▲ a favor | +0.64 | RLM | 61 | ❌ L | -1.00 |
| 2026-10-24 | WSH @ CHI | Spread | CHI -2.5 | -2.5 | -1.5 | ▼ en contra | -1.00 | INFO,RLM | 41 | ❌ L | -1.00 |
| 2026-10-24 | WSH @ CHI | Total | Under 244.5 | 244.5 | 244.5 | = sin mov. | -0.00 | — | 49 | ✅ W | +0.87 |
| 2026-10-24 | BKN @ CLE | ML | BKN ML | 20.0% | 20.0% | = sin mov. | -0.00 | — | 5 | ❌ L | -1.00 |
| 2026-10-24 | BKN @ CLE | Spread | BKN +11.5 | +11.5 | +11.5 | = sin mov. | -0.00 | — | 29 | ✅ W | +0.89 |
| 2026-10-24 | BKN @ CLE | Total | Under 228.5 | 228.5 | 228.5 | = sin mov. | -0.00 | — | 44 | ❌ L | -1.00 |
| 2026-10-24 | MIL @ PHI | ML | MIL ML | 16.3% | 16.3% | = sin mov. | -0.00 | — | 7 | ❌ L | -1.00 |
| 2026-10-24 | MIL @ PHI | Spread | MIL +12.5 | +12.5 | +12.5 | = sin mov. | -0.00 | STEAM | 41 | ✅ W | +0.91 |
| 2026-10-24 | MIL @ PHI | Total | Under 235.5 | 235.5 | 234.5 | ▲ a favor | +1.00 | — | 47 | ❌ L | -1.00 |
| 2026-10-24 | MIA @ CHA | ML | CHA ML | 43.7% | 38.4% | ▼ en contra | -5.29 | — | 11 | ✅ W | +1.20 |
| 2026-10-24 | MIA @ CHA | Spread | CHA +3.5 | +3.5 | +4.5 | ▼ en contra | -1.00 | STEAM | 18 | ✅ W | +0.87 |
| 2026-10-24 | MIA @ CHA | Total | Under 229.5 | 229.5 | 227.5 | ▲ a favor | +2.00 | RLM | 21 | ✅ W | +0.89 |
| 2026-10-23 | LAC @ LAL | ML | LAC ML | 23.4% | 24.9% | ▲ a favor | +1.51 | RLM | 5 | ❌ L | -1.00 |
| 2026-10-23 | LAC @ LAL | Spread | LAC +9.5 | +9.5 | +8.5 | ▲ a favor | +1.00 | RLM | 35 | ✅ W | +0.89 |
| 2026-10-23 | LAC @ LAL | Total | Under 228.5 | 228.5 | 225.5 | ▲ a favor | +3.00 | RLM | 11 | ❌ L | -1.00 |
| 2026-10-23 | MEM @ GS | ML | GS ML | 58.3% | 58.3% | = sin mov. | +0.00 | — | 89 | ❌ L | -1.00 |
| 2026-10-23 | MEM @ GS | Spread | GS -3.5 | -3.5 | -4.5 | ▲ a favor | +1.00 | STEAM | 72 | ❌ L | -1.00 |
| 2026-10-23 | MEM @ GS | Total | Under 235.5 | 235.5 | 236.5 | ▼ en contra | -1.00 | — | 29 | ✅ W | +0.91 |
| 2026-10-23 | POR @ SAC | ML | POR ML | 72.2% | 79.1% | ▲ a favor | +6.93 | — | 97 | ✅ W | +0.33 |
| 2026-10-23 | POR @ SAC | Spread | POR -7.5 | -7.5 | -9.5 | ▲ a favor | +2.00 | — | 88 | ✅ W | +0.91 |
| 2026-10-23 | POR @ SAC | Total | Under 232.5 | 232.5 | 231.5 | ▲ a favor | +1.00 | RLM | 34 | ❌ L | -1.00 |
| 2026-10-23 | HOU @ SA | ML | HOU ML | 30.0% | 37.8% | ▲ a favor | +7.77 | RLM | 9 | ✅ W | +2.20 |
| 2026-10-23 | HOU @ SA | Spread | HOU +6.5 | +6.5 | +4.5 | ▲ a favor | +2.00 | — | 46 | ✅ W | +0.95 |
| 2026-10-23 | HOU @ SA | Total | Under 225.5 | 225.5 | 224.5 | ▲ a favor | +1.00 | RLM | 17 | ✅ W | +0.91 |
| 2026-10-23 | NO @ UTAH | ML | NO ML | 44.9% | 49.6% | ▲ a favor | +4.71 | — | 44 | ❌ L | -1.00 |
| 2026-10-23 | NO @ UTAH | Spread | NO +2.5 | +2.5 | +1.5 | ▲ a favor | +1.00 | — | 75 | ✅ W | +0.93 |
| 2026-10-23 | NO @ UTAH | Total | Under 238.5 | 238.5 | 238.5 | = sin mov. | -0.00 | — | 24 | ❌ L | -1.00 |
| 2026-10-23 | DET @ MIA | ML | DET ML | 46.8% | 54.3% | ▲ a favor | +7.52 | RLM | 53 | ✅ W | +1.05 |
| 2026-10-23 | DET @ MIA | Spread | DET +1.5 | +1.5 | -2.5 | ▲ a favor | +4.00 | STEAM | 58 | ✅ W | +0.95 |
| 2026-10-23 | DET @ MIA | Total | Under 234.5 | 234.5 | 235.5 | ▼ en contra | -1.00 | — | 26 | ❌ L | -1.00 |
| 2026-10-23 | ATL @ CHA | ML | CHA ML | 43.7% | 43.7% | = sin mov. | +0.00 | — | 13 | ❌ L | -1.00 |
| 2026-10-23 | ATL @ CHA | Spread | CHA +2.5 | +2.5 | +2.5 | = sin mov. | +0.00 | — | 18 | ❌ L | -1.00 |
| 2026-10-23 | ATL @ CHA | Total | Over 225.5 | 225.5 | 226.5 | ▲ a favor | +1.00 | — | 94 | ❌ L | -1.00 |
| 2026-10-23 | DAL @ IND | ML | DAL ML | 33.6% | 30.4% | ▼ en contra | -3.21 | — | 9 | ✅ W | +1.85 |
| 2026-10-23 | DAL @ IND | Spread | IND -5.5 | -5.5 | -7.5 | ▲ a favor | +2.00 | — | 69 | ❌ L | -1.00 |
| 2026-10-23 | DAL @ IND | Total | Over 236.5 | 236.5 | 241.5 | ▲ a favor | +5.00 | INFO | 86 | ❌ L | -1.00 |
| 2026-10-23 | MIN @ ORL | ML | ORL ML | 46.8% | 52.6% | ▲ a favor | +5.86 | RLM | 20 | ❌ L | -1.00 |
| 2026-10-23 | MIN @ ORL | Spread | ORL +1.5 | +1.5 | -1.5 | ▲ a favor | +3.00 | RLM | 21 | ❌ L | -1.00 |
| 2026-10-23 | MIN @ ORL | Total | Under 236.5 | 236.5 | 234.5 | ▲ a favor | +2.00 | RLM | 23 | ✅ W | +0.91 |
| 2026-10-23 | NY @ BOS | ML | BOS ML | 55.1% | 56.3% | ▲ a favor | +1.21 | — | 65 | ✅ W | +0.74 |
| 2026-10-23 | NY @ BOS | Spread | BOS -2.5 | -2.5 | -2.5 | = sin mov. | +0.00 | — | 56 | ✅ W | +0.91 |
| 2026-10-23 | NY @ BOS | Total | Under 223.5 | 223.5 | 220.5 | ▲ a favor | +3.00 | RLM | 25 | ✅ W | +0.91 |
| 2026-10-23 | TOR @ WSH | ML | TOR ML | 65.7% | 74.1% | ▲ a favor | +8.34 | — | 89 | ✅ W | +0.46 |
| 2026-10-23 | TOR @ WSH | Spread | TOR -5.5 | -5.5 | -9.5 | ▲ a favor | +4.00 | — | 63 | ✅ W | +0.95 |
| 2026-10-23 | TOR @ WSH | Total | Under 236.5 | 236.5 | 236.5 | = sin mov. | -0.00 | — | 10 | ✅ W | +0.89 |
| 2026-10-23 | CHI @ MIL | ML | MIL ML | 51.1% | 51.1% | = sin mov. | +0.00 | — | 63 | ❌ L | -1.00 |
| 2026-10-23 | CHI @ MIL | Spread | MIL -1.5 | -1.5 | -1.5 | = sin mov. | +0.00 | — | 44 | ❌ L | -1.00 |
| 2026-10-23 | CHI @ MIL | Total | Under 237.5 | 237.5 | 237.5 | = sin mov. | -0.00 | — | 39 | ❌ L | -1.00 |
| 2026-10-22 | DEN @ OKC | ML | DEN ML | 27.4% | 25.9% | ▼ en contra | -1.51 | — | 9 | ❌ L | -1.00 |
| 2026-10-22 | DEN @ OKC | Spread | DEN +7.5 | +7.5 | +7.5 | = sin mov. | -0.00 | — | 56 | ❌ L | -1.00 |
| 2026-10-22 | DEN @ OKC | Total | Under 235.5 | 235.5 | 236.5 | ▼ en contra | -1.00 | — | 31 | ✅ W | +0.91 |
| 2026-10-22 | CLE @ PHI | ML | CLE ML | 41.7% | 40.7% | ▼ en contra | -1.04 | GRADUAL | 14 | ❌ L | -1.00 |
| 2026-10-22 | CLE @ PHI | Spread | CLE +3.5 | +3.5 | +2.5 | ▲ a favor | +1.00 | STEAM | 73 | ❌ L | -1.00 |
| 2026-10-22 | CLE @ PHI | Total | Under 235.5 | 235.5 | 235.5 | = sin mov. | -0.00 | — | 39 | ✅ W | +0.93 |
| 2026-10-21 | SAC @ LAC | ML | LAC ML | 60.9% | 62.2% | ▲ a favor | +1.32 | GRADUAL | 91 | ✅ W | +0.57 |
| 2026-10-21 | SAC @ LAC | Spread | LAC -4.5 | -4.5 | -4.5 | = sin mov. | +0.00 | INFO | 73 | ✅ W | +0.91 |
| 2026-10-21 | SAC @ LAC | Total | Over 229.5 | 229.5 | 226.5 | ▼ en contra | -3.00 | RLM | 76 | ❌ L | -1.00 |
| 2026-10-21 | PHX @ POR | ML | PHX ML | 40.0% | 41.7% | ▲ a favor | +1.66 | RLM | 16 | ❌ L | -1.00 |
| 2026-10-21 | PHX @ POR | Spread | PHX +4.5 | +4.5 | +3.5 | ▲ a favor | +1.00 | STEAM | 43 | ❌ L | -1.00 |
| 2026-10-21 | PHX @ POR | Total | Under 235.5 | 235.5 | 232.5 | ▲ a favor | +3.00 | RLM,STEAM | 35 | ✅ W | +0.91 |
| 2026-10-21 | GS @ LAL | ML | LAL ML | 70.5% | 66.9% | ▼ en contra | -3.60 | RLM | 82 | ✅ W | +0.36 |
| 2026-10-21 | GS @ LAL | Spread | LAL -7.5 | -7.5 | -6.5 | ▼ en contra | -1.00 | STEAM | 29 | ✅ W | +0.95 |
| 2026-10-21 | GS @ LAL | Total | Over 230.5 | 230.5 | 233.5 | ▲ a favor | +3.00 | — | 62 | ✅ W | +0.91 |
| 2026-10-21 | DAL @ HOU | ML | DAL ML | 26.6% | 22.3% | ▼ en contra | -4.33 | — | 8 | ❌ L | -1.00 |
| 2026-10-21 | DAL @ HOU | Spread | HOU -8.5 | -8.5 | -9.5 | ▲ a favor | +1.00 | RLM | 38 | ✅ W | +0.98 |
| 2026-10-21 | DAL @ HOU | Total | Over 229.5 | 229.5 | 230.5 | ▲ a favor | +1.00 | — | 66 | ✅ W | +0.87 |
| 2026-10-21 | IND @ NO | ML | NO ML | 41.7% | 43.7% | ▲ a favor | +1.95 | — | 16 | ❌ L | -1.00 |
| 2026-10-21 | IND @ NO | Spread | NO +3.5 | +3.5 | +2.5 | ▲ a favor | +1.00 | — | 40 | ✅ W | +0.91 |
| 2026-10-21 | IND @ NO | Total | Over 241.5 | 241.5 | 238.5 | ▼ en contra | -3.00 | — | 52 | ✅ W | +0.95 |
| 2026-10-21 | UTAH @ MEM | ML | UTAH ML | 50.4% | 46.8% | ▼ en contra | -3.68 | RLM | 70 | ❌ L | -1.00 |
| 2026-10-21 | UTAH @ MEM | Spread | MEM +1.5 | +1.5 | -1.5 | ▲ a favor | +3.00 | RLM | 37 | ✅ W | +0.87 |
| 2026-10-21 | UTAH @ MEM | Total | Under 242.5 | 242.5 | 240.5 | ▲ a favor | +2.00 | — | 48 | ✅ W | +0.87 |
| 2026-10-21 | CHI @ TOR | ML | TOR ML | 76.6% | 79.1% | ▲ a favor | +2.55 | — | 92 | ✅ W | +0.25 |
| 2026-10-21 | CHI @ TOR | Spread | TOR -9.5 | -9.5 | -10.5 | ▲ a favor | +1.00 | — | 52 | ✅ W | +0.93 |
| 2026-10-21 | CHI @ TOR | Total | Under 236.5 | 236.5 | 237.5 | ▼ en contra | -1.00 | — | 34 | ✅ W | +0.89 |
| 2026-10-21 | MIN @ MIA | ML | MIN ML | 48.3% | 47.4% | ▼ en contra | -0.87 | — | 28 | ✅ W | +0.98 |
| 2026-10-21 | MIN @ MIA | Spread | MIN +1.5 | +1.5 | +1.5 | = sin mov. | -0.00 | — | 67 | ✅ W | +0.89 |
| 2026-10-21 | MIN @ MIA | Total | Under 242.5 | 242.5 | 240.5 | ▲ a favor | +2.00 | — | 45 | ✅ W | +0.93 |
| 2026-10-21 | CHA @ BKN | ML | CHA ML | 51.1% | 52.2% | ▲ a favor | +1.09 | RLM | 64 | ✅ W | +0.87 |
| 2026-10-21 | CHA @ BKN | Spread | CHA -1.5 | -1.5 | -1.5 | = sin mov. | -0.00 | INFO | 29 | ✅ W | +0.98 |
| 2026-10-21 | CHA @ BKN | Total | Over 220.5 | 220.5 | 220.5 | = sin mov. | +0.00 | RLM | 73 | ❌ L | -1.00 |
| 2026-10-21 | ATL @ ORL | ML | ATL ML | 43.7% | 44.9% | ▲ a favor | +1.21 | — | 23 | ✅ W | +1.20 |
| 2026-10-21 | ATL @ ORL | Spread | ATL +2.5 | +2.5 | +2.5 | = sin mov. | -0.00 | — | 54 | ✅ W | +0.95 |
| 2026-10-21 | ATL @ ORL | Total | Under 235.5 | 235.5 | 233.5 | ▲ a favor | +2.00 | — | 38 | ❌ L | -1.00 |
| 2026-10-21 | MIL @ WSH | ML | MIL ML | 36.3% | 39.1% | ▲ a favor | +2.77 | RLM | 11 | ❌ L | -1.00 |
| 2026-10-21 | MIL @ WSH | Spread | MIL +5.5 | +5.5 | +4.5 | ▲ a favor | +1.00 | — | 52 | ❌ L | -1.00 |
| 2026-10-21 | MIL @ WSH | Total | Over 238.5 | 238.5 | 237.5 | ▼ en contra | -1.00 | — | 51 | ✅ W | +0.95 |
| 2026-10-20 | OKC @ SA | ML | SA ML | 56.3% | 48.3% | ▼ en contra | -8.09 | GRADUAL,RLM | 75 | ❌ L | -1.00 |
| 2026-10-20 | OKC @ SA | Spread | SA -2.5 | -2.5 | +1.5 | ▼ en contra | -4.00 | RLM | 66 | ❌ L | -1.00 |
| 2026-10-20 | OKC @ SA | Total | Under 231.5 | 231.5 | 229.5 | ▲ a favor | +2.00 | RLM | 36 | ✅ W | +0.93 |
| 2026-10-20 | PHI @ NY | ML | NY ML | 63.1% | 60.9% | ▼ en contra | -2.17 | RLM | 76 | ❌ L | -1.00 |
| 2026-10-20 | PHI @ NY | Spread | NY -4.5 | -4.5 | -4.5 | = sin mov. | +0.00 | — | 31 | ❌ L | -1.00 |
| 2026-10-20 | PHI @ NY | Total | Under 231.5 | 231.5 | 231.5 | = sin mov. | -0.00 | — | 35 | ✅ W | +0.91 |
| 2026-10-20 | BOS @ DET | ML | BOS ML | 50.4% | 52.2% | ▲ a favor | +1.74 | RLM | 33 | ❌ L | -1.00 |
| 2026-10-20 | BOS @ DET | Spread | DET +1.5 | +1.5 | +1.5 | = sin mov. | +0.00 | INFO | 52 | ✅ W | +0.85 |
| 2026-10-20 | BOS @ DET | Total | Over 222.5 | 222.5 | 221.5 | ▼ en contra | -1.00 | RLM | 67 | ✅ W | +0.95 |
