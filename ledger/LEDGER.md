# Ledger de picks del modelo
_Actualizado: 2026-11-08 05:30 UTC · un pick por partido y mercado (primer snapshot del modelo, con la línea del NBA Odds Tracker en ese momento)._

Picks del workflow de GitHub *Ejecutar modelo* (líneas de ESPN): [github/LEDGER.md](github/LEDGER.md)

**Mercado vs modelo:** ▲ *a favor* = la línea de cierre se movió hacia el número del modelo (CLV positivo); ▼ *en contra* = se alejó; umbral 0.25 pts en spread/total y 0.5 pp de probabilidad en ML. CLV en puntos (spread/total) o en pp de probabilidad sin vig (ML). Spread y total se califican contra la línea del pick a −110; ML al precio del pick.

## Récord

| Grupo | Valor | Picks | Calificados | Récord | WR | Unidades | ROI | CLV medio |
|---|---|---|---|---|---|---|---|---|
| GENERAL | todos | 423 | 399 | 196-203-0 | 49.1% | -25.38 | -6.4% | +0.225 |
| mercado | ml | 141 | 133 | 52-81-0 | 39.1% | -34.47 | -25.9% | +0.003 |
| mercado | spread | 141 | 133 | 67-66-0 | 50.4% | -4.97 | -3.7% | +0.106 |
| mercado | total | 141 | 133 | 77-56-0 | 57.9% | +14.06 | +10.6% | +0.567 |
| movimiento | a favor | 157 | 156 | 86-70-0 | 55.1% | +8.79 | +5.6% | +1.426 |
| movimiento | en contra | 120 | 116 | 51-65-0 | 44.0% | -19.16 | -16.5% | -1.070 |
| movimiento | sin movimiento | 146 | 127 | 59-68-0 | 46.5% | -15.01 | -11.8% | +0.000 |
| mercado × movimiento | ml · a favor | 57 | 57 | 27-30-0 | 47.4% | -4.59 | -8.1% | +0.032 |
| mercado × movimiento | ml · en contra | 48 | 45 | 17-28-0 | 37.8% | -13.35 | -29.7% | -0.030 |
| mercado × movimiento | ml · sin movimiento | 36 | 31 | 8-23-0 | 25.8% | -16.52 | -53.3% | +0.000 |
| mercado × movimiento | spread · a favor | 42 | 42 | 23-19-0 | 54.8% | +1.84 | +4.4% | +1.643 |
| mercado × movimiento | spread · en contra | 31 | 31 | 13-18-0 | 41.9% | -6.07 | -19.6% | -1.742 |
| mercado × movimiento | spread · sin movimiento | 68 | 60 | 31-29-0 | 51.7% | -0.75 | -1.2% | +0.000 |
| mercado × movimiento | total · a favor | 58 | 57 | 36-21-0 | 63.2% | +11.54 | +20.2% | +2.638 |
| mercado × movimiento | total · en contra | 41 | 40 | 21-19-0 | 52.5% | +0.26 | +0.6% | -1.780 |
| mercado × movimiento | total · sin movimiento | 42 | 36 | 20-16-0 | 55.6% | +2.26 | +6.3% | +0.000 |

## CLV y movimiento del mercado hacia el modelo

_% hacia el modelo = picks en que la línea se movió a favor ÷ picks con movimiento (sin contar "sin movimiento"); 50% es lo esperado por azar y `p (azar)` es la probabilidad de ver ese % o más si la línea se moviera al azar. CLV medio por pick con cierre conocido, con su intervalo de confianza del 95%: si el intervalo no incluye 0, el CLV es distinguible del azar._

| Mercado | Con cierre | ▲ a favor | ▼ en contra | % hacia el modelo | p (azar) | CLV medio | IC 95% |
|---|---|---|---|---|---|---|---|
| Spread | 141 | 42 | 31 | 57.5% | 0.121 | +0.11 pts | [-0.14, +0.35] |
| Total | 141 | 58 | 41 | 58.6% | 0.054 | +0.57 pts | [+0.20, +0.94] |
| ML | 141 | 57 | 48 | 54.3% | 0.218 | +0.26 pp | [-0.35, +0.87] |
| **Todos** | 423 | 157 | 120 | 56.7% | 0.015 | — | — |

## Picks

| Fecha | Partido | Mercado | Pick | Línea pick | Cierre | Mercado vs modelo | CLV | Alertas | % público en pick | Resultado | Unidades |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-11-08 | MIA @ SAC | ML | SAC ML | 26.8% | 25.9% | ▼ en contra | -0.93 | — | 5 | pendiente | — |
| 2026-11-08 | MIA @ SAC | Spread | SAC +8.5 | +8.5 | +8.5 | = sin mov. | +0.00 | — | 25 | pendiente | — |
| 2026-11-08 | MIA @ SAC | Total | Under 238.5 | 238.5 | 238.5 | = sin mov. | -0.00 | — | 54 | pendiente | — |
| 2026-11-08 | NO @ LAC | ML | LAC ML | 47.8% | 47.8% | = sin mov. | +0.00 | — | 37 | pendiente | — |
| 2026-11-08 | NO @ LAC | Spread | LAC +1.5 | +1.5 | +1.5 | = sin mov. | +0.00 | — | 33 | pendiente | — |
| 2026-11-08 | NO @ LAC | Total | Under 229.5 | 229.5 | 229.5 | = sin mov. | -0.00 | — | 42 | pendiente | — |
| 2026-11-08 | BOS @ MIL | ML | MIL ML | 16.8% | 16.8% | = sin mov. | +0.02 | — | 4 | pendiente | — |
| 2026-11-08 | BOS @ MIL | Spread | BOS -12.5 | -12.5 | -12.5 | = sin mov. | -0.00 | — | 78 | pendiente | — |
| 2026-11-08 | BOS @ MIL | Total | Over 222.5 | 222.5 | 222.5 | = sin mov. | +0.00 | — | 75 | pendiente | — |
| 2026-11-08 | BKN @ DAL | ML | BKN ML | 26.5% | 25.2% | ▼ en contra | -1.30 | — | 9 | pendiente | — |
| 2026-11-08 | BKN @ DAL | Spread | BKN +8.5 | +8.5 | +8.5 | = sin mov. | -0.00 | — | — | pendiente | — |
| 2026-11-08 | BKN @ DAL | Total | Under 219.5 | 219.5 | 219.5 | = sin mov. | -0.00 | RLM | — | pendiente | — |
| 2026-11-08 | UTAH @ MIN | ML | MIN ML | 81.7% | 81.7% | = sin mov. | +0.00 | — | 95 | pendiente | — |
| 2026-11-08 | UTAH @ MIN | Spread | MIN -11.5 | -11.5 | -11.5 | = sin mov. | +0.00 | — | 76 | pendiente | — |
| 2026-11-08 | UTAH @ MIN | Total | Under 222.5 | 222.5 | 223.5 | ▼ en contra | -1.00 | — | 38 | pendiente | — |
| 2026-11-08 | LAL @ DET | ML | LAL ML | 37.7% | 37.7% | = sin mov. | -0.00 | — | 55 | pendiente | — |
| 2026-11-08 | LAL @ DET | Spread | LAL +4.5 | +4.5 | +4.5 | = sin mov. | -0.00 | — | 58 | pendiente | — |
| 2026-11-08 | LAL @ DET | Total | Under 222.5 | 222.5 | 222.5 | = sin mov. | -0.00 | — | 15 | pendiente | — |
| 2026-11-08 | PHI @ CHI | ML | CHI ML | 25.0% | 24.4% | ▼ en contra | -0.56 | — | 4 | pendiente | — |
| 2026-11-08 | PHI @ CHI | Spread | CHI +8.5 | +8.5 | +8.5 | = sin mov. | +0.00 | — | 10 | pendiente | — |
| 2026-11-08 | PHI @ CHI | Total | Under 238.5 | 238.5 | 238.5 | = sin mov. | -0.00 | — | 55 | pendiente | — |
| 2026-11-07 | SA @ POR | ML | POR ML | 34.3% | 34.3% | = sin mov. | +0.00 | — | 10 | pendiente | — |
| 2026-11-07 | SA @ POR | Spread | SA -5.5 | -5.5 | -5.5 | = sin mov. | -0.00 | STEAM | 69 | pendiente | — |
| 2026-11-07 | SA @ POR | Total | Over 226.5 | 226.5 | 228.5 | ▲ a favor | +2.00 | INFO,RLM | 81 | pendiente | — |
| 2026-11-07 | HOU @ PHX | ML | PHX ML | 29.0% | 30.3% | ▲ a favor | +1.31 | — | 6 | ✅ W | +2.31 |
| 2026-11-07 | HOU @ PHX | Spread | PHX +6.5 | +6.5 | +6.5 | = sin mov. | +0.00 | — | 18 | ✅ W | +0.95 |
| 2026-11-07 | HOU @ PHX | Total | Over 224.5 | 224.5 | 223.5 | ▼ en contra | -1.00 | — | 83 | ❌ L | -1.00 |
| 2026-11-07 | ORL @ GS | ML | ORL ML | 34.3% | 27.4% | ▼ en contra | -6.84 | STEAM | 4 | ❌ L | -1.00 |
| 2026-11-07 | ORL @ GS | Spread | ORL +5.5 | +5.5 | +7.5 | ▼ en contra | -2.00 | INFO,STEAM | 12 | ❌ L | -1.00 |
| 2026-11-07 | ORL @ GS | Total | Over 222.5 | 222.5 | 220.5 | ▼ en contra | -2.00 | STEAM | 83 | ✅ W | +0.91 |
| 2026-11-07 | NY @ CLE | ML | CLE ML | 36.9% | 36.3% | ▼ en contra | -0.60 | — | 26 | ❌ L | -1.00 |
| 2026-11-07 | NY @ CLE | Spread | CLE +4.5 | +4.5 | +4.5 | = sin mov. | +0.00 | INFO,STEAM | 46 | ❌ L | -1.00 |
| 2026-11-07 | NY @ CLE | Total | Over 224.5 | 224.5 | 222.5 | ▼ en contra | -2.00 | INFO,RLM,STEAM | 78 | ❌ L | -1.00 |
| 2026-11-07 | WSH @ OKC | ML | OKC ML | 81.2% | 82.8% | ▲ a favor | +1.58 | GRADUAL | 96 | ✅ W | +0.18 |
| 2026-11-07 | WSH @ OKC | Spread | OKC -11.5 | -11.5 | -12.5 | ▲ a favor | +1.00 | INFO,STEAM | 78 | ✅ W | +0.87 |
| 2026-11-07 | WSH @ OKC | Total | Over 222.5 | 222.5 | 223.5 | ▲ a favor | +1.00 | — | 83 | ❌ L | -1.00 |
| 2026-11-07 | BKN @ ATL | ML | ATL ML | 70.1% | 69.7% | = sin mov. | -0.35 | INFO | 94 | ✅ W | +0.37 |
| 2026-11-07 | BKN @ ATL | Spread | ATL -6.5 | -6.5 | -6.5 | = sin mov. | +0.00 | INFO,STEAM | 76 | ❌ L | -1.00 |
| 2026-11-07 | BKN @ ATL | Total | Under 226.5 | 226.5 | 226.5 | = sin mov. | -0.00 | STEAM | 27 | ❌ L | -1.00 |
| 2026-11-07 | DEN @ IND | ML | DEN ML | 70.0% | 73.4% | ▲ a favor | +3.42 | — | 94 | ✅ W | +0.37 |
| 2026-11-07 | DEN @ IND | Spread | DEN -7.5 | -7.5 | -8.5 | ▲ a favor | +1.00 | STEAM | 81 | ✅ W | +0.94 |
| 2026-11-07 | DEN @ IND | Total | Over 229.5 | 229.5 | 229.5 | = sin mov. | +0.00 | — | 75 | ❌ L | -1.00 |
| 2026-11-06 | POR @ LAL | ML | POR ML | 41.7% | 41.8% | = sin mov. | +0.06 | RLM | 17 | ❌ L | -1.00 |
| 2026-11-06 | POR @ LAL | Spread | POR +3.5 | +3.5 | +3.5 | = sin mov. | -0.00 | RLM,STEAM | 30 | ❌ L | -1.00 |
| 2026-11-06 | POR @ LAL | Total | Under 238.5 | 238.5 | 231.5 | ▲ a favor | +7.00 | RLM | 15 | ❌ L | -1.00 |
| 2026-11-06 | SA @ SAC | ML | SAC ML | 13.5% | 10.6% | ▼ en contra | -2.97 | — | 4 | ❌ L | -1.00 |
| 2026-11-06 | SA @ SAC | Spread | SA -15.5 | -15.5 | -17.5 | ▲ a favor | +2.00 | RLM,STEAM | 73 | ❌ L | -1.00 |
| 2026-11-06 | SA @ SAC | Total | Over 228.5 | 228.5 | 231.5 | ▲ a favor | +3.00 | STEAM | 68 | ✅ W | +0.91 |
| 2026-11-06 | MIN @ NO | ML | NO ML | 37.3% | 40.0% | ▲ a favor | +2.69 | RLM | 14 | ❌ L | -1.00 |
| 2026-11-06 | MIN @ NO | Spread | NO +5.5 | +5.5 | +3.5 | ▲ a favor | +2.00 | RLM,STEAM | 32 | ❌ L | -1.00 |
| 2026-11-06 | MIN @ NO | Total | Under 229.5 | 229.5 | 230.5 | ▼ en contra | -1.00 | — | 28 | ✅ W | +0.87 |
| 2026-11-06 | OKC @ MEM | ML | OKC ML | 61.7% | 61.0% | ▼ en contra | -0.77 | — | 86 | ✅ W | +0.56 |
| 2026-11-06 | OKC @ MEM | Spread | OKC -4.5 | -4.5 | -3.5 | ▼ en contra | -1.00 | STEAM | 74 | ✅ W | +0.96 |
| 2026-11-06 | OKC @ MEM | Total | Over 224.5 | 224.5 | 224.5 | = sin mov. | +0.00 | — | 79 | ✅ W | +0.95 |
| 2026-11-06 | TOR @ MIL | ML | TOR ML | 66.6% | 59.3% | ▼ en contra | -7.21 | INFO,RLM,STEAM | 88 | ✅ W | +0.44 |
| 2026-11-06 | TOR @ MIL | Spread | TOR -6.5 | -6.5 | -3.5 | ▼ en contra | -3.00 | INFO,RLM,STEAM | 66 | ✅ W | +0.86 |
| 2026-11-06 | TOR @ MIL | Total | Under 231.5 | 231.5 | 228.5 | ▲ a favor | +3.00 | INFO,RLM | 38 | ✅ W | +0.91 |
| 2026-11-06 | UTAH @ DAL | ML | UTAH ML | 30.9% | 30.9% | = sin mov. | -0.00 | — | 5 | ❌ L | -1.00 |
| 2026-11-06 | UTAH @ DAL | Spread | DAL -6.5 | -6.5 | -6.5 | = sin mov. | +0.00 | — | 85 | ✅ W | +0.89 |
| 2026-11-06 | UTAH @ DAL | Total | Under 225.5 | 225.5 | 226.5 | ▼ en contra | -1.00 | — | 22 | ✅ W | +0.91 |
| 2026-11-06 | PHI @ CLE | ML | CLE ML | 52.2% | 42.1% | ▼ en contra | -10.07 | GRADUAL | 13 | ✅ W | +0.83 |
| 2026-11-06 | PHI @ CLE | Spread | CLE -1.5 | -1.5 | +2.5 | ▼ en contra | -4.00 | STEAM | 16 | ✅ W | +0.91 |
| 2026-11-06 | PHI @ CLE | Total | Under 234.5 | 234.5 | 232.5 | ▲ a favor | +2.00 | RLM,STEAM | 37 | ✅ W | +0.87 |
| 2026-11-06 | BOS @ CHA | ML | CHA ML | 22.3% | 22.3% | = sin mov. | +0.00 | — | 4 | ❌ L | -1.00 |
| 2026-11-06 | BOS @ CHA | Spread | CHA +10.5 | +10.5 | +10.5 | = sin mov. | +0.00 | — | 19 | ❌ L | -1.00 |
| 2026-11-06 | BOS @ CHA | Total | Over 207.5 | 207.5 | 209.5 | ▲ a favor | +2.00 | STEAM | 85 | ❌ L | -1.00 |
| 2026-11-06 | WSH @ ATL | ML | ATL ML | 72.6% | 72.6% | = sin mov. | +0.00 | — | 82 | ✅ W | +0.32 |
| 2026-11-06 | WSH @ ATL | Spread | ATL -8.5 | -8.5 | -8.5 | = sin mov. | +0.00 | — | 49 | ❌ L | -1.00 |
| 2026-11-06 | WSH @ ATL | Total | Under 227.5 | 227.5 | 227.5 | = sin mov. | -0.00 | — | 34 | ❌ L | -1.00 |
| 2026-11-05 | MIA @ GS | ML | MIA ML | 40.7% | 40.0% | ▼ en contra | -0.74 | — | 22 | ❌ L | -1.00 |
| 2026-11-05 | MIA @ GS | Spread | MIA +3.5 | +3.5 | +3.5 | = sin mov. | -0.00 | — | 49 | ❌ L | -1.00 |
| 2026-11-05 | MIA @ GS | Total | Over 235.5 | 235.5 | 236.5 | ▲ a favor | +1.00 | — | 72 | ❌ L | -1.00 |
| 2026-11-05 | ORL @ PHX | ML | PHX ML | 51.8% | 52.5% | ▲ a favor | +0.76 | RLM | 68 | ✅ W | +0.85 |
| 2026-11-05 | ORL @ PHX | Spread | PHX -1.5 | -1.5 | -1.5 | = sin mov. | +0.00 | — | 65 | ✅ W | +0.98 |
| 2026-11-05 | ORL @ PHX | Total | Over 222.5 | 222.5 | 222.5 | = sin mov. | +0.00 | — | 77 | ❌ L | -1.00 |
| 2026-11-04 | MIA @ LAC | ML | LAC ML | 34.3% | 34.3% | = sin mov. | +0.00 | — | 8 | ❌ L | -1.00 |
| 2026-11-04 | MIA @ LAC | Spread | LAC +5.5 | +5.5 | +5.5 | = sin mov. | +0.00 | STEAM | 38 | ✅ W | +0.95 |
| 2026-11-04 | MIA @ LAC | Total | Over 233.5 | 233.5 | 233.5 | = sin mov. | +0.00 | — | 79 | ❌ L | -1.00 |
| 2026-11-04 | LAL @ SAC | ML | SAC ML | 17.9% | 16.8% | ▼ en contra | -1.06 | RLM | 3 | ❌ L | -1.00 |
| 2026-11-04 | LAL @ SAC | Spread | LAL -11.5 | -11.5 | -12.5 | ▲ a favor | +1.00 | STEAM | 66 | ✅ W | +0.92 |
| 2026-11-04 | LAL @ SAC | Total | Under 238.5 | 238.5 | 233.5 | ▲ a favor | +5.00 | RLM,STEAM | 18 | ✅ W | +0.87 |
| 2026-11-04 | DAL @ SA | ML | SA ML | 80.8% | 82.8% | ▲ a favor | +1.95 | RLM | 93 | ✅ W | +0.19 |
| 2026-11-04 | DAL @ SA | Spread | SA -11.5 | -11.5 | -12.5 | ▲ a favor | +1.00 | STEAM | 42 | ❌ L | -1.00 |
| 2026-11-04 | DAL @ SA | Total | Under 227.5 | 227.5 | 226.5 | ▲ a favor | +1.00 | RLM | 14 | ✅ W | +0.91 |
| 2026-11-04 | POR @ PHX | ML | PHX ML | 42.8% | 42.8% | = sin mov. | +0.00 | — | 15 | ❌ L | -1.00 |
| 2026-11-04 | POR @ PHX | Spread | PHX +3.5 | +3.5 | +2.5 | ▲ a favor | +1.00 | STEAM | 43 | ❌ L | -1.00 |
| 2026-11-04 | POR @ PHX | Total | Under 227.5 | 227.5 | 227.5 | = sin mov. | -0.00 | RLM | 14 | ❌ L | -1.00 |
| 2026-11-04 | TOR @ DEN | ML | TOR ML | 35.6% | 35.7% | = sin mov. | +0.12 | RLM | 11 | ❌ L | -1.00 |
| 2026-11-04 | TOR @ DEN | Spread | TOR +4.5 | +4.5 | +4.5 | = sin mov. | -0.00 | — | 45 | ❌ L | -1.00 |
| 2026-11-04 | TOR @ DEN | Total | Over 231.5 | 231.5 | 231.5 | = sin mov. | +0.00 | RLM | 81 | ✅ W | +0.91 |
| 2026-11-04 | MIN @ HOU | ML | MIN ML | 28.2% | 29.4% | ▲ a favor | +1.21 | RLM | 10 | ✅ W | +2.41 |
| 2026-11-04 | MIN @ HOU | Spread | MIN +8.5 | +8.5 | +7.5 | ▲ a favor | +1.00 | RLM,STEAM | 49 | ✅ W | +0.86 |
| 2026-11-04 | MIN @ HOU | Total | Over 219.5 | 219.5 | 219.5 | = sin mov. | +0.00 | RLM,STEAM | 87 | ✅ W | +0.87 |
| 2026-11-04 | CLE @ OKC | ML | OKC ML | 52.3% | 59.3% | ▲ a favor | +6.98 | STEAM | 70 | ✅ W | +0.83 |
| 2026-11-04 | CLE @ OKC | Spread | OKC -1.5 | -1.5 | -3.5 | ▲ a favor | +2.00 | RLM,STEAM | 39 | ✅ W | +0.87 |
| 2026-11-04 | CLE @ OKC | Total | Under 227.5 | 227.5 | 226.5 | ▲ a favor | +1.00 | RLM | 15 | ❌ L | -1.00 |
| 2026-11-04 | CHA @ BKN | ML | BKN ML | 42.9% | 39.5% | ▼ en contra | -3.34 | GRADUAL | 21 | ✅ W | +1.24 |
| 2026-11-04 | CHA @ BKN | Spread | BKN +3.5 | +3.5 | +3.5 | = sin mov. | +0.00 | STEAM | 49 | ✅ W | +0.88 |
| 2026-11-04 | CHA @ BKN | Total | Under 212.5 | 212.5 | 213.5 | ▼ en contra | -1.00 | RLM,STEAM | 20 | ❌ L | -1.00 |
| 2026-11-04 | CHI @ NY | ML | NY ML | 82.3% | 81.8% | ▼ en contra | -0.54 | — | 96 | ✅ W | +0.17 |
| 2026-11-04 | CHI @ NY | Spread | NY -12.5 | -12.5 | -11.5 | ▼ en contra | -1.00 | RLM,STEAM | 61 | ✅ W | +0.91 |
| 2026-11-04 | CHI @ NY | Total | Under 232.5 | 232.5 | 233.5 | ▼ en contra | -1.00 | — | 30 | ❌ L | -1.00 |
| 2026-11-04 | MIL @ BOS | ML | MIL ML | 19.6% | 18.3% | ▼ en contra | -1.23 | RLM | 4 | ❌ L | -1.00 |
| 2026-11-04 | MIL @ BOS | Spread | BOS -11.5 | -11.5 | -12.5 | ▲ a favor | +1.00 | INFO,RLM,STEAM | 62 | ❌ L | -1.00 |
| 2026-11-04 | MIL @ BOS | Total | Over 223.5 | 223.5 | 222.5 | ▼ en contra | -1.00 | GRADUAL,RLM,STEAM | 80 | ❌ L | -1.00 |
| 2026-11-04 | ATL @ WSH | ML | ATL ML | 52.9% | 53.2% | = sin mov. | +0.21 | INFO,STEAM | 54 | ✅ W | +0.81 |
| 2026-11-04 | ATL @ WSH | Spread | ATL -1.5 | -1.5 | -1.5 | = sin mov. | -0.00 | INFO,RLM,STEAM | 33 | ✅ W | +0.88 |
| 2026-11-04 | ATL @ WSH | Total | Under 233.5 | 233.5 | 229.5 | ▲ a favor | +4.00 | GRADUAL,INFO,RLM | 38 | ✅ W | +0.91 |
| 2026-11-04 | PHI @ DET | ML | DET ML | 53.2% | 55.3% | ▲ a favor | +2.09 | GRADUAL,RLM | 35 | ❌ L | -1.00 |
| 2026-11-04 | PHI @ DET | Spread | DET -2.5 | -2.5 | -2.5 | = sin mov. | +0.00 | — | 23 | ❌ L | -1.00 |
| 2026-11-04 | PHI @ DET | Total | Under 217.5 | 217.5 | 219.5 | ▼ en contra | -2.00 | — | 22 | ❌ L | -1.00 |
| 2026-11-02 | MIA @ LAL | ML | LAL ML | 55.1% | 54.3% | ▼ en contra | -0.87 | GRADUAL | 70 | ✅ W | +0.74 |
| 2026-11-02 | MIA @ LAL | Spread | LAL -2.5 | -2.5 | -1.5 | ▼ en contra | -1.00 | RLM,STEAM | 42 | ✅ W | +0.93 |
| 2026-11-02 | MIA @ LAL | Total | Over 236.5 | 236.5 | 238.5 | ▲ a favor | +2.00 | — | 88 | ✅ W | +0.91 |
| 2026-11-02 | PHX @ GS | ML | PHX ML | 43.7% | 44.7% | ▲ a favor | +1.01 | RLM | 13 | ❌ L | -1.00 |
| 2026-11-02 | PHX @ GS | Spread | PHX +2.5 | +2.5 | +2.5 | = sin mov. | -0.00 | — | 42 | ❌ L | -1.00 |
| 2026-11-02 | PHX @ GS | Total | Over 227.5 | 227.5 | 227.5 | = sin mov. | +0.00 | — | 92 | ✅ W | +0.94 |
| 2026-11-02 | TOR @ LAC | ML | TOR ML | 61.7% | 66.8% | ▲ a favor | +5.06 | — | 91 | ✅ W | +0.56 |
| 2026-11-02 | TOR @ LAC | Spread | TOR -4.5 | -4.5 | -6.5 | ▲ a favor | +2.00 | INFO,STEAM | 67 | ✅ W | +0.94 |
| 2026-11-02 | TOR @ LAC | Total | Over 219.5 | 219.5 | 219.5 | = sin mov. | +0.00 | — | 92 | ✅ W | +0.91 |
| 2026-11-02 | POR @ DEN | ML | POR ML | 39.0% | 39.0% | = sin mov. | -0.00 | — | 21 | ✅ W | +1.46 |
| 2026-11-02 | POR @ DEN | Spread | POR +4.5 | +4.5 | +4.5 | = sin mov. | -0.00 | — | 53 | ✅ W | +0.86 |
| 2026-11-02 | POR @ DEN | Total | Under 231.5 | 231.5 | 231.5 | = sin mov. | -0.00 | — | 9 | ✅ W | +0.88 |
| 2026-11-02 | BOS @ HOU | ML | BOS ML | 36.9% | 38.4% | ▲ a favor | +1.46 | — | 31 | ❌ L | -1.00 |
| 2026-11-02 | BOS @ HOU | Spread | BOS +4.5 | +4.5 | +4.5 | = sin mov. | -0.00 | — | 60 | ❌ L | -1.00 |
| 2026-11-02 | BOS @ HOU | Total | Over 215.5 | 215.5 | 215.5 | = sin mov. | +0.00 | — | 94 | ❌ L | -1.00 |
| 2026-11-02 | UTAH @ SA | ML | SA ML | 88.6% | 88.6% | = sin mov. | +0.00 | — | 98 | ✅ W | +0.08 |
| 2026-11-02 | UTAH @ SA | Spread | SA -16.5 | -16.5 | -16.5 | = sin mov. | +0.00 | — | 54 | ✅ W | +0.93 |
| 2026-11-02 | UTAH @ SA | Total | Under 227.5 | 227.5 | 226.5 | ▲ a favor | +1.00 | RLM | 15 | ✅ W | +0.95 |
| 2026-11-02 | MIL @ MIN | ML | MIN ML | 77.7% | 80.0% | ▲ a favor | +2.28 | — | 95 | ✅ W | +0.24 |
| 2026-11-02 | MIL @ MIN | Spread | MIN -10.5 | -10.5 | -11.5 | ▲ a favor | +1.00 | STEAM | 55 | ✅ W | +0.87 |
| 2026-11-02 | MIL @ MIN | Total | Under 230.5 | 230.5 | 233.5 | ▼ en contra | -3.00 | RLM,STEAM | 17 | ✅ W | +0.93 |
| 2026-11-02 | NO @ MEM | ML | NO ML | 35.7% | 34.5% | ▼ en contra | -1.14 | RLM | 10 | ✅ W | +1.69 |
| 2026-11-02 | NO @ MEM | Spread | NO +5.5 | +5.5 | +5.5 | = sin mov. | -0.00 | — | 38 | ✅ W | +0.95 |
| 2026-11-02 | NO @ MEM | Total | Over 232.5 | 232.5 | 231.5 | ▼ en contra | -1.00 | RLM | 88 | ✅ W | +0.94 |
| 2026-11-02 | SAC @ DAL | ML | SAC ML | 25.6% | 28.2% | ▲ a favor | +2.61 | GRADUAL,RLM | 3 | ✅ W | +2.76 |
| 2026-11-02 | SAC @ DAL | Spread | SAC +8.5 | +8.5 | +7.5 | ▲ a favor | +1.00 | RLM,STEAM | 27 | ✅ W | +0.88 |
| 2026-11-02 | SAC @ DAL | Total | Under 231.5 | 231.5 | 232.5 | ▼ en contra | -1.00 | — | 13 | ✅ W | +0.91 |
| 2026-11-02 | ATL @ IND | ML | IND ML | 22.3% | 21.8% | = sin mov. | -0.46 | — | 14 | ❌ L | -1.00 |
| 2026-11-02 | ATL @ IND | Spread | IND +10.5 | +10.5 | +10.5 | = sin mov. | +0.00 | INFO,STEAM | 39 | ✅ W | +0.88 |
| 2026-11-02 | ATL @ IND | Total | Over 229.5 | 229.5 | 226.5 | ▼ en contra | -3.00 | RLM,STEAM | 85 | ❌ L | -1.00 |
| 2026-11-02 | BKN @ NY | ML | BKN ML | 12.5% | 13.0% | ▲ a favor | +0.51 | — | 4 | ❌ L | -1.00 |
| 2026-11-02 | BKN @ NY | Spread | NY -14.5 | -14.5 | -14.5 | = sin mov. | +0.00 | — | 52 | ❌ L | -1.00 |
| 2026-11-02 | BKN @ NY | Total | Under 218.5 | 218.5 | 218.5 | = sin mov. | -0.00 | RLM | 38 | ✅ W | +0.93 |
| 2026-11-02 | CHI @ PHI | ML | CHI ML | 19.4% | 19.5% | = sin mov. | +0.08 | RLM | 3 | ❌ L | -1.00 |
| 2026-11-02 | CHI @ PHI | Spread | PHI -9.5 | -9.5 | -10.5 | ▲ a favor | +1.00 | STEAM | 70 | ✅ W | +0.88 |
| 2026-11-02 | CHI @ PHI | Total | Under 238.5 | 238.5 | 240.5 | ▼ en contra | -2.00 | — | 27 | ✅ W | +0.93 |
| 2026-11-02 | DET @ CHA | ML | CHA ML | 33.2% | 33.7% | = sin mov. | +0.49 | — | 7 | ❌ L | -1.00 |
| 2026-11-02 | DET @ CHA | Spread | CHA +5.5 | +5.5 | +5.5 | = sin mov. | +0.00 | STEAM | 15 | ❌ L | -1.00 |
| 2026-11-02 | DET @ CHA | Total | Under 209.5 | 209.5 | 209.5 | = sin mov. | -0.00 | — | 49 | ❌ L | -1.00 |
| 2026-11-02 | WSH @ ORL | ML | ORL ML | 58.4% | 58.2% | = sin mov. | -0.17 | — | 51 | ❌ L | -1.00 |
| 2026-11-02 | WSH @ ORL | Spread | ORL -3.5 | -3.5 | -2.5 | ▼ en contra | -1.00 | STEAM | 29 | ❌ L | -1.00 |
| 2026-11-02 | WSH @ ORL | Total | Under 224.5 | 224.5 | 224.5 | = sin mov. | -0.00 | — | 14 | ✅ W | +0.91 |
| 2026-11-02 | OKC @ CLE | ML | OKC ML | 39.6% | 39.1% | ▼ en contra | -0.55 | — | 21 | ✅ W | +1.42 |
| 2026-11-02 | OKC @ CLE | Spread | OKC +4.5 | +4.5 | +4.5 | = sin mov. | -0.00 | — | 18 | ✅ W | +0.86 |
| 2026-11-02 | OKC @ CLE | Total | Under 229.5 | 229.5 | 229.5 | = sin mov. | -0.00 | — | 13 | ✅ W | +0.91 |
| 2026-11-01 | TOR @ LAL | ML | TOR ML | 42.8% | 39.6% | ▼ en contra | -3.17 | GRADUAL,RLM | 11 | ❌ L | -1.00 |
| 2026-11-01 | TOR @ LAL | Spread | TOR +2.5 | +2.5 | +3.5 | ▼ en contra | -1.00 | RLM,STEAM | 24 | ❌ L | -1.00 |
| 2026-11-01 | TOR @ LAL | Total | Under 225.5 | 225.5 | 223.5 | ▲ a favor | +2.00 | RLM,STEAM | 14 | ❌ L | -1.00 |
| 2026-11-01 | LAC @ GS | ML | GS ML | 55.1% | 54.3% | ▼ en contra | -0.87 | — | 84 | ✅ W | +0.74 |
| 2026-11-01 | LAC @ GS | Spread | GS -2.5 | -2.5 | -2.5 | = sin mov. | +0.00 | STEAM | 70 | ✅ W | +0.95 |
| 2026-11-01 | LAC @ GS | Total | Over 221.5 | 221.5 | 220.5 | ▼ en contra | -1.00 | — | 80 | ✅ W | +0.87 |
| 2026-11-01 | BKN @ IND | ML | IND ML | 60.4% | 58.3% | ▼ en contra | -2.08 | RLM | 86 | ❌ L | -1.00 |
| 2026-11-01 | BKN @ IND | Spread | IND -3.5 | -3.5 | -3.5 | = sin mov. | +0.00 | — | 73 | ❌ L | -1.00 |
| 2026-11-01 | BKN @ IND | Total | Under 231.5 | 231.5 | 230.5 | ▲ a favor | +1.00 | — | 23 | ✅ W | +0.91 |
| 2026-11-01 | BOS @ ORL | ML | ORL ML | 30.9% | 29.0% | ▼ en contra | -1.88 | — | 8 | ❌ L | -1.00 |
| 2026-11-01 | BOS @ ORL | Spread | ORL +6.5 | +6.5 | +6.5 | = sin mov. | +0.00 | INFO,STEAM | 24 | ❌ L | -1.00 |
| 2026-11-01 | BOS @ ORL | Total | Over 220.5 | 220.5 | 221.5 | ▲ a favor | +1.00 | — | 88 | ❌ L | -1.00 |
| 2026-10-31 | OKC @ HOU | ML | OKC ML | 43.7% | 43.7% | = sin mov. | -0.00 | — | 29 | ❌ L | -1.00 |
| 2026-10-31 | OKC @ HOU | Spread | OKC +2.5 | +2.5 | +2.5 | = sin mov. | -0.00 | — | 40 | ❌ L | -1.00 |
| 2026-10-31 | OKC @ HOU | Total | Under 218.5 | 218.5 | 219.5 | ▼ en contra | -1.00 | — | 13 | ✅ W | +0.91 |
| 2026-10-31 | CLE @ MIL | ML | CLE ML | 75.1% | 74.1% | ▼ en contra | -0.99 | — | 94 | ✅ W | +0.28 |
| 2026-10-31 | CLE @ MIL | Spread | CLE -9.5 | -9.5 | -8.5 | ▼ en contra | -1.00 | RLM,STEAM | 68 | ✅ W | +0.95 |
| 2026-10-31 | CLE @ MIL | Total | Under 236.5 | 236.5 | 234.5 | ▲ a favor | +2.00 | RLM,STEAM | 23 | ❌ L | -1.00 |
| 2026-10-31 | MIN @ SA | ML | MIN ML | 19.6% | 18.3% | ▼ en contra | -1.30 | — | 9 | ❌ L | -1.00 |
| 2026-10-31 | MIN @ SA | Spread | MIN +11.5 | +11.5 | +12.5 | ▼ en contra | -1.00 | RLM,STEAM | 48 | ✅ W | +0.95 |
| 2026-10-31 | MIN @ SA | Total | Under 227.5 | 227.5 | 230.5 | ▼ en contra | -3.00 | INFO,RLM,STEAM | 12 | ❌ L | -1.00 |
| 2026-10-31 | SAC @ MEM | ML | SAC ML | 21.8% | 28.2% | ▲ a favor | +6.39 | GRADUAL,RLM,STEAM | 6 | ❌ L | -1.00 |
| 2026-10-31 | SAC @ MEM | Spread | SAC +10.5 | +10.5 | +7.5 | ▲ a favor | +3.00 | INFO,RLM,STEAM | 26 | ❌ L | -1.00 |
| 2026-10-31 | SAC @ MEM | Total | Over 233.5 | 233.5 | 229.5 | ▼ en contra | -4.00 | RLM,STEAM | 86 | ✅ W | +0.91 |
| 2026-10-31 | ATL @ NO | ML | NO ML | 39.6% | 36.3% | ▼ en contra | -3.31 | — | 13 | ✅ W | +1.42 |
| 2026-10-31 | ATL @ NO | Spread | NO +4.5 | +4.5 | +5.5 | ▼ en contra | -1.00 | STEAM | 23 | ✅ W | +0.87 |
| 2026-10-31 | ATL @ NO | Total | Under 239.5 | 239.5 | 239.5 | = sin mov. | -0.00 | STEAM | 39 | ✅ W | +0.95 |
| 2026-10-31 | PHI @ CHA | ML | CHA ML | 47.8% | 45.7% | ▼ en contra | -2.10 | INFO,RLM,STEAM | 13 | ❌ L | -1.00 |
| 2026-10-31 | PHI @ CHA | Spread | CHA +1.5 | +1.5 | +2.5 | ▼ en contra | -1.00 | INFO,RLM,STEAM | 6 | ❌ L | -1.00 |
| 2026-10-31 | PHI @ CHA | Total | Under 216.5 | 216.5 | 212.5 | ▲ a favor | +4.00 | INFO,RLM | 20 | ✅ W | +0.95 |
| 2026-10-31 | POR @ UTAH | ML | POR ML | 66.4% | 69.1% | ▲ a favor | +2.71 | GRADUAL,STEAM | 89 | ✅ W | +0.44 |
| 2026-10-31 | POR @ UTAH | Spread | POR -6.5 | -6.5 | -6.5 | = sin mov. | -0.00 | STEAM | 72 | ✅ W | +0.91 |
| 2026-10-31 | POR @ UTAH | Total | Under 231.5 | 231.5 | 232.5 | ▼ en contra | -1.00 | STEAM | 18 | ✅ W | +0.95 |
| 2026-10-30 | DEN @ PHX | ML | PHX ML | 45.7% | 38.4% | ▼ en contra | -7.37 | — | 10 | ❌ L | -1.00 |
| 2026-10-30 | DEN @ PHX | Spread | PHX +2.5 | +2.5 | +4.5 | ▼ en contra | -2.00 | STEAM | 25 | ❌ L | -1.00 |
| 2026-10-30 | DEN @ PHX | Total | Under 233.5 | 233.5 | 231.5 | ▲ a favor | +2.00 | GRADUAL,RLM | 12 | ❌ L | -1.00 |
| 2026-10-30 | LAL @ GS | ML | LAL ML | 51.1% | 56.3% | ▲ a favor | +5.27 | — | 69 | ❌ L | -1.00 |
| 2026-10-30 | LAL @ GS | Spread | LAL -1.5 | -1.5 | -2.5 | ▲ a favor | +1.00 | STEAM | 56 | ❌ L | -1.00 |
| 2026-10-30 | LAL @ GS | Total | Under 236.5 | 236.5 | 234.5 | ▲ a favor | +2.00 | RLM | 18 | ✅ W | +0.91 |
| 2026-10-30 | HOU @ DAL | ML | HOU ML | 62.2% | 63.7% | ▲ a favor | +1.44 | INFO | 86 | ❌ L | -1.00 |
| 2026-10-30 | HOU @ DAL | Spread | HOU -5.5 | -5.5 | -5.5 | = sin mov. | -0.00 | INFO,STEAM | 58 | ❌ L | -1.00 |
| 2026-10-30 | HOU @ DAL | Total | Over 227.5 | 227.5 | 223.5 | ▼ en contra | -4.00 | GRADUAL,RLM,STEAM | 94 | ❌ L | -1.00 |
| 2026-10-30 | IND @ MIA | ML | MIA ML | 57.2% | 73.4% | ▲ a favor | +16.15 | GRADUAL,STEAM | 89 | ✅ W | +0.68 |
| 2026-10-30 | IND @ MIA | Spread | MIA -3.5 | -3.5 | -8.5 | ▲ a favor | +5.00 | INFO,RLM,STEAM | 46 | ✅ W | +0.91 |
| 2026-10-30 | IND @ MIA | Total | Under 241.5 | 241.5 | 237.5 | ▲ a favor | +4.00 | RLM,STEAM | 14 | ❌ L | -1.00 |
| 2026-10-30 | LAC @ MIN | ML | LAC ML | 25.9% | 30.4% | ▲ a favor | +4.51 | RLM | 7 | ❌ L | -1.00 |
| 2026-10-30 | LAC @ MIN | Spread | LAC +9.5 | +9.5 | +6.5 | ▲ a favor | +3.00 | RLM,STEAM | 46 | ❌ L | -1.00 |
| 2026-10-30 | LAC @ MIN | Total | Under 230.5 | 230.5 | 222.5 | ▲ a favor | +8.00 | RLM | 12 | ✅ W | +0.91 |
| 2026-10-30 | CHI @ BOS | ML | CHI ML | 14.8% | 14.2% | ▼ en contra | -0.55 | RLM | 5 | ❌ L | -1.00 |
| 2026-10-30 | CHI @ BOS | Spread | BOS -15.5 | -15.5 | -14.5 | ▼ en contra | -1.00 | STEAM | 55 | ❌ L | -1.00 |
| 2026-10-30 | CHI @ BOS | Total | Over 230.5 | 230.5 | 236.5 | ▲ a favor | +6.00 | RLM,STEAM | 83 | ✅ W | +0.91 |
| 2026-10-30 | DET @ BKN | ML | BKN ML | 25.2% | 27.4% | ▲ a favor | +2.20 | RLM,STEAM | 6 | ❌ L | -1.00 |
| 2026-10-30 | DET @ BKN | Spread | BKN +8.5 | +8.5 | +8.5 | = sin mov. | +0.00 | STEAM | 30 | ❌ L | -1.00 |
| 2026-10-30 | DET @ BKN | Total | Under 227.5 | 227.5 | 222.5 | ▲ a favor | +5.00 | INFO,RLM | 14 | ✅ W | +0.91 |
| 2026-10-30 | NY @ PHI | ML | NY ML | 50.4% | 58.3% | ▲ a favor | +7.87 | RLM,STEAM | 49 | ❌ L | -1.00 |
| 2026-10-30 | NY @ PHI | Spread | NY -1.5 | -1.5 | -3.5 | ▲ a favor | +2.00 | INFO,RLM,STEAM | 33 | ❌ L | -1.00 |
| 2026-10-30 | NY @ PHI | Total | Under 230.5 | 230.5 | 225.5 | ▲ a favor | +5.00 | GRADUAL,INFO,RLM | 16 | ✅ W | +0.91 |
| 2026-10-30 | ORL @ TOR | ML | TOR ML | 60.9% | 65.7% | ▲ a favor | +4.82 | RLM | 93 | ❌ L | -1.00 |
| 2026-10-30 | ORL @ TOR | Spread | TOR -4.5 | -4.5 | -5.5 | ▲ a favor | +1.00 | RLM,STEAM | 81 | ❌ L | -1.00 |
| 2026-10-30 | ORL @ TOR | Total | Under 222.5 | 222.5 | 227.5 | ▼ en contra | -5.00 | RLM,STEAM | 10 | ❌ L | -1.00 |
| 2026-10-30 | CHA @ WSH | ML | CHA ML | 51.1% | 51.1% | = sin mov. | -0.00 | GRADUAL | 38 | ❌ L | -1.00 |
| 2026-10-30 | CHA @ WSH | Spread | CHA -1.5 | -1.5 | -1.5 | = sin mov. | -0.00 | INFO | 43 | ❌ L | -1.00 |
| 2026-10-30 | CHA @ WSH | Total | Under 223.5 | 223.5 | 218.5 | ▲ a favor | +5.00 | RLM,STEAM | 14 | ✅ W | +0.91 |
| 2026-10-29 | MEM @ POR | ML | POR ML | 71.4% | 71.0% | = sin mov. | -0.40 | — | 89 | ❌ L | -1.00 |
| 2026-10-29 | MEM @ POR | Spread | POR -7.5 | -7.5 | -7.5 | = sin mov. | +0.00 | INFO,STEAM | 64 | ❌ L | -1.00 |
| 2026-10-29 | MEM @ POR | Total | Under 232.5 | 232.5 | 232.5 | = sin mov. | -0.00 | RLM,STEAM | 14 | ✅ W | +0.95 |
| 2026-10-29 | CLE @ ATL | ML | ATL ML | 51.1% | 51.7% | ▲ a favor | +0.65 | RLM | 44 | ✅ W | +0.87 |
| 2026-10-29 | CLE @ ATL | Spread | ATL -1.5 | -1.5 | -1.5 | = sin mov. | +0.00 | — | 45 | ✅ W | +0.95 |
| 2026-10-29 | CLE @ ATL | Total | Under 237.5 | 237.5 | 237.5 | = sin mov. | -0.00 | — | 17 | ✅ W | +0.95 |
| 2026-10-29 | SAC @ NO | ML | SAC ML | 32.5% | 32.5% | = sin mov. | -0.00 | — | 14 | ❌ L | -1.00 |
| 2026-10-29 | SAC @ NO | Spread | NO -5.5 | -5.5 | -6.5 | ▲ a favor | +1.00 | INFO,STEAM | 68 | ✅ W | +0.85 |
| 2026-10-29 | SAC @ NO | Total | Under 236.5 | 236.5 | 234.5 | ▲ a favor | +2.00 | RLM | 30 | ❌ L | -1.00 |
| 2026-10-28 | LAL @ LAC | ML | LAL ML | 64.5% | 49.6% | ▼ en contra | -14.91 | INFO,RLM | 79 | ✅ W | +0.49 |
| 2026-10-28 | LAL @ LAC | Spread | LAL -5.5 | -5.5 | +1.5 | ▼ en contra | -7.00 | INFO,RLM,STEAM | 68 | ✅ W | +0.95 |
| 2026-10-28 | LAL @ LAC | Total | Under 228.5 | 228.5 | 224.5 | ▲ a favor | +4.00 | INFO,RLM | 12 | ✅ W | +0.87 |
| 2026-10-28 | OKC @ DAL | ML | OKC ML | 64.5% | 63.1% | ▼ en contra | -1.38 | RLM | 89 | ❌ L | -1.00 |
| 2026-10-28 | OKC @ DAL | Spread | OKC -5.5 | -5.5 | -5.5 | = sin mov. | -0.00 | STEAM | 61 | ❌ L | -1.00 |
| 2026-10-28 | OKC @ DAL | Total | Under 230.5 | 230.5 | 228.5 | ▲ a favor | +2.00 | RLM | 19 | ✅ W | +0.91 |
| 2026-10-28 | SA @ UTAH | ML | UTAH ML | 18.3% | 15.3% | ▼ en contra | -2.92 | — | 4 | ❌ L | -1.00 |
| 2026-10-28 | SA @ UTAH | Spread | UTAH +12.5 | +12.5 | +13.5 | ▼ en contra | -1.00 | INFO,STEAM | 43 | ✅ W | +0.91 |
| 2026-10-28 | SA @ UTAH | Total | Under 234.5 | 234.5 | 232.5 | ▲ a favor | +2.00 | RLM | 14 | ✅ W | +0.87 |
| 2026-10-28 | DEN @ NO | ML | NO ML | 37.8% | 38.4% | ▲ a favor | +0.60 | RLM | 10 | ❌ L | -1.00 |
| 2026-10-28 | DEN @ NO | Spread | NO +4.5 | +4.5 | +4.5 | = sin mov. | +0.00 | STEAM | 35 | ❌ L | -1.00 |
| 2026-10-28 | DEN @ NO | Total | Under 238.5 | 238.5 | 240.5 | ▼ en contra | -2.00 | — | 19 | ✅ W | +0.95 |
| 2026-10-28 | GS @ MIN | ML | MIN ML | 58.3% | 60.4% | ▲ a favor | +2.08 | RLM | 76 | ❌ L | -1.00 |
| 2026-10-28 | GS @ MIN | Spread | MIN -3.5 | -3.5 | -4.5 | ▲ a favor | +1.00 | RLM,STEAM | 60 | ❌ L | -1.00 |
| 2026-10-28 | GS @ MIN | Total | Over 225.5 | 225.5 | 227.5 | ▲ a favor | +2.00 | INFO | 91 | ✅ W | +0.91 |
| 2026-10-28 | HOU @ MIL | ML | HOU ML | 72.6% | 74.1% | ▲ a favor | +1.51 | — | 94 | ✅ W | +0.32 |
| 2026-10-28 | HOU @ MIL | Spread | HOU -8.5 | -8.5 | -8.5 | = sin mov. | -0.00 | — | 71 | ✅ W | +0.91 |
| 2026-10-28 | HOU @ MIL | Total | Over 227.5 | 227.5 | 226.5 | ▼ en contra | -1.00 | RLM,STEAM | 91 | ✅ W | +0.87 |
| 2026-10-28 | NY @ CHI | ML | NY ML | 70.0% | 70.5% | = sin mov. | +0.49 | — | 92 | ✅ W | +0.37 |
| 2026-10-28 | NY @ CHI | Spread | NY -7.5 | -7.5 | -6.5 | ▼ en contra | -1.00 | INFO,RLM,STEAM | 74 | ❌ L | -1.00 |
| 2026-10-28 | NY @ CHI | Total | Under 234.5 | 234.5 | 232.5 | ▲ a favor | +2.00 | RLM,STEAM | 19 | ❌ L | -1.00 |
| 2026-10-28 | ORL @ TOR | ML | TOR ML | 60.9% | 63.1% | ▲ a favor | +2.17 | — | 86 | ✅ W | +0.57 |
| 2026-10-28 | ORL @ TOR | Spread | TOR -4.5 | -4.5 | -5.5 | ▲ a favor | +1.00 | STEAM | 72 | ✅ W | +0.91 |
| 2026-10-28 | ORL @ TOR | Total | Under 223.5 | 223.5 | 224.5 | ▼ en contra | -1.00 | RLM,STEAM | 16 | ❌ L | -1.00 |
| 2026-10-28 | CHA @ DET | ML | CHA ML | 28.6% | 28.6% | = sin mov. | -0.00 | RLM | 7 | ❌ L | -1.00 |
| 2026-10-28 | CHA @ DET | Spread | CHA +7.5 | +7.5 | +7.5 | = sin mov. | -0.00 | RLM,STEAM | 42 | ❌ L | -1.00 |
| 2026-10-28 | CHA @ DET | Total | Under 216.5 | 216.5 | 212.5 | ▲ a favor | +4.00 | RLM,STEAM | 13 | ✅ W | +0.87 |
| 2026-10-28 | MIA @ ATL | ML | ATL ML | 59.3% | 56.3% | ▼ en contra | -2.99 | GRADUAL,RLM | 62 | ❌ L | -1.00 |
| 2026-10-28 | MIA @ ATL | Spread | ATL -3.5 | -3.5 | -2.5 | ▼ en contra | -1.00 | STEAM | 46 | ❌ L | -1.00 |
| 2026-10-28 | MIA @ ATL | Total | Under 239.5 | 239.5 | 243.5 | ▼ en contra | -4.00 | GRADUAL | 24 | ❌ L | -1.00 |
| 2026-10-28 | PHI @ IND | ML | IND ML | 40.0% | 29.5% | ▼ en contra | -10.54 | GRADUAL,INFO | 10 | ❌ L | -1.00 |
| 2026-10-28 | PHI @ IND | Spread | IND +4.5 | +4.5 | +7.5 | ▼ en contra | -3.00 | INFO,STEAM | 31 | ❌ L | -1.00 |
| 2026-10-28 | PHI @ IND | Total | Under 237.5 | 237.5 | 234.5 | ▲ a favor | +3.00 | INFO,RLM | 23 | ✅ W | +0.91 |
| 2026-10-28 | WSH @ CLE | ML | WSH ML | 23.4% | 23.4% | = sin mov. | -0.00 | — | 7 | ❌ L | -1.00 |
| 2026-10-28 | WSH @ CLE | Spread | CLE -10.5 | -10.5 | -9.5 | ▼ en contra | -1.00 | STEAM | 64 | ❌ L | -1.00 |
| 2026-10-28 | WSH @ CLE | Total | Under 239.5 | 239.5 | 240.5 | ▼ en contra | -1.00 | — | 20 | ✅ W | +0.91 |
| 2026-10-27 | POR @ LAL | ML | LAL ML | 53.2% | 51.1% | ▼ en contra | -2.16 | RLM | 77 | ❌ L | -1.00 |
| 2026-10-27 | POR @ LAL | Spread | LAL -1.5 | -1.5 | -1.5 | = sin mov. | +0.00 | — | 63 | ❌ L | -1.00 |
| 2026-10-27 | POR @ LAL | Total | Under 233.5 | 233.5 | 234.5 | ▼ en contra | -1.00 | RLM | 14 | ❌ L | -1.00 |
| 2026-10-26 | GS @ DEN | ML | GS ML | 28.6% | 30.0% | ▲ a favor | +1.34 | — | 9 | ✅ W | +2.35 |
| 2026-10-26 | GS @ DEN | Spread | GS +7.5 | +7.5 | +7.5 | = sin mov. | -0.00 | STEAM | 43 | ✅ W | +0.91 |
| 2026-10-26 | GS @ DEN | Total | Under 235.5 | 235.5 | 236.5 | ▼ en contra | -1.00 | RLM,STEAM | 19 | ❌ L | -1.00 |
| 2026-10-26 | MEM @ UTAH | ML | UTAH ML | 49.6% | 49.6% | = sin mov. | +0.00 | — | 49 | ❌ L | -1.00 |
| 2026-10-26 | MEM @ UTAH | Spread | UTAH +1.5 | +1.5 | +1.5 | = sin mov. | +0.00 | INFO | 46 | ❌ L | -1.00 |
| 2026-10-26 | MEM @ UTAH | Total | Over 237.5 | 237.5 | 237.5 | = sin mov. | +0.00 | — | 85 | ❌ L | -1.00 |
| 2026-10-26 | ATL @ HOU | ML | ATL ML | 34.3% | 36.9% | ▲ a favor | +2.65 | RLM | 10 | ❌ L | -1.00 |
| 2026-10-26 | ATL @ HOU | Spread | ATL +5.5 | +5.5 | +4.5 | ▲ a favor | +1.00 | RLM,STEAM | 33 | ❌ L | -1.00 |
| 2026-10-26 | ATL @ HOU | Total | Under 229.5 | 229.5 | 228.5 | ▲ a favor | +1.00 | RLM | 16 | ❌ L | -1.00 |
| 2026-10-26 | IND @ MIL | ML | IND ML | 60.0% | 58.3% | ▼ en contra | -1.66 | GRADUAL,RLM | 82 | ❌ L | -1.00 |
| 2026-10-26 | IND @ MIL | Spread | IND -4.5 | -4.5 | -3.5 | ▼ en contra | -1.00 | INFO | 54 | ❌ L | -1.00 |
| 2026-10-26 | IND @ MIL | Total | Over 238.5 | 238.5 | 239.5 | ▲ a favor | +1.00 | — | 75 | ❌ L | -1.00 |
| 2026-10-26 | PHX @ OKC | ML | OKC ML | 77.2% | 73.4% | ▼ en contra | -3.80 | INFO,RLM | 95 | ✅ W | +0.24 |
| 2026-10-26 | PHX @ OKC | Spread | OKC -10.5 | -10.5 | -8.5 | ▼ en contra | -2.00 | INFO,RLM | 56 | ✅ W | +0.91 |
| 2026-10-26 | PHX @ OKC | Total | Under 220.5 | 220.5 | 221.5 | ▼ en contra | -1.00 | — | 16 | ❌ L | -1.00 |
| 2026-10-26 | CHI @ BOS | ML | CHI ML | 14.2% | 15.3% | ▲ a favor | +1.14 | — | 6 | ❌ L | -1.00 |
| 2026-10-26 | CHI @ BOS | Spread | CHI +13.5 | +13.5 | +14.5 | ▼ en contra | -1.00 | RLM,STEAM | 58 | ❌ L | -1.00 |
| 2026-10-26 | CHI @ BOS | Total | Under 233.5 | 233.5 | 233.5 | = sin mov. | -0.00 | RLM,STEAM | 28 | ✅ W | +0.91 |
| 2026-10-26 | DAL @ MIA | ML | DAL ML | 28.6% | 29.0% | = sin mov. | +0.40 | GRADUAL | 10 | ✅ W | +2.35 |
| 2026-10-26 | DAL @ MIA | Spread | DAL +7.5 | +7.5 | +7.5 | = sin mov. | -0.00 | INFO,RLM,STEAM | 65 | ✅ W | +0.91 |
| 2026-10-26 | DAL @ MIA | Total | Over 235.5 | 235.5 | 240.5 | ▲ a favor | +5.00 | GRADUAL | 55 | ❌ L | -1.00 |
| 2026-10-26 | MIN @ CLE | ML | MIN ML | 38.4% | 41.7% | ▲ a favor | +3.34 | GRADUAL,STEAM | 47 | ❌ L | -1.00 |
| 2026-10-26 | MIN @ CLE | Spread | MIN +4.5 | +4.5 | +3.5 | ▲ a favor | +1.00 | INFO,RLM,STEAM | 75 | ✅ W | +0.87 |
| 2026-10-26 | MIN @ CLE | Total | Under 233.5 | 233.5 | 234.5 | ▼ en contra | -1.00 | GRADUAL,RLM | 18 | ❌ L | -1.00 |
| 2026-10-26 | WSH @ CHA | ML | CHA ML | 56.3% | 56.3% | = sin mov. | +0.00 | RLM | 63 | ✅ W | +0.70 |
| 2026-10-26 | WSH @ CHA | Spread | CHA -2.5 | -2.5 | -2.5 | = sin mov. | +0.00 | INFO,STEAM | 35 | ✅ W | +0.87 |
| 2026-10-26 | WSH @ CHA | Total | Under 228.5 | 228.5 | 225.5 | ▲ a favor | +3.00 | RLM,STEAM | 19 | ✅ W | +0.91 |
| 2026-10-25 | MEM @ SAC | ML | SAC ML | 40.0% | 40.0% | = sin mov. | +0.00 | — | 16 | ❌ L | -1.00 |
| 2026-10-25 | MEM @ SAC | Spread | SAC +3.5 | +3.5 | +3.5 | = sin mov. | +0.00 | — | 43 | ❌ L | -1.00 |
| 2026-10-25 | MEM @ SAC | Total | Over 234.5 | 234.5 | 234.5 | = sin mov. | +0.00 | — | 82 | ✅ W | +0.91 |
| 2026-10-25 | DET @ PHI | ML | DET ML | 49.6% | 53.2% | ▲ a favor | +3.68 | RLM | 36 | ✅ W | +0.93 |
| 2026-10-25 | DET @ PHI | Spread | DET -1.5 | -1.5 | -1.5 | = sin mov. | -0.00 | INFO,STEAM | 49 | ✅ W | +0.98 |
| 2026-10-25 | DET @ PHI | Total | Under 227.5 | 227.5 | 228.5 | ▼ en contra | -1.00 | — | 15 | ✅ W | +0.95 |
| 2026-10-25 | LAC @ OKC | ML | LAC ML | 10.7% | 10.7% | = sin mov. | -0.00 | — | 4 | ❌ L | -1.00 |
| 2026-10-25 | LAC @ OKC | Spread | LAC +16.5 | +16.5 | +16.5 | = sin mov. | -0.00 | STEAM | 48 | ✅ W | +0.87 |
| 2026-10-25 | LAC @ OKC | Total | Under 224.5 | 224.5 | 223.5 | ▲ a favor | +1.00 | — | 10 | ✅ W | +0.89 |
| 2026-10-25 | ORL @ NY | ML | NY ML | 71.8% | 70.0% | ▼ en contra | -1.78 | RLM | 94 | ❌ L | -1.00 |
| 2026-10-25 | ORL @ NY | Spread | NY -7.5 | -7.5 | -6.5 | ▼ en contra | -1.00 | INFO | 54 | ❌ L | -1.00 |
| 2026-10-25 | ORL @ NY | Total | Under 224.5 | 224.5 | 224.5 | = sin mov. | -0.00 | — | 17 | ✅ W | +0.87 |
| 2026-10-25 | TOR @ MIN | ML | MIN ML | 51.1% | 60.0% | ▲ a favor | +8.88 | INFO | 81 | ✅ W | +0.87 |
| 2026-10-25 | TOR @ MIN | Spread | TOR +1.5 | +1.5 | +3.5 | ▼ en contra | -2.00 | INFO | 40 | ❌ L | -1.00 |
| 2026-10-25 | TOR @ MIN | Total | Under 229.5 | 229.5 | 228.5 | ▲ a favor | +1.00 | GRADUAL,RLM | 14 | ✅ W | +0.93 |
| 2026-10-25 | IND @ BKN | ML | BKN ML | 29.5% | 32.5% | ▲ a favor | +3.00 | — | 11 | ❌ L | -1.00 |
| 2026-10-25 | IND @ BKN | Spread | BKN +7.5 | +7.5 | +6.5 | ▲ a favor | +1.00 | STEAM | 53 | ❌ L | -1.00 |
| 2026-10-25 | IND @ BKN | Total | Under 231.5 | 231.5 | 231.5 | = sin mov. | -0.00 | — | 18 | ❌ L | -1.00 |
| 2026-10-25 | LAL @ UTAH | ML | UTAH ML | 31.9% | 31.5% | = sin mov. | -0.48 | — | 11 | ❌ L | -1.00 |
| 2026-10-25 | LAL @ UTAH | Spread | LAL -6.5 | -6.5 | -6.5 | = sin mov. | -0.00 | — | 69 | ✅ W | +0.93 |
| 2026-10-25 | LAL @ UTAH | Total | Under 237.5 | 237.5 | 237.5 | = sin mov. | -0.00 | — | 14 | ❌ L | -1.00 |
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
| 2026-10-24 | SA @ DAL | Spread | DAL +12.5 | +12.5 | +14.5 | ▼ en contra | -2.00 | INFO | 56 | ❌ L | -1.00 |
| 2026-10-24 | SA @ DAL | Total | Under 232.5 | 232.5 | 229.5 | ▲ a favor | +3.00 | GRADUAL | 31 | ✅ W | +0.89 |
| 2026-10-24 | WSH @ CHI | ML | CHI ML | 52.6% | 53.2% | ▲ a favor | +0.64 | GRADUAL,RLM | 61 | ❌ L | -1.00 |
| 2026-10-24 | WSH @ CHI | Spread | CHI -2.5 | -2.5 | -1.5 | ▼ en contra | -1.00 | STEAM | 41 | ❌ L | -1.00 |
| 2026-10-24 | WSH @ CHI | Total | Under 244.5 | 244.5 | 244.5 | = sin mov. | -0.00 | — | 49 | ✅ W | +0.87 |
| 2026-10-24 | BKN @ CLE | ML | BKN ML | 20.0% | 20.0% | = sin mov. | -0.00 | — | 5 | ❌ L | -1.00 |
| 2026-10-24 | BKN @ CLE | Spread | BKN +11.5 | +11.5 | +11.5 | = sin mov. | -0.00 | — | 29 | ✅ W | +0.89 |
| 2026-10-24 | BKN @ CLE | Total | Under 228.5 | 228.5 | 228.5 | = sin mov. | -0.00 | RLM | 44 | ❌ L | -1.00 |
| 2026-10-24 | MIL @ PHI | ML | MIL ML | 16.3% | 16.8% | ▲ a favor | +0.54 | — | 7 | ❌ L | -1.00 |
| 2026-10-24 | MIL @ PHI | Spread | MIL +12.5 | +12.5 | +12.5 | = sin mov. | -0.00 | RLM,STEAM | 41 | ✅ W | +0.91 |
| 2026-10-24 | MIL @ PHI | Total | Under 235.5 | 235.5 | 234.5 | ▲ a favor | +1.00 | — | 47 | ❌ L | -1.00 |
| 2026-10-24 | MIA @ CHA | ML | CHA ML | 43.7% | 38.4% | ▼ en contra | -5.29 | GRADUAL | 11 | ✅ W | +1.20 |
| 2026-10-24 | MIA @ CHA | Spread | CHA +3.5 | +3.5 | +4.5 | ▼ en contra | -1.00 | STEAM | 18 | ✅ W | +0.87 |
| 2026-10-24 | MIA @ CHA | Total | Under 229.5 | 229.5 | 227.5 | ▲ a favor | +2.00 | GRADUAL,RLM | 21 | ✅ W | +0.89 |
| 2026-10-23 | LAC @ LAL | ML | LAC ML | 23.4% | 24.9% | ▲ a favor | +1.51 | — | 5 | ❌ L | -1.00 |
| 2026-10-23 | LAC @ LAL | Spread | LAC +9.5 | +9.5 | +8.5 | ▲ a favor | +1.00 | RLM | 35 | ✅ W | +0.89 |
| 2026-10-23 | LAC @ LAL | Total | Under 228.5 | 228.5 | 225.5 | ▲ a favor | +3.00 | RLM | 12 | ❌ L | -1.00 |
| 2026-10-23 | MEM @ GS | ML | GS ML | 58.3% | 59.3% | ▲ a favor | +1.04 | — | 89 | ❌ L | -1.00 |
| 2026-10-23 | MEM @ GS | Spread | GS -3.5 | -3.5 | -4.5 | ▲ a favor | +1.00 | STEAM | 71 | ❌ L | -1.00 |
| 2026-10-23 | MEM @ GS | Total | Under 235.5 | 235.5 | 236.5 | ▼ en contra | -1.00 | — | 28 | ✅ W | +0.91 |
| 2026-10-23 | POR @ SAC | ML | POR ML | 72.2% | 79.1% | ▲ a favor | +6.93 | — | 97 | ✅ W | +0.33 |
| 2026-10-23 | POR @ SAC | Spread | POR -7.5 | -7.5 | -9.5 | ▲ a favor | +2.00 | — | 88 | ✅ W | +0.91 |
| 2026-10-23 | POR @ SAC | Total | Under 232.5 | 232.5 | 231.5 | ▲ a favor | +1.00 | RLM | 33 | ❌ L | -1.00 |
| 2026-10-23 | HOU @ SA | ML | HOU ML | 30.0% | 37.8% | ▲ a favor | +7.77 | GRADUAL,RLM | 9 | ✅ W | +2.20 |
| 2026-10-23 | HOU @ SA | Spread | HOU +6.5 | +6.5 | +4.5 | ▲ a favor | +2.00 | — | 46 | ✅ W | +0.95 |
| 2026-10-23 | HOU @ SA | Total | Under 225.5 | 225.5 | 224.5 | ▲ a favor | +1.00 | RLM | 17 | ✅ W | +0.91 |
| 2026-10-23 | NO @ UTAH | ML | NO ML | 44.9% | 49.6% | ▲ a favor | +4.71 | RLM | 44 | ❌ L | -1.00 |
| 2026-10-23 | NO @ UTAH | Spread | NO +2.5 | +2.5 | +1.5 | ▲ a favor | +1.00 | — | 74 | ✅ W | +0.93 |
| 2026-10-23 | NO @ UTAH | Total | Under 238.5 | 238.5 | 238.5 | = sin mov. | -0.00 | RLM | 23 | ❌ L | -1.00 |
| 2026-10-23 | DET @ MIA | ML | DET ML | 46.8% | 54.3% | ▲ a favor | +7.52 | GRADUAL,RLM | 53 | ✅ W | +1.05 |
| 2026-10-23 | DET @ MIA | Spread | DET +1.5 | +1.5 | -2.5 | ▲ a favor | +4.00 | STEAM | 58 | ✅ W | +0.95 |
| 2026-10-23 | DET @ MIA | Total | Under 234.5 | 234.5 | 235.5 | ▼ en contra | -1.00 | — | 26 | ❌ L | -1.00 |
| 2026-10-23 | ATL @ CHA | ML | CHA ML | 43.7% | 43.7% | = sin mov. | +0.00 | — | 13 | ❌ L | -1.00 |
| 2026-10-23 | ATL @ CHA | Spread | CHA +2.5 | +2.5 | +2.5 | = sin mov. | +0.00 | — | 18 | ❌ L | -1.00 |
| 2026-10-23 | ATL @ CHA | Total | Over 225.5 | 225.5 | 226.5 | ▲ a favor | +1.00 | — | 94 | ❌ L | -1.00 |
| 2026-10-23 | DAL @ IND | ML | DAL ML | 33.6% | 30.4% | ▼ en contra | -3.21 | GRADUAL | 9 | ✅ W | +1.85 |
| 2026-10-23 | DAL @ IND | Spread | IND -5.5 | -5.5 | -7.5 | ▲ a favor | +2.00 | STEAM | 69 | ❌ L | -1.00 |
| 2026-10-23 | DAL @ IND | Total | Over 236.5 | 236.5 | 241.5 | ▲ a favor | +5.00 | GRADUAL | 86 | ❌ L | -1.00 |
| 2026-10-23 | MIN @ ORL | ML | ORL ML | 46.8% | 51.7% | ▲ a favor | +4.98 | RLM | 20 | ❌ L | -1.00 |
| 2026-10-23 | MIN @ ORL | Spread | ORL +1.5 | +1.5 | -1.5 | ▲ a favor | +3.00 | RLM | 21 | ❌ L | -1.00 |
| 2026-10-23 | MIN @ ORL | Total | Under 236.5 | 236.5 | 234.5 | ▲ a favor | +2.00 | GRADUAL,RLM | 23 | ✅ W | +0.91 |
| 2026-10-23 | NY @ BOS | ML | BOS ML | 55.1% | 56.3% | ▲ a favor | +1.21 | — | 65 | ✅ W | +0.74 |
| 2026-10-23 | NY @ BOS | Spread | BOS -2.5 | -2.5 | -2.5 | = sin mov. | +0.00 | — | 56 | ✅ W | +0.91 |
| 2026-10-23 | NY @ BOS | Total | Under 223.5 | 223.5 | 220.5 | ▲ a favor | +3.00 | GRADUAL,RLM | 25 | ✅ W | +0.91 |
| 2026-10-23 | TOR @ WSH | ML | TOR ML | 65.7% | 74.1% | ▲ a favor | +8.34 | GRADUAL | 89 | ✅ W | +0.46 |
| 2026-10-23 | TOR @ WSH | Spread | TOR -5.5 | -5.5 | -9.5 | ▲ a favor | +4.00 | STEAM | 63 | ✅ W | +0.95 |
| 2026-10-23 | TOR @ WSH | Total | Under 236.5 | 236.5 | 236.5 | = sin mov. | -0.00 | — | 10 | ✅ W | +0.89 |
| 2026-10-23 | CHI @ MIL | ML | MIL ML | 51.1% | 52.2% | ▲ a favor | +1.09 | — | 62 | ❌ L | -1.00 |
| 2026-10-23 | CHI @ MIL | Spread | MIL -1.5 | -1.5 | -1.5 | = sin mov. | +0.00 | — | 57 | ❌ L | -1.00 |
| 2026-10-23 | CHI @ MIL | Total | Under 237.5 | 237.5 | 240.5 | ▼ en contra | -3.00 | — | 47 | ❌ L | -1.00 |
| 2026-10-22 | DEN @ OKC | ML | DEN ML | 27.4% | 25.9% | ▼ en contra | -1.51 | — | 9 | ❌ L | -1.00 |
| 2026-10-22 | DEN @ OKC | Spread | DEN +7.5 | +7.5 | +7.5 | = sin mov. | -0.00 | — | 57 | ❌ L | -1.00 |
| 2026-10-22 | DEN @ OKC | Total | Under 235.5 | 235.5 | 236.5 | ▼ en contra | -1.00 | — | 32 | ✅ W | +0.91 |
| 2026-10-22 | CLE @ PHI | ML | CLE ML | 41.7% | 43.7% | ▲ a favor | +1.95 | — | 17 | ❌ L | -1.00 |
| 2026-10-22 | CLE @ PHI | Spread | CLE +3.5 | +3.5 | +2.5 | ▲ a favor | +1.00 | — | 53 | ❌ L | -1.00 |
| 2026-10-22 | CLE @ PHI | Total | Under 235.5 | 235.5 | 236.5 | ▼ en contra | -1.00 | — | 38 | ✅ W | +0.93 |
| 2026-10-21 | SAC @ LAC | ML | LAC ML | 60.9% | 62.2% | ▲ a favor | +1.32 | — | 91 | ✅ W | +0.57 |
| 2026-10-21 | SAC @ LAC | Spread | LAC -4.5 | -4.5 | -5.5 | ▲ a favor | +1.00 | — | 74 | ✅ W | +0.91 |
| 2026-10-21 | SAC @ LAC | Total | Over 229.5 | 229.5 | 226.5 | ▼ en contra | -3.00 | RLM | 76 | ❌ L | -1.00 |
| 2026-10-21 | PHX @ POR | ML | PHX ML | 40.0% | 43.7% | ▲ a favor | +3.61 | RLM | 16 | ❌ L | -1.00 |
| 2026-10-21 | PHX @ POR | Spread | PHX +4.5 | +4.5 | +2.5 | ▲ a favor | +2.00 | — | 44 | ❌ L | -1.00 |
| 2026-10-21 | PHX @ POR | Total | Under 235.5 | 235.5 | 231.5 | ▲ a favor | +4.00 | RLM | 35 | ✅ W | +0.91 |
| 2026-10-21 | GS @ LAL | ML | LAL ML | 70.5% | 66.9% | ▼ en contra | -3.60 | RLM | 82 | ✅ W | +0.36 |
| 2026-10-21 | GS @ LAL | Spread | LAL -7.5 | -7.5 | -6.5 | ▼ en contra | -1.00 | — | 29 | ✅ W | +0.95 |
| 2026-10-21 | GS @ LAL | Total | Over 230.5 | 230.5 | 234.5 | ▲ a favor | +4.00 | — | 62 | ✅ W | +0.91 |
| 2026-10-21 | DAL @ HOU | ML | DAL ML | 26.6% | 22.3% | ▼ en contra | -4.33 | — | 8 | ❌ L | -1.00 |
| 2026-10-21 | DAL @ HOU | Spread | HOU -8.5 | -8.5 | -9.5 | ▲ a favor | +1.00 | RLM | 45 | ✅ W | +0.98 |
| 2026-10-21 | DAL @ HOU | Total | Over 229.5 | 229.5 | 230.5 | ▲ a favor | +1.00 | — | 73 | ✅ W | +0.87 |
| 2026-10-21 | IND @ NO | ML | NO ML | 41.7% | 43.7% | ▲ a favor | +1.95 | — | 16 | ❌ L | -1.00 |
| 2026-10-21 | IND @ NO | Spread | NO +3.5 | +3.5 | +3.5 | = sin mov. | +0.00 | — | 26 | ✅ W | +0.91 |
| 2026-10-21 | IND @ NO | Total | Over 241.5 | 241.5 | 238.5 | ▼ en contra | -3.00 | — | 53 | ✅ W | +0.95 |
| 2026-10-21 | UTAH @ MEM | ML | UTAH ML | 50.4% | 46.8% | ▼ en contra | -3.68 | RLM | 66 | ❌ L | -1.00 |
| 2026-10-21 | UTAH @ MEM | Spread | MEM +1.5 | +1.5 | -1.5 | ▲ a favor | +3.00 | RLM | 41 | ✅ W | +0.87 |
| 2026-10-21 | UTAH @ MEM | Total | Under 242.5 | 242.5 | 240.5 | ▲ a favor | +2.00 | — | 47 | ✅ W | +0.87 |
| 2026-10-21 | CHI @ TOR | ML | TOR ML | 76.6% | 79.1% | ▲ a favor | +2.55 | — | 92 | ✅ W | +0.25 |
| 2026-10-21 | CHI @ TOR | Spread | TOR -9.5 | -9.5 | -10.5 | ▲ a favor | +1.00 | — | 54 | ✅ W | +0.93 |
| 2026-10-21 | CHI @ TOR | Total | Under 236.5 | 236.5 | 237.5 | ▼ en contra | -1.00 | — | 33 | ✅ W | +0.89 |
| 2026-10-21 | MIN @ MIA | ML | MIN ML | 48.3% | 47.4% | ▼ en contra | -0.87 | — | 31 | ✅ W | +0.98 |
| 2026-10-21 | MIN @ MIA | Spread | MIN +1.5 | +1.5 | +1.5 | = sin mov. | -0.00 | — | 57 | ✅ W | +0.89 |
| 2026-10-21 | MIN @ MIA | Total | Under 242.5 | 242.5 | 240.5 | ▲ a favor | +2.00 | — | 44 | ✅ W | +0.93 |
| 2026-10-21 | CHA @ BKN | ML | CHA ML | 51.1% | 52.2% | ▲ a favor | +1.09 | RLM | 59 | ✅ W | +0.87 |
| 2026-10-21 | CHA @ BKN | Spread | CHA -1.5 | -1.5 | -1.5 | = sin mov. | -0.00 | — | 22 | ✅ W | +0.98 |
| 2026-10-21 | CHA @ BKN | Total | Over 220.5 | 220.5 | 220.5 | = sin mov. | +0.00 | RLM | 74 | ❌ L | -1.00 |
| 2026-10-21 | ATL @ ORL | ML | ATL ML | 43.7% | 44.9% | ▲ a favor | +1.21 | RLM | 24 | ✅ W | +1.20 |
| 2026-10-21 | ATL @ ORL | Spread | ATL +2.5 | +2.5 | +2.5 | = sin mov. | -0.00 | — | 54 | ✅ W | +0.95 |
| 2026-10-21 | ATL @ ORL | Total | Under 235.5 | 235.5 | 233.5 | ▲ a favor | +2.00 | GRADUAL,RLM | 36 | ❌ L | -1.00 |
| 2026-10-21 | MIL @ WSH | ML | MIL ML | 36.3% | 39.1% | ▲ a favor | +2.77 | RLM | 11 | ❌ L | -1.00 |
| 2026-10-21 | MIL @ WSH | Spread | MIL +5.5 | +5.5 | +4.5 | ▲ a favor | +1.00 | RLM | 39 | ❌ L | -1.00 |
| 2026-10-21 | MIL @ WSH | Total | Over 238.5 | 238.5 | 238.5 | = sin mov. | +0.00 | — | 52 | ✅ W | +0.95 |
| 2026-10-20 | OKC @ SA | ML | SA ML | 56.3% | 48.3% | ▼ en contra | -8.09 | GRADUAL,RLM | 76 | ❌ L | -1.00 |
| 2026-10-20 | OKC @ SA | Spread | SA -2.5 | -2.5 | +1.5 | ▼ en contra | -4.00 | RLM | 64 | ❌ L | -1.00 |
| 2026-10-20 | OKC @ SA | Total | Under 231.5 | 231.5 | 230.5 | ▲ a favor | +1.00 | RLM | 37 | ✅ W | +0.93 |
| 2026-10-20 | PHI @ NY | ML | NY ML | 63.1% | 61.6% | ▼ en contra | -1.45 | — | 77 | ❌ L | -1.00 |
| 2026-10-20 | PHI @ NY | Spread | NY -4.5 | -4.5 | -4.5 | = sin mov. | +0.00 | — | 30 | ❌ L | -1.00 |
| 2026-10-20 | PHI @ NY | Total | Under 231.5 | 231.5 | 231.5 | = sin mov. | -0.00 | — | 36 | ✅ W | +0.91 |
| 2026-10-20 | BOS @ DET | ML | BOS ML | 50.4% | 52.6% | ▲ a favor | +2.18 | RLM | 38 | ❌ L | -1.00 |
| 2026-10-20 | BOS @ DET | Spread | DET +1.5 | +1.5 | +1.5 | = sin mov. | +0.00 | — | 51 | ✅ W | +0.85 |
| 2026-10-20 | BOS @ DET | Total | Over 222.5 | 222.5 | 219.5 | ▼ en contra | -3.00 | GRADUAL,RLM | 70 | ✅ W | +0.95 |
