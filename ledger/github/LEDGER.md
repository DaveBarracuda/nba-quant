# Ledger de picks — workflow de GitHub
_Actualizado: 2026-11-12 23:39 UTC · un pick por partido y mercado (primer snapshot del modelo, con la línea de DraftKings del NBA Odds Tracker (o de ESPN si el partido no está en el tracker) en ese momento)._

Generado por el workflow *Ejecutar modelo* (modelo sin mezcla). El cierre y el movimiento a favor / en contra se toman al liquidar de la misma fuente que la línea del pick. Ledger de la PC local: [../LEDGER.md](../LEDGER.md)

**Mercado vs modelo:** ▲ *a favor* = la línea de cierre se movió hacia el número del modelo (CLV positivo); ▼ *en contra* = se alejó; umbral 0.25 pts en spread/total y 0.5 pp de probabilidad en ML. CLV en puntos (spread/total) o en pp de probabilidad sin vig (ML). Spread y total se califican contra la línea del pick a −110; ML al precio del pick.

## Récord

| Grupo | Valor | Picks | Calificados | Récord | WR | Unidades | ROI | CLV medio |
|---|---|---|---|---|---|---|---|---|
| GENERAL | todos | 465 | 453 | 207-246-0 | 45.7% | -62.30 | -13.8% | +0.007 |
| mercado | ml | 155 | 151 | 59-92-0 | 39.1% | -42.89 | -28.4% | -0.000 |
| mercado | spread | 155 | 151 | 72-79-0 | 47.7% | -13.42 | -8.9% | -0.093 |
| mercado | total | 155 | 151 | 76-75-0 | 50.3% | -5.99 | -4.0% | +0.113 |
| movimiento | a favor | 129 | 129 | 69-60-0 | 53.5% | +3.90 | +3.0% | +0.846 |
| movimiento | en contra | 112 | 112 | 41-71-0 | 36.6% | -35.21 | -31.4% | -0.948 |
| movimiento | pendiente | 12 | 0 | 0-0-0 | — | +0.00 | — | — |
| movimiento | sin movimiento | 212 | 212 | 97-115-0 | 45.8% | -30.99 | -14.6% | +0.000 |
| mercado × movimiento | ml · a favor | 53 | 53 | 27-26-0 | 50.9% | +0.40 | +0.7% | +0.021 |
| mercado × movimiento | ml · en contra | 46 | 46 | 11-35-0 | 23.9% | -26.84 | -58.3% | -0.025 |
| mercado × movimiento | ml · pendiente | 4 | 0 | 0-0-0 | — | +0.00 | — | — |
| mercado × movimiento | ml · sin movimiento | 52 | 52 | 21-31-0 | 40.4% | -16.45 | -31.6% | +0.000 |
| mercado × movimiento | spread · a favor | 26 | 26 | 14-12-0 | 53.8% | +0.35 | +1.3% | +1.308 |
| mercado × movimiento | spread · en contra | 30 | 30 | 13-17-0 | 43.3% | -5.07 | -16.9% | -1.600 |
| mercado × movimiento | spread · pendiente | 4 | 0 | 0-0-0 | — | +0.00 | — | — |
| mercado × movimiento | spread · sin movimiento | 95 | 95 | 45-50-0 | 47.4% | -8.69 | -9.1% | +0.000 |
| mercado × movimiento | total · a favor | 50 | 50 | 28-22-0 | 56.0% | +3.16 | +6.3% | +1.480 |
| mercado × movimiento | total · en contra | 36 | 36 | 17-19-0 | 47.2% | -3.30 | -9.2% | -1.583 |
| mercado × movimiento | total · pendiente | 4 | 0 | 0-0-0 | — | +0.00 | — | — |
| mercado × movimiento | total · sin movimiento | 65 | 65 | 31-34-0 | 47.7% | -5.85 | -9.0% | +0.000 |

## CLV y movimiento del mercado hacia el modelo

_% hacia el modelo = picks en que la línea se movió a favor ÷ picks con movimiento (sin contar "sin movimiento"); 50% es lo esperado por azar y `p (azar)` es la probabilidad de ver ese % o más si la línea se moviera al azar. CLV medio por pick con cierre conocido, con su intervalo de confianza del 95%: si el intervalo no incluye 0, el CLV es distinguible del azar._

| Mercado | Con cierre | ▲ a favor | ▼ en contra | % hacia el modelo | p (azar) | CLV medio | IC 95% |
|---|---|---|---|---|---|---|---|
| Spread | 151 | 26 | 30 | 46.4% | 0.748 | -0.09 pts | [-0.27, +0.08] |
| Total | 151 | 50 | 36 | 58.1% | 0.080 | +0.11 pts | [-0.10, +0.33] |
| ML | 151 | 53 | 46 | 53.5% | 0.273 | -0.03 pp | [-0.45, +0.39] |
| **Todos** | 453 | 129 | 112 | 53.5% | 0.151 | — | — |

## Picks

| Fecha | Partido | Mercado | Pick | Línea pick | Cierre | Mercado vs modelo | CLV | Alertas | % público en pick | Resultado | Unidades |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-11-12 | CHA @ PHX | ML | CHA ML | 33.1% | — | … pendiente | — | — | 12 | pendiente | — |
| 2026-11-12 | CHA @ PHX | Spread | PHX -6.5 | -6.5 | — | … pendiente | — | — | 77 | pendiente | — |
| 2026-11-12 | CHA @ PHX | Total | Over 214.5 | 214.5 | — | … pendiente | — | — | 86 | pendiente | — |
| 2026-11-12 | DAL @ MIN | ML | MIN ML | 66.3% | — | … pendiente | — | — | 71 | pendiente | — |
| 2026-11-12 | DAL @ MIN | Spread | MIN -5.5 | -5.5 | — | … pendiente | — | — | 42 | pendiente | — |
| 2026-11-12 | DAL @ MIN | Total | Over 225.5 | 225.5 | — | … pendiente | — | — | 69 | pendiente | — |
| 2026-11-12 | DET @ WSH | ML | DET ML | 78.6% | — | … pendiente | — | — | 91 | pendiente | — |
| 2026-11-12 | DET @ WSH | Spread | DET -10.5 | -10.5 | — | … pendiente | — | — | 57 | pendiente | — |
| 2026-11-12 | DET @ WSH | Total | Over 220.5 | 220.5 | — | … pendiente | — | — | 77 | pendiente | — |
| 2026-11-12 | TOR @ PHI | ML | TOR ML | 29.9% | — | … pendiente | — | — | 7 | pendiente | — |
| 2026-11-12 | TOR @ PHI | Spread | TOR +7.5 | +7.5 | — | … pendiente | — | — | 41 | pendiente | — |
| 2026-11-12 | TOR @ PHI | Total | Over 223.5 | 223.5 | — | … pendiente | — | — | 76 | pendiente | — |
| 2026-11-11 | OKC @ POR | ML | POR ML | 49.1% | 57.1% | ▲ a favor | +8.02 | INFO,RLM | 45 | ✅ W | +0.95 |
| 2026-11-11 | OKC @ POR | Spread | POR +1.5 | +1.5 | -2.5 | ▲ a favor | +4.00 | INFO,RLM | 44 | ✅ W | +0.85 |
| 2026-11-11 | OKC @ POR | Total | Under 225.5 | 225.5 | 224.5 | ▲ a favor | +1.00 | — | 20 | ❌ L | -1.00 |
| 2026-11-11 | GS @ HOU | ML | GS ML | 30.3% | 31.5% | ▲ a favor | +1.17 | — | 40 | ❌ L | -1.00 |
| 2026-11-11 | GS @ HOU | Spread | HOU -6.5 | -6.5 | -6.5 | = sin mov. | +0.00 | — | 36 | ✅ W | +0.87 |
| 2026-11-11 | GS @ HOU | Total | Over 219.5 | 219.5 | 219.5 | = sin mov. | +0.00 | — | 85 | ✅ W | +0.87 |
| 2026-11-11 | ORL @ UTAH | ML | UTAH ML | 38.4% | 38.4% | = sin mov. | +0.00 | — | 9 | ❌ L | -1.00 |
| 2026-11-11 | ORL @ UTAH | Spread | UTAH +4.5 | +4.5 | +4.5 | = sin mov. | +0.00 | INFO,STEAM | 28 | ❌ L | -1.00 |
| 2026-11-11 | ORL @ UTAH | Total | Over 214.5 | 214.5 | 216.5 | ▲ a favor | +2.00 | RLM,STEAM | 78 | ✅ W | +0.91 |
| 2026-11-11 | BKN @ NO | ML | BKN ML | 40.7% | 43.7% | ▲ a favor | +2.99 | RLM | 13 | ✅ W | +1.36 |
| 2026-11-11 | BKN @ NO | Spread | BKN +3.5 | +3.5 | +2.5 | ▲ a favor | +1.00 | RLM,STEAM | 35 | ✅ W | +0.88 |
| 2026-11-11 | BKN @ NO | Total | Under 228.5 | 228.5 | 228.5 | = sin mov. | -0.00 | — | 42 | ❌ L | -1.00 |
| 2026-11-11 | DEN @ MEM | ML | MEM ML | 40.1% | 40.7% | ▲ a favor | +0.58 | — | 16 | ❌ L | -1.00 |
| 2026-11-11 | DEN @ MEM | Spread | MEM +3.5 | +3.5 | +3.5 | = sin mov. | +0.00 | STEAM | 38 | ❌ L | -1.00 |
| 2026-11-11 | DEN @ MEM | Total | Over 229.5 | 229.5 | 230.5 | ▲ a favor | +1.00 | — | 73 | ✅ W | +0.93 |
| 2026-11-11 | LAL @ MIL | ML | LAL ML | 85.3% | 86.7% | ▲ a favor | +1.36 | — | 98 | ✅ W | +0.13 |
| 2026-11-11 | LAL @ MIL | Spread | LAL -14.5 | -14.5 | -14.5 | = sin mov. | -0.00 | STEAM | 88 | ❌ L | -1.00 |
| 2026-11-11 | LAL @ MIL | Total | Over 228.5 | 228.5 | 230.5 | ▲ a favor | +2.00 | RLM,STEAM | 68 | ✅ W | +0.89 |
| 2026-11-11 | SA @ CHI | ML | SA ML | 88.7% | 88.6% | = sin mov. | -0.13 | — | 97 | ✅ W | +0.08 |
| 2026-11-11 | SA @ CHI | Spread | SA -15.5 | -15.5 | -15.5 | = sin mov. | -0.00 | — | 85 | ❌ L | -1.00 |
| 2026-11-11 | SA @ CHI | Total | Under 237.5 | 237.5 | 237.5 | = sin mov. | -0.00 | GRADUAL,INFO | 42 | ❌ L | -1.00 |
| 2026-11-11 | BOS @ TOR | ML | TOR ML | 33.8% | 36.3% | ▲ a favor | +2.46 | GRADUAL,RLM | 4 | ❌ L | -1.00 |
| 2026-11-11 | BOS @ TOR | Spread | TOR +5.5 | +5.5 | +4.5 | ▲ a favor | +1.00 | RLM,STEAM | 14 | ✅ W | +0.93 |
| 2026-11-11 | BOS @ TOR | Total | Over 215.5 | 215.5 | 215.5 | = sin mov. | +0.00 | — | 82 | ❌ L | -1.00 |
| 2026-11-11 | CLE @ NY | ML | NY ML | 61.6% | 65.7% | ▲ a favor | +4.12 | GRADUAL | 91 | ❌ L | -1.00 |
| 2026-11-11 | CLE @ NY | Spread | NY -3.5 | -3.5 | -4.5 | ▲ a favor | +1.00 | STEAM | 77 | ❌ L | -1.00 |
| 2026-11-11 | CLE @ NY | Total | Over 221.5 | 221.5 | 220.5 | ▼ en contra | -1.00 | — | 73 | ✅ W | +0.89 |
| 2026-11-11 | WSH @ IND | ML | IND ML | 57.2% | 58.2% | ▲ a favor | +1.03 | — | 64 | ✅ W | +0.68 |
| 2026-11-11 | WSH @ IND | Spread | IND -2.5 | -2.5 | -3.5 | ▲ a favor | +1.00 | STEAM | 45 | ✅ W | +0.87 |
| 2026-11-11 | WSH @ IND | Total | Under 228.5 | 228.5 | 227.5 | ▲ a favor | +1.00 | — | 31 | ✅ W | +0.88 |
| 2026-11-10 | OKC @ POR | ML | OKC ML | 53.4% | 51.8% | ▼ en contra | -1.61 | — | 88 | ❌ L | -1.00 |
| 2026-11-10 | OKC @ POR | Spread | OKC -1.5 | -1.5 | -1.5 | = sin mov. | -0.00 | — | 94 | ❌ L | -1.00 |
| 2026-11-10 | OKC @ POR | Total | Under 226.5 | 226.5 | 226.5 | = sin mov. | -0.00 | — | 18 | ✅ W | +0.88 |
| 2026-11-10 | ORL @ SAC | ML | SAC ML | 33.1% | 34.3% | ▲ a favor | +1.16 | RLM | 15 | ❌ L | -1.00 |
| 2026-11-10 | ORL @ SAC | Spread | SAC +5.5 | +5.5 | +5.5 | = sin mov. | +0.00 | — | 42 | ❌ L | -1.00 |
| 2026-11-10 | ORL @ SAC | Total | Over 222.5 | 222.5 | 222.5 | = sin mov. | +0.00 | — | 80 | ❌ L | -1.00 |
| 2026-11-10 | LAC @ PHX | ML | LAC ML | 39.2% | 38.4% | ▼ en contra | -0.77 | — | 13 | ❌ L | -1.00 |
| 2026-11-10 | LAC @ PHX | Spread | LAC +3.5 | +3.5 | +3.5 | = sin mov. | -0.00 | — | 27 | ❌ L | -1.00 |
| 2026-11-10 | LAC @ PHX | Total | Over 224.5 | 224.5 | 224.5 | = sin mov. | +0.00 | RLM | 78 | ✅ W | +0.93 |
| 2026-11-10 | MIA @ UTAH | ML | UTAH ML | 22.9% | 25.6% | ▲ a favor | +2.63 | INFO,RLM | 5 | ❌ L | -1.00 |
| 2026-11-10 | MIA @ UTAH | Spread | UTAH +9.5 | +9.5 | +8.5 | ▲ a favor | +1.00 | INFO,RLM | 21 | ✅ W | +0.87 |
| 2026-11-10 | MIA @ UTAH | Total | Over 227.5 | 227.5 | 227.5 | = sin mov. | +0.00 | RLM,STEAM | 73 | ❌ L | -1.00 |
| 2026-11-10 | BOS @ PHI | ML | BOS ML | 51.8% | 53.2% | ▲ a favor | +1.40 | RLM | 38 | ✅ W | +0.85 |
| 2026-11-10 | BOS @ PHI | Spread | PHI +1.5 | +1.5 | +1.5 | = sin mov. | +0.00 | — | 60 | ❌ L | -1.00 |
| 2026-11-10 | BOS @ PHI | Total | Over 217.5 | 217.5 | 216.5 | ▼ en contra | -1.00 | — | 85 | ✅ W | +0.93 |
| 2026-11-10 | MIL @ NY | ML | NY ML | 87.5% | 87.9% | = sin mov. | +0.31 | — | 96 | ✅ W | +0.10 |
| 2026-11-10 | MIL @ NY | Spread | NY -15.5 | -15.5 | -15.5 | = sin mov. | +0.00 | INFO | 79 | ✅ W | +0.91 |
| 2026-11-10 | MIL @ NY | Total | Over 221.5 | 221.5 | 221.5 | = sin mov. | +0.00 | — | 79 | ❌ L | -1.00 |
| 2026-11-09 | NO @ GS | ML | NO ML | 21.4% | 18.9% | ▼ en contra | -2.57 | — | 4 | ❌ L | -1.00 |
| 2026-11-09 | NO @ GS | Spread | NO +9.5 | +9.5 | +10.5 | ▼ en contra | -1.00 | STEAM | 23 | ❌ L | -1.00 |
| 2026-11-09 | NO @ GS | Total | Under 231.5 | 231.5 | 228.5 | ▲ a favor | +3.00 | RLM | 24 | ✅ W | +0.88 |
| 2026-11-09 | SA @ PHX | ML | SA ML | 75.7% | 76.7% | ▲ a favor | +0.95 | — | 95 | ✅ W | +0.27 |
| 2026-11-09 | SA @ PHX | Spread | SA -8.5 | -8.5 | -8.5 | = sin mov. | -0.00 | STEAM | 77 | ✅ W | +0.91 |
| 2026-11-09 | SA @ PHX | Total | Under 226.5 | 226.5 | 225.5 | ▲ a favor | +1.00 | — | 21 | ✅ W | +0.88 |
| 2026-11-09 | DEN @ HOU | ML | DEN ML | 39.1% | 36.9% | ▼ en contra | -2.13 | — | 23 | ❌ L | -1.00 |
| 2026-11-09 | DEN @ HOU | Spread | DEN +4.5 | +4.5 | +4.5 | = sin mov. | -0.00 | — | 56 | ❌ L | -1.00 |
| 2026-11-09 | DEN @ HOU | Total | Over 223.5 | 223.5 | 224.5 | ▲ a favor | +1.00 | — | 82 | ❌ L | -1.00 |
| 2026-11-09 | IND @ DAL | ML | DAL ML | 60.5% | 63.1% | ▲ a favor | +2.58 | GRADUAL | 91 | ✅ W | +0.59 |
| 2026-11-09 | IND @ DAL | Spread | DAL -3.5 | -3.5 | -4.5 | ▲ a favor | +1.00 | — | 79 | ❌ L | -1.00 |
| 2026-11-09 | IND @ DAL | Total | Over 226.5 | 226.5 | 227.5 | ▲ a favor | +1.00 | — | 78 | ✅ W | +0.95 |
| 2026-11-09 | MEM @ TOR | ML | TOR ML | 56.3% | 47.8% | ▼ en contra | -8.55 | INFO,RLM | 72 | ❌ L | -1.00 |
| 2026-11-09 | MEM @ TOR | Spread | TOR -2.5 | -2.5 | +1.5 | ▼ en contra | -4.00 | INFO,RLM | 58 | ❌ L | -1.00 |
| 2026-11-09 | MEM @ TOR | Total | Over 228.5 | 228.5 | 225.5 | ▼ en contra | -3.00 | INFO,RLM | 71 | ❌ L | -1.00 |
| 2026-11-09 | CLE @ CHA | ML | CHA ML | 26.0% | 26.6% | ▲ a favor | +0.65 | — | 3 | ✅ W | +2.70 |
| 2026-11-09 | CLE @ CHA | Spread | CHA +8.5 | +8.5 | +8.5 | = sin mov. | +0.00 | STEAM | 15 | ✅ W | +0.96 |
| 2026-11-09 | CLE @ CHA | Total | Over 215.5 | 215.5 | 215.5 | = sin mov. | +0.00 | — | 81 | ✅ W | +0.93 |
| 2026-11-09 | LAL @ ATL | ML | ATL ML | 52.3% | 56.6% | ▲ a favor | +4.30 | INFO,RLM | 24 | ❌ L | -1.00 |
| 2026-11-09 | LAL @ ATL | Spread | ATL -1.5 | -1.5 | -2.5 | ▲ a favor | +1.00 | INFO,RLM | 23 | ❌ L | -1.00 |
| 2026-11-09 | LAL @ ATL | Total | Under 236.5 | 236.5 | 233.5 | ▲ a favor | +3.00 | INFO,RLM | 20 | ❌ L | -1.00 |
| 2026-11-09 | WSH @ DET | ML | DET ML | 80.5% | 77.3% | ▼ en contra | -3.26 | INFO | 95 | ✅ W | +0.19 |
| 2026-11-09 | WSH @ DET | Spread | DET -10.5 | -10.5 | -9.5 | ▼ en contra | -1.00 | INFO | 73 | ✅ W | +0.96 |
| 2026-11-09 | WSH @ DET | Total | Over 219.5 | 219.5 | 218.5 | ▼ en contra | -1.00 | — | 78 | ✅ W | +0.93 |
| 2026-11-08 | MIA @ SAC | ML | SAC ML | 21.5% | 18.2% | ▼ en contra | -3.37 | — | 6 | ❌ L | -1.00 |
| 2026-11-08 | MIA @ SAC | Spread | SAC +10.5 | +10.5 | +11.5 | ▼ en contra | -1.00 | INFO,STEAM | 38 | ✅ W | +0.89 |
| 2026-11-08 | MIA @ SAC | Total | Under 237.5 | 237.5 | 235.5 | ▲ a favor | +2.00 | — | 43 | ✅ W | +0.88 |
| 2026-11-08 | NO @ LAC | ML | LAC ML | 47.4% | 45.9% | ▼ en contra | -1.43 | — | 33 | ✅ W | +1.03 |
| 2026-11-08 | NO @ LAC | Spread | LAC +1.5 | +1.5 | +1.5 | = sin mov. | +0.00 | — | 30 | ✅ W | +0.91 |
| 2026-11-08 | NO @ LAC | Total | Under 226.5 | 226.5 | 225.5 | ▲ a favor | +1.00 | RLM | 26 | ❌ L | -1.00 |
| 2026-11-08 | BOS @ MIL | ML | MIL ML | 15.3% | 14.7% | ▼ en contra | -0.60 | — | 3 | ❌ L | -1.00 |
| 2026-11-08 | BOS @ MIL | Spread | BOS -12.5 | -12.5 | -13.5 | ▲ a favor | +1.00 | STEAM | 77 | ✅ W | +0.86 |
| 2026-11-08 | BOS @ MIL | Total | Over 221.5 | 221.5 | 222.5 | ▲ a favor | +1.00 | — | 75 | ❌ L | -1.00 |
| 2026-11-08 | BKN @ DAL | ML | BKN ML | 27.6% | 27.6% | = sin mov. | -0.00 | — | 6 | ❌ L | -1.00 |
| 2026-11-08 | BKN @ DAL | Spread | BKN +7.5 | +7.5 | +7.5 | = sin mov. | -0.00 | — | 27 | ❌ L | -1.00 |
| 2026-11-08 | BKN @ DAL | Total | Under 222.5 | 222.5 | 223.5 | ▼ en contra | -1.00 | — | 25 | ❌ L | -1.00 |
| 2026-11-08 | UTAH @ MIN | ML | MIN ML | 83.2% | 84.1% | ▲ a favor | +0.92 | — | 96 | ✅ W | +0.15 |
| 2026-11-08 | UTAH @ MIN | Spread | MIN -12.5 | -12.5 | -12.5 | = sin mov. | +0.00 | STEAM | 78 | ✅ W | +0.97 |
| 2026-11-08 | UTAH @ MIN | Total | Under 221.5 | 221.5 | 222.5 | ▼ en contra | -1.00 | — | 23 | ✅ W | +0.93 |
| 2026-11-08 | LAL @ DET | ML | DET ML | 69.7% | 70.5% | ▲ a favor | +0.86 | — | 60 | ❌ L | -1.00 |
| 2026-11-08 | LAL @ DET | Spread | DET -7.5 | -7.5 | -8.5 | ▲ a favor | +1.00 | STEAM | 56 | ❌ L | -1.00 |
| 2026-11-08 | LAL @ DET | Total | Over 217.5 | 217.5 | 216.5 | ▼ en contra | -1.00 | — | 83 | ✅ W | +0.93 |
| 2026-11-07 | SA @ POR | ML | SA ML | 64.6% | 65.7% | ▲ a favor | +1.16 | — | 90 | ✅ W | +0.49 |
| 2026-11-07 | SA @ POR | Spread | SA -5.5 | -5.5 | -5.5 | = sin mov. | -0.00 | STEAM | 69 | ✅ W | +0.93 |
| 2026-11-07 | SA @ POR | Total | Over 225.5 | 225.5 | 228.5 | ▲ a favor | +3.00 | INFO | 81 | ✅ W | +0.87 |
| 2026-11-07 | HOU @ PHX | ML | PHX ML | 29.9% | 30.3% | = sin mov. | +0.37 | — | 6 | ✅ W | +2.21 |
| 2026-11-07 | HOU @ PHX | Spread | PHX +6.5 | +6.5 | +6.5 | = sin mov. | +0.00 | — | 18 | ✅ W | +0.91 |
| 2026-11-07 | HOU @ PHX | Total | Over 223.5 | 223.5 | 223.5 | = sin mov. | +0.00 | — | 83 | ❌ L | -1.00 |
| 2026-11-07 | ORL @ GS | ML | ORL ML | 34.3% | 27.4% | ▼ en contra | -6.84 | STEAM | 4 | ❌ L | -1.00 |
| 2026-11-07 | ORL @ GS | Spread | ORL +5.5 | +5.5 | +7.5 | ▼ en contra | -2.00 | INFO,STEAM | 12 | ❌ L | -1.00 |
| 2026-11-07 | ORL @ GS | Total | Over 222.5 | 222.5 | 220.5 | ▼ en contra | -2.00 | STEAM | 83 | ✅ W | +0.91 |
| 2026-11-07 | NY @ CLE | ML | CLE ML | 35.6% | 36.3% | ▲ a favor | +0.79 | — | 26 | ❌ L | -1.00 |
| 2026-11-07 | NY @ CLE | Spread | NY -4.5 | -4.5 | -4.5 | = sin mov. | -0.00 | INFO,STEAM | 54 | ✅ W | +0.92 |
| 2026-11-07 | NY @ CLE | Total | Over 222.5 | 222.5 | 222.5 | = sin mov. | +0.00 | INFO,RLM | 78 | ❌ L | -1.00 |
| 2026-11-07 | WSH @ OKC | ML | OKC ML | 82.3% | 82.8% | = sin mov. | +0.47 | — | 96 | ✅ W | +0.17 |
| 2026-11-07 | WSH @ OKC | Spread | OKC -12.5 | -12.5 | -12.5 | = sin mov. | +0.00 | INFO,STEAM | 78 | ✅ W | +0.97 |
| 2026-11-07 | WSH @ OKC | Total | Over 222.5 | 222.5 | 223.5 | ▲ a favor | +1.00 | — | 83 | ❌ L | -1.00 |
| 2026-11-07 | BKN @ ATL | ML | ATL ML | 70.1% | 69.7% | = sin mov. | -0.35 | INFO | 94 | ✅ W | +0.37 |
| 2026-11-07 | BKN @ ATL | Spread | ATL -7.5 | -7.5 | -6.5 | ▼ en contra | -1.00 | STEAM | 76 | ❌ L | -1.00 |
| 2026-11-07 | BKN @ ATL | Total | Under 227.5 | 227.5 | 226.5 | ▲ a favor | +1.00 | STEAM | 27 | ❌ L | -1.00 |
| 2026-11-07 | DEN @ IND | ML | DEN ML | 72.4% | 73.4% | ▲ a favor | +1.01 | — | 94 | ✅ W | +0.33 |
| 2026-11-07 | DEN @ IND | Spread | DEN -7.5 | -7.5 | -8.5 | ▲ a favor | +1.00 | STEAM | 81 | ✅ W | +0.94 |
| 2026-11-07 | DEN @ IND | Total | Over 229.5 | 229.5 | 229.5 | = sin mov. | +0.00 | — | 75 | ❌ L | -1.00 |
| 2026-11-06 | POR @ LAL | ML | POR ML | 41.8% | 41.8% | = sin mov. | -0.00 | — | 17 | ❌ L | -1.00 |
| 2026-11-06 | POR @ LAL | Spread | POR +3.5 | +3.5 | +3.5 | = sin mov. | -0.00 | — | 30 | ❌ L | -1.00 |
| 2026-11-06 | POR @ LAL | Total | Under 231.5 | 231.5 | 231.5 | = sin mov. | -0.00 | — | 15 | ❌ L | -1.00 |
| 2026-11-06 | SA @ SAC | ML | SAC ML | 10.6% | 10.6% | = sin mov. | +0.00 | — | 4 | ❌ L | -1.00 |
| 2026-11-06 | SA @ SAC | Spread | SA -17.5 | -17.5 | -17.5 | = sin mov. | -0.00 | — | 73 | ❌ L | -1.00 |
| 2026-11-06 | SA @ SAC | Total | Under 231.5 | 231.5 | 231.5 | = sin mov. | -0.00 | — | 32 | ❌ L | -1.00 |
| 2026-11-06 | MIN @ NO | ML | NO ML | 40.0% | 40.0% | = sin mov. | +0.00 | — | 14 | ❌ L | -1.00 |
| 2026-11-06 | MIN @ NO | Spread | NO +3.5 | +3.5 | +3.5 | = sin mov. | +0.00 | — | 32 | ❌ L | -1.00 |
| 2026-11-06 | MIN @ NO | Total | Under 230.5 | 230.5 | 230.5 | = sin mov. | -0.00 | — | 28 | ✅ W | +0.93 |
| 2026-11-06 | OKC @ MEM | ML | OKC ML | 60.8% | 61.0% | = sin mov. | +0.15 | — | 86 | ✅ W | +0.58 |
| 2026-11-06 | OKC @ MEM | Spread | OKC -4.5 | -4.5 | -3.5 | ▼ en contra | -1.00 | STEAM | 74 | ✅ W | +0.96 |
| 2026-11-06 | OKC @ MEM | Total | Over 223.5 | 223.5 | 224.5 | ▲ a favor | +1.00 | — | 79 | ✅ W | +0.93 |
| 2026-11-06 | TOR @ MIL | ML | TOR ML | 62.2% | 59.3% | ▼ en contra | -2.86 | INFO,RLM | 88 | ✅ W | +0.54 |
| 2026-11-06 | TOR @ MIL | Spread | TOR -4.5 | -4.5 | -3.5 | ▼ en contra | -1.00 | INFO,RLM | 66 | ✅ W | +0.91 |
| 2026-11-06 | TOR @ MIL | Total | Under 228.5 | 228.5 | 228.5 | = sin mov. | -0.00 | — | 38 | ✅ W | +0.95 |
| 2026-11-06 | UTAH @ DAL | ML | UTAH ML | 30.3% | 30.9% | ▲ a favor | +0.56 | — | 5 | ❌ L | -1.00 |
| 2026-11-06 | UTAH @ DAL | Spread | DAL -6.5 | -6.5 | -6.5 | = sin mov. | +0.00 | — | 85 | ✅ W | +0.88 |
| 2026-11-06 | UTAH @ DAL | Total | Under 225.5 | 225.5 | 226.5 | ▼ en contra | -1.00 | — | 22 | ✅ W | +0.93 |
| 2026-11-06 | PHI @ CLE | ML | CLE ML | 42.7% | 42.1% | ▼ en contra | -0.58 | — | 13 | ✅ W | +1.25 |
| 2026-11-06 | PHI @ CLE | Spread | CLE +2.5 | +2.5 | +2.5 | = sin mov. | +0.00 | — | 16 | ✅ W | +0.91 |
| 2026-11-06 | PHI @ CLE | Total | Over 231.5 | 231.5 | 232.5 | ▲ a favor | +1.00 | RLM | 63 | ❌ L | -1.00 |
| 2026-11-06 | BOS @ CHA | ML | CHA ML | 23.3% | 22.3% | ▼ en contra | -1.03 | — | 4 | ❌ L | -1.00 |
| 2026-11-06 | BOS @ CHA | Spread | CHA +10.5 | +10.5 | +10.5 | = sin mov. | +0.00 | — | 19 | ❌ L | -1.00 |
| 2026-11-06 | BOS @ CHA | Total | Over 208.5 | 208.5 | 209.5 | ▲ a favor | +1.00 | STEAM | 85 | ❌ L | -1.00 |
| 2026-11-06 | WSH @ ATL | ML | ATL ML | 69.4% | 72.6% | ▲ a favor | +3.14 | — | 82 | ✅ W | +0.38 |
| 2026-11-06 | WSH @ ATL | Spread | ATL -6.5 | -6.5 | -8.5 | ▲ a favor | +2.00 | — | 49 | ✅ W | +0.86 |
| 2026-11-06 | WSH @ ATL | Total | Under 228.5 | 228.5 | 227.5 | ▲ a favor | +1.00 | — | 34 | ❌ L | -1.00 |
| 2026-11-05 | MIA @ GS | ML | MIA ML | 40.7% | 40.0% | ▼ en contra | -0.74 | — | 22 | ❌ L | -1.00 |
| 2026-11-05 | MIA @ GS | Spread | MIA +3.5 | +3.5 | +3.5 | = sin mov. | -0.00 | — | 49 | ❌ L | -1.00 |
| 2026-11-05 | MIA @ GS | Total | Over 235.5 | 235.5 | 236.5 | ▲ a favor | +1.00 | — | 72 | ❌ L | -1.00 |
| 2026-11-05 | ORL @ PHX | ML | PHX ML | 51.8% | 52.5% | ▲ a favor | +0.76 | RLM | 68 | ✅ W | +0.85 |
| 2026-11-05 | ORL @ PHX | Spread | PHX -1.5 | -1.5 | -1.5 | = sin mov. | +0.00 | — | 65 | ✅ W | +0.98 |
| 2026-11-05 | ORL @ PHX | Total | Over 222.5 | 222.5 | 222.5 | = sin mov. | +0.00 | — | 77 | ❌ L | -1.00 |
| 2026-11-04 | MIA @ LAC | ML | LAC ML | 36.3% | 34.3% | ▼ en contra | -2.03 | — | 8 | ❌ L | -1.00 |
| 2026-11-04 | MIA @ LAC | Spread | LAC +4.5 | +4.5 | +5.5 | ▼ en contra | -1.00 | STEAM | 38 | ✅ W | +0.95 |
| 2026-11-04 | MIA @ LAC | Total | Over 233.5 | 233.5 | 233.5 | = sin mov. | +0.00 | — | 79 | ❌ L | -1.00 |
| 2026-11-04 | LAL @ SAC | ML | SAC ML | 17.6% | 16.8% | ▼ en contra | -0.77 | — | 3 | ❌ L | -1.00 |
| 2026-11-04 | LAL @ SAC | Spread | LAL -12.5 | -12.5 | -12.5 | = sin mov. | -0.00 | STEAM | 66 | ✅ W | +0.95 |
| 2026-11-04 | LAL @ SAC | Total | Under 234.5 | 234.5 | 233.5 | ▲ a favor | +1.00 | RLM | 18 | ✅ W | +0.91 |
| 2026-11-04 | DAL @ SA | ML | SA ML | 82.3% | 82.8% | = sin mov. | +0.47 | — | 93 | ✅ W | +0.17 |
| 2026-11-04 | DAL @ SA | Spread | SA -12.5 | -12.5 | -12.5 | = sin mov. | +0.00 | — | 42 | ❌ L | -1.00 |
| 2026-11-04 | DAL @ SA | Total | Under 226.5 | 226.5 | 226.5 | = sin mov. | -0.00 | RLM | 14 | ✅ W | +0.87 |
| 2026-11-04 | POR @ PHX | ML | POR ML | 58.3% | 57.2% | ▼ en contra | -1.09 | — | 85 | ✅ W | +0.65 |
| 2026-11-04 | POR @ PHX | Spread | POR -3.5 | -3.5 | -2.5 | ▼ en contra | -1.00 | STEAM | 57 | ✅ W | +0.97 |
| 2026-11-04 | POR @ PHX | Total | Under 227.5 | 227.5 | 227.5 | = sin mov. | -0.00 | — | 14 | ❌ L | -1.00 |
| 2026-11-04 | TOR @ DEN | ML | TOR ML | 36.9% | 35.7% | ▼ en contra | -1.22 | RLM | 11 | ❌ L | -1.00 |
| 2026-11-04 | TOR @ DEN | Spread | TOR +4.5 | +4.5 | +4.5 | = sin mov. | -0.00 | — | 45 | ❌ L | -1.00 |
| 2026-11-04 | TOR @ DEN | Total | Over 230.5 | 230.5 | 231.5 | ▲ a favor | +1.00 | — | 81 | ✅ W | +0.93 |
| 2026-11-04 | MIN @ HOU | ML | MIN ML | 28.7% | 29.4% | ▲ a favor | +0.69 | RLM | 10 | ✅ W | +2.35 |
| 2026-11-04 | MIN @ HOU | Spread | MIN +7.5 | +7.5 | +7.5 | = sin mov. | -0.00 | STEAM | 49 | ✅ W | +0.90 |
| 2026-11-04 | MIN @ HOU | Total | Over 220.5 | 220.5 | 219.5 | ▼ en contra | -1.00 | RLM | 87 | ✅ W | +0.92 |
| 2026-11-04 | CLE @ OKC | ML | OKC ML | 58.4% | 59.3% | ▲ a favor | +0.88 | — | 70 | ✅ W | +0.65 |
| 2026-11-04 | CLE @ OKC | Spread | OKC -3.5 | -3.5 | -3.5 | = sin mov. | +0.00 | RLM | 39 | ✅ W | +0.93 |
| 2026-11-04 | CLE @ OKC | Total | Over 226.5 | 226.5 | 226.5 | = sin mov. | +0.00 | — | 85 | ✅ W | +0.88 |
| 2026-11-04 | IND @ MEM | ML | MEM ML | 68.0% | 66.8% | ▼ en contra | -1.24 | GRADUAL,RLM | 91 | ❌ L | -1.00 |
| 2026-11-04 | IND @ MEM | Spread | MEM -6.5 | -6.5 | -5.5 | ▼ en contra | -1.00 | INFO,STEAM | 62 | ❌ L | -1.00 |
| 2026-11-04 | IND @ MEM | Total | Over 229.5 | 229.5 | 227.5 | ▼ en contra | -2.00 | RLM | 83 | ❌ L | -1.00 |
| 2026-11-04 | UTAH @ NO | ML | NO ML | 66.8% | 64.2% | ▼ en contra | -2.61 | — | 89 | ✅ W | +0.44 |
| 2026-11-04 | UTAH @ NO | Spread | NO -5.5 | -5.5 | -5.5 | = sin mov. | +0.00 | INFO,STEAM | 62 | ✅ W | +0.84 |
| 2026-11-04 | UTAH @ NO | Total | Under 232.5 | 232.5 | 231.5 | ▲ a favor | +1.00 | GRADUAL,RLM | 26 | ❌ L | -1.00 |
| 2026-11-04 | CHA @ BKN | ML | BKN ML | 39.7% | 39.5% | = sin mov. | -0.15 | — | 21 | ✅ W | +1.42 |
| 2026-11-04 | CHA @ BKN | Spread | BKN +3.5 | +3.5 | +3.5 | = sin mov. | +0.00 | STEAM | 49 | ✅ W | +0.91 |
| 2026-11-04 | CHA @ BKN | Total | Under 212.5 | 212.5 | 213.5 | ▼ en contra | -1.00 | — | 20 | ❌ L | -1.00 |
| 2026-11-04 | CHI @ NY | ML | NY ML | 82.3% | 81.8% | ▼ en contra | -0.54 | — | 96 | ✅ W | +0.17 |
| 2026-11-04 | CHI @ NY | Spread | NY -11.5 | -11.5 | -11.5 | = sin mov. | +0.00 | STEAM | 61 | ✅ W | +0.87 |
| 2026-11-04 | CHI @ NY | Total | Under 233.5 | 233.5 | 233.5 | = sin mov. | -0.00 | — | 30 | ❌ L | -1.00 |
| 2026-11-04 | MIL @ BOS | ML | MIL ML | 18.3% | 18.3% | = sin mov. | -0.00 | RLM | 4 | ❌ L | -1.00 |
| 2026-11-04 | MIL @ BOS | Spread | BOS -11.5 | -11.5 | -12.5 | ▲ a favor | +1.00 | INFO,RLM,STEAM | 62 | ❌ L | -1.00 |
| 2026-11-04 | MIL @ BOS | Total | Over 223.5 | 223.5 | 222.5 | ▼ en contra | -1.00 | GRADUAL,RLM | 80 | ❌ L | -1.00 |
| 2026-11-04 | ATL @ WSH | ML | ATL ML | 58.2% | 53.2% | ▼ en contra | -5.08 | INFO | 54 | ✅ W | +0.65 |
| 2026-11-04 | ATL @ WSH | Spread | ATL -2.5 | -2.5 | -1.5 | ▼ en contra | -1.00 | INFO,RLM,STEAM | 33 | ✅ W | +0.85 |
| 2026-11-04 | ATL @ WSH | Total | Under 232.5 | 232.5 | 229.5 | ▲ a favor | +3.00 | INFO,RLM | 38 | ✅ W | +0.92 |
| 2026-11-04 | PHI @ DET | ML | DET ML | 56.3% | 55.3% | ▼ en contra | -1.01 | RLM | 35 | ❌ L | -1.00 |
| 2026-11-04 | PHI @ DET | Spread | DET -2.5 | -2.5 | -2.5 | = sin mov. | +0.00 | — | 23 | ❌ L | -1.00 |
| 2026-11-04 | PHI @ DET | Total | Under 219.5 | 219.5 | 219.5 | = sin mov. | -0.00 | — | 22 | ✅ W | +0.89 |
| 2026-11-02 | MIA @ LAL | ML | LAL ML | 53.2% | 54.3% | ▲ a favor | +1.03 | GRADUAL | 70 | ✅ W | +0.80 |
| 2026-11-02 | MIA @ LAL | Spread | LAL -1.5 | -1.5 | -1.5 | = sin mov. | +0.00 | RLM,STEAM | 42 | ✅ W | +0.88 |
| 2026-11-02 | MIA @ LAL | Total | Under 236.5 | 236.5 | 238.5 | ▼ en contra | -2.00 | — | 12 | ❌ L | -1.00 |
| 2026-11-02 | PHX @ GS | ML | PHX ML | 42.6% | 44.7% | ▲ a favor | +2.04 | RLM | 13 | ❌ L | -1.00 |
| 2026-11-02 | PHX @ GS | Spread | PHX +2.5 | +2.5 | +2.5 | = sin mov. | -0.00 | — | 42 | ❌ L | -1.00 |
| 2026-11-02 | PHX @ GS | Total | Over 227.5 | 227.5 | 227.5 | = sin mov. | +0.00 | — | 92 | ✅ W | +0.87 |
| 2026-11-02 | TOR @ LAC | ML | TOR ML | 64.4% | 66.8% | ▲ a favor | +2.36 | INFO,RLM | 91 | ✅ W | +0.49 |
| 2026-11-02 | TOR @ LAC | Spread | TOR -4.5 | -4.5 | -6.5 | ▲ a favor | +2.00 | INFO,STEAM | 67 | ✅ W | +0.85 |
| 2026-11-02 | TOR @ LAC | Total | Under 221.5 | 221.5 | 219.5 | ▲ a favor | +2.00 | — | 8 | ❌ L | -1.00 |
| 2026-11-02 | POR @ DEN | ML | POR ML | 39.0% | 39.0% | = sin mov. | -0.00 | — | 21 | ✅ W | +1.46 |
| 2026-11-02 | POR @ DEN | Spread | POR +4.5 | +4.5 | +4.5 | = sin mov. | -0.00 | — | 53 | ✅ W | +0.89 |
| 2026-11-02 | POR @ DEN | Total | Under 230.5 | 230.5 | 231.5 | ▼ en contra | -1.00 | — | 9 | ✅ W | +0.95 |
| 2026-11-02 | BOS @ HOU | ML | BOS ML | 36.9% | 38.4% | ▲ a favor | +1.46 | — | 31 | ❌ L | -1.00 |
| 2026-11-02 | BOS @ HOU | Spread | BOS +4.5 | +4.5 | +4.5 | = sin mov. | -0.00 | STEAM | 60 | ❌ L | -1.00 |
| 2026-11-02 | BOS @ HOU | Total | Over 218.5 | 218.5 | 215.5 | ▼ en contra | -3.00 | GRADUAL,RLM | 94 | ❌ L | -1.00 |
| 2026-11-02 | UTAH @ SA | ML | SA ML | 88.6% | 88.6% | = sin mov. | +0.00 | — | 98 | ✅ W | +0.08 |
| 2026-11-02 | UTAH @ SA | Spread | SA -16.5 | -16.5 | -16.5 | = sin mov. | +0.00 | STEAM | 54 | ✅ W | +0.97 |
| 2026-11-02 | UTAH @ SA | Total | Under 229.5 | 229.5 | 226.5 | ▲ a favor | +3.00 | RLM | 15 | ✅ W | +0.91 |
| 2026-11-02 | MIL @ MIN | ML | MIN ML | 79.2% | 80.0% | ▲ a favor | +0.78 | — | 95 | ✅ W | +0.21 |
| 2026-11-02 | MIL @ MIN | Spread | MIN -11.5 | -11.5 | -11.5 | = sin mov. | +0.00 | INFO,STEAM | 55 | ✅ W | +0.95 |
| 2026-11-02 | MIL @ MIN | Total | Under 234.5 | 234.5 | 233.5 | ▲ a favor | +1.00 | INFO,RLM,STEAM | 17 | ✅ W | +0.87 |
| 2026-11-02 | NO @ MEM | ML | NO ML | 36.4% | 34.5% | ▼ en contra | -1.84 | RLM | 10 | ✅ W | +1.64 |
| 2026-11-02 | NO @ MEM | Spread | NO +5.5 | +5.5 | +5.5 | = sin mov. | -0.00 | — | 38 | ✅ W | +0.91 |
| 2026-11-02 | NO @ MEM | Total | Under 233.5 | 233.5 | 231.5 | ▲ a favor | +2.00 | RLM | 12 | ❌ L | -1.00 |
| 2026-11-02 | SAC @ DAL | ML | SAC ML | 22.9% | 28.2% | ▲ a favor | +5.29 | GRADUAL,RLM | 3 | ✅ W | +3.20 |
| 2026-11-02 | SAC @ DAL | Spread | SAC +10.5 | +10.5 | +7.5 | ▲ a favor | +3.00 | RLM,STEAM | 27 | ✅ W | +0.90 |
| 2026-11-02 | SAC @ DAL | Total | Under 232.5 | 232.5 | 232.5 | = sin mov. | -0.00 | RLM | 13 | ✅ W | +0.91 |
| 2026-11-02 | ATL @ IND | ML | IND ML | 36.1% | 21.8% | ▼ en contra | -14.27 | INFO | 14 | ❌ L | -1.00 |
| 2026-11-02 | ATL @ IND | Spread | IND +5.5 | +5.5 | +10.5 | ▼ en contra | -5.00 | INFO,STEAM | 39 | ✅ W | +0.87 |
| 2026-11-02 | ATL @ IND | Total | Over 231.5 | 231.5 | 226.5 | ▼ en contra | -5.00 | GRADUAL,RLM,STEAM | 85 | ❌ L | -1.00 |
| 2026-11-02 | BKN @ NY | ML | BKN ML | 12.8% | 13.0% | = sin mov. | +0.16 | — | 4 | ❌ L | -1.00 |
| 2026-11-02 | BKN @ NY | Spread | NY -14.5 | -14.5 | -14.5 | = sin mov. | +0.00 | — | 52 | ❌ L | -1.00 |
| 2026-11-02 | BKN @ NY | Total | Under 219.5 | 219.5 | 218.5 | ▲ a favor | +1.00 | RLM | 38 | ✅ W | +0.87 |
| 2026-11-02 | CHI @ PHI | ML | CHI ML | 19.0% | 19.5% | = sin mov. | +0.46 | RLM | 3 | ❌ L | -1.00 |
| 2026-11-02 | CHI @ PHI | Spread | CHI +10.5 | +10.5 | +10.5 | = sin mov. | -0.00 | RLM,STEAM | 30 | ❌ L | -1.00 |
| 2026-11-02 | CHI @ PHI | Total | Under 238.5 | 238.5 | 240.5 | ▼ en contra | -2.00 | — | 27 | ✅ W | +0.93 |
| 2026-11-02 | DET @ CHA | ML | CHA ML | 35.2% | 33.7% | ▼ en contra | -1.47 | GRADUAL | 7 | ❌ L | -1.00 |
| 2026-11-02 | DET @ CHA | Spread | CHA +5.5 | +5.5 | +5.5 | = sin mov. | +0.00 | STEAM | 15 | ❌ L | -1.00 |
| 2026-11-02 | DET @ CHA | Total | Under 209.5 | 209.5 | 209.5 | = sin mov. | -0.00 | — | 49 | ❌ L | -1.00 |
| 2026-11-02 | WSH @ ORL | ML | ORL ML | 57.3% | 58.2% | ▲ a favor | +0.92 | GRADUAL | 51 | ❌ L | -1.00 |
| 2026-11-02 | WSH @ ORL | Spread | ORL -2.5 | -2.5 | -2.5 | = sin mov. | +0.00 | RLM,STEAM | 29 | ❌ L | -1.00 |
| 2026-11-02 | WSH @ ORL | Total | Under 225.5 | 225.5 | 224.5 | ▲ a favor | +1.00 | — | 14 | ✅ W | +0.91 |
| 2026-11-02 | OKC @ CLE | ML | OKC ML | 38.4% | 39.1% | ▲ a favor | +0.68 | — | 21 | ✅ W | +1.50 |
| 2026-11-02 | OKC @ CLE | Spread | OKC +4.5 | +4.5 | +4.5 | = sin mov. | -0.00 | STEAM | 18 | ✅ W | +0.85 |
| 2026-11-02 | OKC @ CLE | Total | Under 229.5 | 229.5 | 229.5 | = sin mov. | -0.00 | — | 13 | ✅ W | +0.87 |
| 2026-11-01 | TOR @ LAL | ML | TOR ML | 42.8% | 39.6% | ▼ en contra | -3.17 | GRADUAL,RLM | 11 | ❌ L | -1.00 |
| 2026-11-01 | TOR @ LAL | Spread | TOR +2.5 | +2.5 | +3.5 | ▼ en contra | -1.00 | RLM,STEAM | 24 | ❌ L | -1.00 |
| 2026-11-01 | TOR @ LAL | Total | Under 224.5 | 224.5 | 223.5 | ▲ a favor | +1.00 | RLM | 14 | ❌ L | -1.00 |
| 2026-11-01 | LAC @ GS | ML | GS ML | 54.3% | 54.3% | = sin mov. | +0.00 | — | 84 | ✅ W | +0.77 |
| 2026-11-01 | LAC @ GS | Spread | GS -2.5 | -2.5 | -2.5 | = sin mov. | +0.00 | STEAM | 70 | ✅ W | +0.98 |
| 2026-11-01 | LAC @ GS | Total | Over 220.5 | 220.5 | 220.5 | = sin mov. | +0.00 | — | 80 | ✅ W | +0.89 |
| 2026-11-01 | BKN @ IND | ML | IND ML | 60.4% | 58.3% | ▼ en contra | -2.08 | RLM | 86 | ❌ L | -1.00 |
| 2026-11-01 | BKN @ IND | Spread | IND -3.5 | -3.5 | -3.5 | = sin mov. | +0.00 | — | 73 | ❌ L | -1.00 |
| 2026-11-01 | BKN @ IND | Total | Under 230.5 | 230.5 | 230.5 | = sin mov. | -0.00 | — | 23 | ✅ W | +0.93 |
| 2026-10-31 | OKC @ HOU | ML | OKC ML | 42.8% | 43.7% | ▲ a favor | +0.86 | — | 29 | ❌ L | -1.00 |
| 2026-10-31 | OKC @ HOU | Spread | OKC +2.5 | +2.5 | +2.5 | = sin mov. | -0.00 | — | 40 | ❌ L | -1.00 |
| 2026-10-31 | OKC @ HOU | Total | Under 219.5 | 219.5 | 219.5 | = sin mov. | -0.00 | — | 13 | ✅ W | +0.87 |
| 2026-10-31 | CLE @ MIL | ML | MIL ML | 23.4% | 25.9% | ▲ a favor | +2.50 | — | 6 | ❌ L | -1.00 |
| 2026-10-31 | CLE @ MIL | Spread | CLE -9.5 | -9.5 | -8.5 | ▼ en contra | -1.00 | STEAM | 68 | ✅ W | +0.89 |
| 2026-10-31 | CLE @ MIL | Total | Under 235.5 | 235.5 | 234.5 | ▲ a favor | +1.00 | RLM | 23 | ❌ L | -1.00 |
| 2026-10-31 | MIN @ SA | ML | MIN ML | 18.3% | 18.3% | = sin mov. | -0.00 | — | 9 | ❌ L | -1.00 |
| 2026-10-31 | MIN @ SA | Spread | MIN +12.5 | +12.5 | +12.5 | = sin mov. | -0.00 | — | 48 | ✅ W | +0.87 |
| 2026-10-31 | MIN @ SA | Total | Under 225.5 | 225.5 | 230.5 | ▼ en contra | -5.00 | INFO | 12 | ❌ L | -1.00 |
| 2026-10-31 | SAC @ MEM | ML | SAC ML | 24.3% | 28.2% | ▲ a favor | +3.92 | RLM,STEAM | 6 | ❌ L | -1.00 |
| 2026-10-31 | SAC @ MEM | Spread | SAC +8.5 | +8.5 | +7.5 | ▲ a favor | +1.00 | INFO,RLM,STEAM | 26 | ❌ L | -1.00 |
| 2026-10-31 | SAC @ MEM | Total | Over 230.5 | 230.5 | 229.5 | ▼ en contra | -1.00 | RLM | 86 | ✅ W | +0.95 |
| 2026-10-31 | ATL @ NO | ML | ATL ML | 61.6% | 63.7% | ▲ a favor | +2.05 | — | 87 | ❌ L | -1.00 |
| 2026-10-31 | ATL @ NO | Spread | ATL -4.5 | -4.5 | -5.5 | ▲ a favor | +1.00 | STEAM | 77 | ❌ L | -1.00 |
| 2026-10-31 | ATL @ NO | Total | Under 240.5 | 240.5 | 239.5 | ▲ a favor | +1.00 | — | 39 | ✅ W | +0.89 |
| 2026-10-31 | PHI @ CHA | ML | CHA ML | 50.4% | 45.7% | ▼ en contra | -4.71 | RLM,STEAM | 13 | ❌ L | -1.00 |
| 2026-10-31 | PHI @ CHA | Spread | CHA -1.5 | -1.5 | +2.5 | ▼ en contra | -4.00 | INFO,STEAM | 6 | ❌ L | -1.00 |
| 2026-10-31 | PHI @ CHA | Total | Under 213.5 | 213.5 | 212.5 | ▲ a favor | +1.00 | RLM | 20 | ✅ W | +0.91 |
| 2026-10-31 | POR @ UTAH | ML | UTAH ML | 27.4% | 30.9% | ▲ a favor | +3.50 | STEAM | 11 | ❌ L | -1.00 |
| 2026-10-31 | POR @ UTAH | Spread | POR -7.5 | -7.5 | -6.5 | ▼ en contra | -1.00 | STEAM | 72 | ✅ W | +0.89 |
| 2026-10-31 | POR @ UTAH | Total | Under 231.5 | 231.5 | 232.5 | ▼ en contra | -1.00 | STEAM | 18 | ✅ W | +0.93 |
| 2026-10-30 | DEN @ PHX | ML | PHX ML | 38.4% | 38.4% | = sin mov. | +0.00 | — | 10 | ❌ L | -1.00 |
| 2026-10-30 | DEN @ PHX | Spread | PHX +3.5 | +3.5 | +4.5 | ▼ en contra | -1.00 | STEAM | 25 | ❌ L | -1.00 |
| 2026-10-30 | DEN @ PHX | Total | Under 231.5 | 231.5 | 231.5 | = sin mov. | -0.00 | — | 12 | ❌ L | -1.00 |
| 2026-10-30 | LAL @ GS | ML | LAL ML | 57.2% | 56.3% | ▼ en contra | -0.86 | — | 69 | ❌ L | -1.00 |
| 2026-10-30 | LAL @ GS | Spread | LAL -3.5 | -3.5 | -2.5 | ▼ en contra | -1.00 | STEAM | 56 | ❌ L | -1.00 |
| 2026-10-30 | LAL @ GS | Total | Under 233.5 | 233.5 | 234.5 | ▼ en contra | -1.00 | — | 18 | ✅ W | +0.93 |
| 2026-10-30 | HOU @ DAL | ML | HOU ML | 67.5% | 63.7% | ▼ en contra | -3.81 | INFO | 86 | ❌ L | -1.00 |
| 2026-10-30 | HOU @ DAL | Spread | HOU -6.5 | -6.5 | -5.5 | ▼ en contra | -1.00 | INFO | 58 | ❌ L | -1.00 |
| 2026-10-30 | HOU @ DAL | Total | Over 223.5 | 223.5 | 223.5 | = sin mov. | +0.00 | — | 94 | ✅ W | +0.95 |
| 2026-10-30 | IND @ MIA | ML | MIA ML | 73.4% | 73.4% | = sin mov. | +0.00 | — | 89 | ✅ W | +0.31 |
| 2026-10-30 | IND @ MIA | Spread | MIA -8.5 | -8.5 | -8.5 | = sin mov. | +0.00 | — | 46 | ✅ W | +0.87 |
| 2026-10-30 | IND @ MIA | Total | Over 237.5 | 237.5 | 237.5 | = sin mov. | +0.00 | — | 86 | ✅ W | +0.91 |
| 2026-10-30 | LAC @ MIN | ML | LAC ML | 30.4% | 30.4% | = sin mov. | -0.00 | — | 7 | ❌ L | -1.00 |
| 2026-10-30 | LAC @ MIN | Spread | LAC +6.5 | +6.5 | +6.5 | = sin mov. | -0.00 | STEAM | 46 | ❌ L | -1.00 |
| 2026-10-30 | LAC @ MIN | Total | Under 223.5 | 223.5 | 222.5 | ▲ a favor | +1.00 | — | 12 | ❌ L | -1.00 |
| 2026-10-30 | CHI @ BOS | ML | CHI ML | 13.2% | 14.2% | ▲ a favor | +0.98 | — | 5 | ❌ L | -1.00 |
| 2026-10-30 | CHI @ BOS | Spread | BOS -15.5 | -15.5 | -14.5 | ▼ en contra | -1.00 | STEAM | 55 | ❌ L | -1.00 |
| 2026-10-30 | CHI @ BOS | Total | Under 235.5 | 235.5 | 236.5 | ▼ en contra | -1.00 | — | 17 | ❌ L | -1.00 |
| 2026-10-30 | DET @ BKN | ML | BKN ML | 27.4% | 27.4% | = sin mov. | +0.00 | — | 6 | ❌ L | -1.00 |
| 2026-10-30 | DET @ BKN | Spread | BKN +8.5 | +8.5 | +8.5 | = sin mov. | +0.00 | STEAM | 30 | ❌ L | -1.00 |
| 2026-10-30 | DET @ BKN | Total | Under 222.5 | 222.5 | 222.5 | = sin mov. | -0.00 | — | 14 | ✅ W | +0.89 |
| 2026-10-30 | NY @ PHI | ML | NY ML | 53.2% | 58.3% | ▲ a favor | +5.05 | STEAM | 49 | ❌ L | -1.00 |
| 2026-10-30 | NY @ PHI | Spread | NY -1.5 | -1.5 | -3.5 | ▲ a favor | +2.00 | INFO,RLM,STEAM | 33 | ❌ L | -1.00 |
| 2026-10-30 | NY @ PHI | Total | Under 226.5 | 226.5 | 225.5 | ▲ a favor | +1.00 | INFO,RLM | 16 | ✅ W | +0.93 |
| 2026-10-30 | ORL @ TOR | ML | TOR ML | 65.7% | 65.7% | = sin mov. | +0.00 | — | 93 | ❌ L | -1.00 |
| 2026-10-30 | ORL @ TOR | Spread | TOR -5.5 | -5.5 | -5.5 | = sin mov. | +0.00 | — | 81 | ❌ L | -1.00 |
| 2026-10-30 | ORL @ TOR | Total | Under 227.5 | 227.5 | 227.5 | = sin mov. | -0.00 | — | 10 | ❌ L | -1.00 |
| 2026-10-30 | CHA @ WSH | ML | CHA ML | 51.1% | 51.1% | = sin mov. | -0.00 | GRADUAL | 38 | ❌ L | -1.00 |
| 2026-10-30 | CHA @ WSH | Spread | CHA -1.5 | -1.5 | -1.5 | = sin mov. | -0.00 | — | 43 | ❌ L | -1.00 |
| 2026-10-30 | CHA @ WSH | Total | Over 218.5 | 218.5 | 218.5 | = sin mov. | +0.00 | RLM | 86 | ❌ L | -1.00 |
| 2026-10-29 | MEM @ POR | ML | POR ML | 71.4% | 71.0% | = sin mov. | -0.40 | — | 89 | ❌ L | -1.00 |
| 2026-10-29 | MEM @ POR | Spread | POR -7.5 | -7.5 | -7.5 | = sin mov. | +0.00 | INFO,STEAM | 64 | ❌ L | -1.00 |
| 2026-10-29 | MEM @ POR | Total | Under 232.5 | 232.5 | 232.5 | = sin mov. | -0.00 | RLM,STEAM | 14 | ✅ W | +0.95 |
| 2026-10-29 | CLE @ ATL | ML | ATL ML | 51.1% | 51.7% | ▲ a favor | +0.65 | RLM | 44 | ✅ W | +0.87 |
| 2026-10-29 | CLE @ ATL | Spread | ATL -1.5 | -1.5 | -1.5 | = sin mov. | +0.00 | — | 45 | ✅ W | +0.95 |
| 2026-10-29 | CLE @ ATL | Total | Under 237.5 | 237.5 | 237.5 | = sin mov. | -0.00 | — | 17 | ✅ W | +0.95 |
| 2026-10-29 | SAC @ NO | ML | SAC ML | 32.5% | 32.5% | = sin mov. | -0.00 | — | 14 | ❌ L | -1.00 |
| 2026-10-29 | SAC @ NO | Spread | SAC +6.5 | +6.5 | +6.5 | = sin mov. | -0.00 | INFO,STEAM | 32 | ❌ L | -1.00 |
| 2026-10-29 | SAC @ NO | Total | Under 236.5 | 236.5 | 234.5 | ▲ a favor | +2.00 | RLM | 30 | ❌ L | -1.00 |
| 2026-10-28 | LAL @ LAC | ML | LAC ML | 37.8% | 50.4% | ▲ a favor | +12.68 | INFO,RLM | 21 | ❌ L | -1.00 |
| 2026-10-28 | LAL @ LAC | Spread | LAL -4.5 | -4.5 | +1.5 | ▼ en contra | -6.00 | INFO,RLM | 68 | ✅ W | +0.91 |
| 2026-10-28 | LAL @ LAC | Total | Under 229.5 | 229.5 | 224.5 | ▲ a favor | +5.00 | INFO,RLM | 12 | ✅ W | +0.91 |
| 2026-10-28 | OKC @ DAL | ML | OKC ML | 65.7% | 63.1% | ▼ en contra | -2.65 | RLM | 89 | ❌ L | -1.00 |
| 2026-10-28 | OKC @ DAL | Spread | OKC -5.5 | -5.5 | -5.5 | = sin mov. | -0.00 | — | 61 | ❌ L | -1.00 |
| 2026-10-28 | OKC @ DAL | Total | Under 227.5 | 227.5 | 228.5 | ▼ en contra | -1.00 | — | 19 | ✅ W | +0.95 |
| 2026-10-28 | SA @ UTAH | ML | UTAH ML | 16.8% | 15.3% | ▼ en contra | -1.49 | — | 4 | ❌ L | -1.00 |
| 2026-10-28 | SA @ UTAH | Spread | SA -13.5 | -13.5 | -13.5 | = sin mov. | -0.00 | INFO,STEAM | 57 | ❌ L | -1.00 |
| 2026-10-28 | SA @ UTAH | Total | Under 233.5 | 233.5 | 232.5 | ▲ a favor | +1.00 | RLM | 14 | ✅ W | +0.89 |
| 2026-10-28 | DEN @ NO | ML | NO ML | 37.8% | 38.4% | ▲ a favor | +0.60 | RLM | 10 | ❌ L | -1.00 |
| 2026-10-28 | DEN @ NO | Spread | NO +4.5 | +4.5 | +4.5 | = sin mov. | +0.00 | — | 35 | ❌ L | -1.00 |
| 2026-10-28 | DEN @ NO | Total | Under 241.5 | 241.5 | 240.5 | ▲ a favor | +1.00 | — | 19 | ✅ W | +0.87 |
| 2026-10-28 | GS @ MIN | ML | GS ML | 39.6% | 39.6% | = sin mov. | -0.00 | — | 24 | ✅ W | +1.42 |
| 2026-10-28 | GS @ MIN | Spread | MIN -3.5 | -3.5 | -4.5 | ▲ a favor | +1.00 | STEAM | 60 | ❌ L | -1.00 |
| 2026-10-28 | GS @ MIN | Total | Under 227.5 | 227.5 | 227.5 | = sin mov. | -0.00 | — | 9 | ❌ L | -1.00 |
| 2026-10-28 | HOU @ MIL | ML | HOU ML | 74.1% | 74.1% | = sin mov. | -0.00 | — | 94 | ✅ W | +0.29 |
| 2026-10-28 | HOU @ MIL | Spread | HOU -8.5 | -8.5 | -8.5 | = sin mov. | -0.00 | — | 71 | ✅ W | +0.95 |
| 2026-10-28 | HOU @ MIL | Total | Over 226.5 | 226.5 | 226.5 | = sin mov. | +0.00 | — | 91 | ✅ W | +0.95 |
| 2026-10-28 | NY @ CHI | ML | NY ML | 70.5% | 70.5% | = sin mov. | -0.00 | — | 92 | ✅ W | +0.36 |
| 2026-10-28 | NY @ CHI | Spread | NY -6.5 | -6.5 | -6.5 | = sin mov. | -0.00 | INFO | 74 | ❌ L | -1.00 |
| 2026-10-28 | NY @ CHI | Total | Under 232.5 | 232.5 | 232.5 | = sin mov. | -0.00 | — | 19 | ❌ L | -1.00 |
| 2026-10-28 | ORL @ TOR | ML | ORL ML | 36.9% | 36.9% | = sin mov. | -0.00 | — | 14 | ❌ L | -1.00 |
| 2026-10-28 | ORL @ TOR | Spread | TOR -4.5 | -4.5 | -5.5 | ▲ a favor | +1.00 | STEAM | 72 | ✅ W | +0.91 |
| 2026-10-28 | ORL @ TOR | Total | Under 223.5 | 223.5 | 224.5 | ▼ en contra | -1.00 | — | 16 | ❌ L | -1.00 |
| 2026-10-28 | CHA @ DET | ML | CHA ML | 28.6% | 28.6% | = sin mov. | -0.00 | — | 7 | ❌ L | -1.00 |
| 2026-10-28 | CHA @ DET | Spread | CHA +7.5 | +7.5 | +7.5 | = sin mov. | -0.00 | — | 42 | ❌ L | -1.00 |
| 2026-10-28 | CHA @ DET | Total | Over 212.5 | 212.5 | 212.5 | = sin mov. | +0.00 | — | 87 | ❌ L | -1.00 |
| 2026-10-28 | MIA @ ATL | ML | ATL ML | 55.1% | 56.3% | ▲ a favor | +1.21 | — | 62 | ❌ L | -1.00 |
| 2026-10-28 | MIA @ ATL | Spread | ATL -1.5 | -1.5 | -2.5 | ▲ a favor | +1.00 | STEAM | 46 | ❌ L | -1.00 |
| 2026-10-28 | MIA @ ATL | Total | Under 241.5 | 241.5 | 243.5 | ▼ en contra | -2.00 | — | 24 | ❌ L | -1.00 |
| 2026-10-28 | PHI @ IND | ML | IND ML | 29.5% | 29.5% | = sin mov. | +0.00 | — | 10 | ❌ L | -1.00 |
| 2026-10-28 | PHI @ IND | Spread | IND +7.5 | +7.5 | +7.5 | = sin mov. | +0.00 | — | 31 | ✅ W | +0.95 |
| 2026-10-28 | PHI @ IND | Total | Under 234.5 | 234.5 | 234.5 | = sin mov. | -0.00 | — | 23 | ✅ W | +0.93 |
| 2026-10-28 | WSH @ CLE | ML | CLE ML | 76.6% | 76.6% | = sin mov. | +0.00 | — | 93 | ✅ W | +0.25 |
| 2026-10-28 | WSH @ CLE | Spread | CLE -10.5 | -10.5 | -9.5 | ▼ en contra | -1.00 | STEAM | 64 | ❌ L | -1.00 |
| 2026-10-28 | WSH @ CLE | Total | Under 239.5 | 239.5 | 240.5 | ▼ en contra | -1.00 | — | 20 | ✅ W | +0.87 |
| 2026-10-27 | POR @ LAL | ML | LAL ML | 53.2% | 51.1% | ▼ en contra | -2.16 | RLM | 77 | ❌ L | -1.00 |
| 2026-10-27 | POR @ LAL | Spread | POR +1.5 | +1.5 | +1.5 | = sin mov. | -0.00 | — | 37 | ✅ W | +0.95 |
| 2026-10-27 | POR @ LAL | Total | Under 233.5 | 233.5 | 234.5 | ▼ en contra | -1.00 | RLM | 14 | ❌ L | -1.00 |
| 2026-10-27 | DET @ NY | ML | DET ML | 39.6% | 39.1% | ▼ en contra | -0.55 | — | 36 | ❌ L | -1.00 |
| 2026-10-27 | DET @ NY | Spread | DET +4.5 | +4.5 | +4.5 | = sin mov. | -0.00 | INFO,STEAM | 74 | ❌ L | -1.00 |
| 2026-10-27 | DET @ NY | Total | Under 219.5 | 219.5 | 220.5 | ▼ en contra | -1.00 | — | 21 | ✅ W | +0.89 |
| 2026-10-27 | SAC @ SA | ML | SAC ML | 8.8% | 8.8% | = sin mov. | -0.00 | — | 7 | ❌ L | -1.00 |
| 2026-10-27 | SAC @ SA | Spread | SAC +18.5 | +18.5 | +19.5 | ▼ en contra | -1.00 | STEAM | 47 | ❌ L | -1.00 |
| 2026-10-27 | SAC @ SA | Total | Under 232.5 | 232.5 | 232.5 | = sin mov. | -0.00 | — | 23 | ❌ L | -1.00 |
| 2026-10-27 | BKN @ BOS | ML | BOS ML | 82.7% | 84.7% | ▲ a favor | +1.94 | — | 95 | ✅ W | +0.16 |
| 2026-10-27 | BKN @ BOS | Spread | BOS -12.5 | -12.5 | -13.5 | ▲ a favor | +1.00 | STEAM | 75 | ❌ L | -1.00 |
| 2026-10-27 | BKN @ BOS | Total | Over 222.5 | 222.5 | 223.5 | ▲ a favor | +1.00 | — | 89 | ✅ W | +0.91 |
| 2026-10-26 | GS @ DEN | ML | GS ML | 30.0% | 30.0% | = sin mov. | -0.00 | — | 9 | ✅ W | +2.20 |
| 2026-10-26 | GS @ DEN | Spread | GS +7.5 | +7.5 | +7.5 | = sin mov. | -0.00 | — | 43 | ✅ W | +0.87 |
| 2026-10-26 | GS @ DEN | Total | Under 236.5 | 236.5 | 236.5 | = sin mov. | -0.00 | — | 19 | ❌ L | -1.00 |
| 2026-10-26 | MEM @ UTAH | ML | MEM ML | 50.0% | 50.4% | = sin mov. | +0.43 | — | 51 | ✅ W | +0.91 |
| 2026-10-26 | MEM @ UTAH | Spread | UTAH +1.5 | +1.5 | +1.5 | = sin mov. | +0.00 | INFO | 46 | ❌ L | -1.00 |
| 2026-10-26 | MEM @ UTAH | Total | Over 237.5 | 237.5 | 237.5 | = sin mov. | +0.00 | — | 85 | ❌ L | -1.00 |
| 2026-10-26 | ATL @ HOU | ML | ATL ML | 35.5% | 36.9% | ▲ a favor | +1.38 | RLM | 10 | ❌ L | -1.00 |
| 2026-10-26 | ATL @ HOU | Spread | ATL +4.5 | +4.5 | +4.5 | = sin mov. | -0.00 | — | 33 | ❌ L | -1.00 |
| 2026-10-26 | ATL @ HOU | Total | Under 229.5 | 229.5 | 228.5 | ▲ a favor | +1.00 | RLM | 16 | ❌ L | -1.00 |
| 2026-10-26 | IND @ MIL | ML | IND ML | 61.6% | 58.3% | ▼ en contra | -3.34 | GRADUAL,RLM | 82 | ❌ L | -1.00 |
| 2026-10-26 | IND @ MIL | Spread | IND -4.5 | -4.5 | -3.5 | ▼ en contra | -1.00 | INFO | 54 | ❌ L | -1.00 |
| 2026-10-26 | IND @ MIL | Total | Over 238.5 | 238.5 | 239.5 | ▲ a favor | +1.00 | — | 75 | ❌ L | -1.00 |
| 2026-10-26 | PHX @ OKC | ML | OKC ML | 77.2% | 73.4% | ▼ en contra | -3.80 | INFO,RLM | 95 | ✅ W | +0.24 |
| 2026-10-26 | PHX @ OKC | Spread | OKC -10.5 | -10.5 | -8.5 | ▼ en contra | -2.00 | INFO,RLM | 56 | ✅ W | +0.91 |
| 2026-10-26 | PHX @ OKC | Total | Under 220.5 | 220.5 | 221.5 | ▼ en contra | -1.00 | — | 16 | ❌ L | -1.00 |
| 2026-10-26 | CHI @ BOS | ML | CHI ML | 15.3% | 15.3% | = sin mov. | -0.00 | — | 6 | ❌ L | -1.00 |
| 2026-10-26 | CHI @ BOS | Spread | CHI +14.5 | +14.5 | +14.5 | = sin mov. | -0.00 | STEAM | 58 | ❌ L | -1.00 |
| 2026-10-26 | CHI @ BOS | Total | Under 231.5 | 231.5 | 233.5 | ▼ en contra | -2.00 | STEAM | 28 | ❌ L | -1.00 |
| 2026-10-26 | DAL @ MIA | ML | DAL ML | 28.2% | 29.0% | ▲ a favor | +0.84 | GRADUAL | 10 | ✅ W | +2.40 |
| 2026-10-26 | DAL @ MIA | Spread | DAL +8.5 | +8.5 | +7.5 | ▲ a favor | +1.00 | STEAM | 65 | ✅ W | +0.87 |
| 2026-10-26 | DAL @ MIA | Total | Under 240.5 | 240.5 | 240.5 | = sin mov. | -0.00 | — | 45 | ✅ W | +0.91 |
| 2026-10-26 | MIN @ CLE | ML | MIN ML | 38.4% | 41.7% | ▲ a favor | +3.34 | GRADUAL,STEAM | 47 | ❌ L | -1.00 |
| 2026-10-26 | MIN @ CLE | Spread | MIN +4.5 | +4.5 | +3.5 | ▲ a favor | +1.00 | INFO,RLM,STEAM | 75 | ✅ W | +0.87 |
| 2026-10-26 | MIN @ CLE | Total | Under 233.5 | 233.5 | 234.5 | ▼ en contra | -1.00 | GRADUAL,RLM | 18 | ❌ L | -1.00 |
| 2026-10-26 | WSH @ CHA | ML | CHA ML | 55.1% | 56.3% | ▲ a favor | +1.21 | — | 63 | ✅ W | +0.74 |
| 2026-10-26 | WSH @ CHA | Spread | CHA -2.5 | -2.5 | -2.5 | = sin mov. | +0.00 | STEAM | 35 | ✅ W | +0.95 |
| 2026-10-26 | WSH @ CHA | Total | Over 227.5 | 227.5 | 225.5 | ▼ en contra | -2.00 | RLM,STEAM | 81 | ❌ L | -1.00 |
| 2026-10-25 | MEM @ SAC | ML | SAC ML | 40.7% | 40.0% | ▼ en contra | -0.63 | — | 16 | ❌ L | -1.00 |
| 2026-10-25 | MEM @ SAC | Spread | SAC +3.5 | +3.5 | +3.5 | = sin mov. | +0.00 | STEAM | 43 | ❌ L | -1.00 |
| 2026-10-25 | MEM @ SAC | Total | Under 236.5 | 236.5 | 234.5 | ▲ a favor | +2.00 | RLM,STEAM | 18 | ✅ W | +0.87 |
| 2026-10-25 | DET @ PHI | ML | DET ML | 50.4% | 53.2% | ▲ a favor | +2.81 | RLM | 36 | ✅ W | +0.89 |
| 2026-10-25 | DET @ PHI | Spread | DET -1.5 | -1.5 | -1.5 | = sin mov. | -0.00 | INFO,STEAM | 49 | ✅ W | +0.98 |
| 2026-10-25 | DET @ PHI | Total | Under 228.5 | 228.5 | 228.5 | = sin mov. | -0.00 | — | 15 | ✅ W | +0.89 |
| 2026-10-25 | LAC @ OKC | ML | LAC ML | 13.2% | 10.7% | ▼ en contra | -2.57 | — | 4 | ❌ L | -1.00 |
| 2026-10-25 | LAC @ OKC | Spread | LAC +14.5 | +14.5 | +16.5 | ▼ en contra | -2.00 | STEAM | 48 | ✅ W | +0.95 |
| 2026-10-25 | LAC @ OKC | Total | Under 221.5 | 221.5 | 223.5 | ▼ en contra | -2.00 | STEAM | 10 | ✅ W | +0.91 |
| 2026-10-25 | ORL @ NY | ML | NY ML | 72.6% | 70.0% | ▼ en contra | -2.56 | RLM | 94 | ❌ L | -1.00 |
| 2026-10-25 | ORL @ NY | Spread | NY -7.5 | -7.5 | -6.5 | ▼ en contra | -1.00 | INFO | 54 | ❌ L | -1.00 |
| 2026-10-25 | ORL @ NY | Total | Under 225.5 | 225.5 | 224.5 | ▲ a favor | +1.00 | RLM | 17 | ✅ W | +0.89 |
| 2026-10-25 | TOR @ MIN | ML | TOR ML | 45.7% | 40.0% | ▼ en contra | -5.69 | INFO | 19 | ❌ L | -1.00 |
| 2026-10-25 | TOR @ MIN | Spread | TOR +2.5 | +2.5 | +3.5 | ▼ en contra | -1.00 | INFO | 40 | ❌ L | -1.00 |
| 2026-10-25 | TOR @ MIN | Total | Under 231.5 | 231.5 | 228.5 | ▲ a favor | +3.00 | GRADUAL,RLM | 14 | ✅ W | +0.91 |
| 2026-10-25 | IND @ BKN | ML | BKN ML | 33.1% | 32.5% | ▼ en contra | -0.60 | — | 11 | ❌ L | -1.00 |
| 2026-10-25 | IND @ BKN | Spread | BKN +6.5 | +6.5 | +6.5 | = sin mov. | +0.00 | INFO,RLM,STEAM | 53 | ❌ L | -1.00 |
| 2026-10-25 | IND @ BKN | Total | Under 232.5 | 232.5 | 231.5 | ▲ a favor | +1.00 | — | 18 | ❌ L | -1.00 |
| 2026-10-25 | LAL @ UTAH | ML | UTAH ML | 31.5% | 31.5% | = sin mov. | +0.00 | — | 11 | ❌ L | -1.00 |
| 2026-10-25 | LAL @ UTAH | Spread | LAL -6.5 | -6.5 | -6.5 | = sin mov. | -0.00 | — | 69 | ✅ W | +0.91 |
| 2026-10-25 | LAL @ UTAH | Total | Under 235.5 | 235.5 | 237.5 | ▼ en contra | -2.00 | — | 14 | ❌ L | -1.00 |
| 2026-10-24 | GS @ PHX | ML | GS ML | 23.4% | 22.8% | ▼ en contra | -0.56 | — | — | ❌ L | -1.00 |
| 2026-10-24 | GS @ PHX | Spread | GS +9.5 | +9.5 | +9.5 | = sin mov. | -0.00 | — | — | ✅ W | +0.91 |
| 2026-10-24 | GS @ PHX | Total | Over 221.5 | 221.5 | 221.5 | = sin mov. | +0.00 | — | — | ✅ W | +0.89 |
| 2026-10-24 | NO @ DEN | ML | NO ML | 20.4% | 20.4% | = sin mov. | -0.00 | — | — | ❌ L | -1.00 |
| 2026-10-24 | NO @ DEN | Spread | NO +11.5 | +11.5 | +11.5 | = sin mov. | -0.00 | — | — | ✅ W | +0.87 |
| 2026-10-24 | NO @ DEN | Total | Under 239.5 | 239.5 | 239.5 | = sin mov. | -0.00 | — | — | ❌ L | -1.00 |
| 2026-10-24 | HOU @ ATL | ML | HOU ML | 50.4% | 50.4% | = sin mov. | -0.00 | — | — | ✅ W | +0.89 |
| 2026-10-24 | HOU @ ATL | Spread | HOU -1.5 | -1.5 | -1.5 | = sin mov. | -0.00 | — | — | ✅ W | +0.98 |
| 2026-10-24 | HOU @ ATL | Total | Under 227.5 | 227.5 | 227.5 | = sin mov. | -0.00 | — | — | ❌ L | -1.00 |
| 2026-10-24 | SA @ DAL | ML | DAL ML | 13.7% | 13.7% | = sin mov. | +0.00 | — | — | ❌ L | -1.00 |
| 2026-10-24 | SA @ DAL | Spread | DAL +14.5 | +14.5 | +14.5 | = sin mov. | +0.00 | — | — | ❌ L | -1.00 |
| 2026-10-24 | SA @ DAL | Total | Under 229.5 | 229.5 | 229.5 | = sin mov. | -0.00 | — | — | ✅ W | +0.91 |
| 2026-10-24 | WSH @ CHI | ML | CHI ML | 54.3% | 53.2% | ▼ en contra | -1.03 | — | — | ❌ L | -1.00 |
| 2026-10-24 | WSH @ CHI | Spread | CHI -2.5 | -2.5 | -1.5 | ▼ en contra | -1.00 | — | — | ❌ L | -1.00 |
| 2026-10-24 | WSH @ CHI | Total | Under 244.5 | 244.5 | 244.5 | = sin mov. | -0.00 | — | — | ✅ W | +0.91 |
| 2026-10-24 | BKN @ CLE | ML | BKN ML | 20.0% | 20.0% | = sin mov. | -0.00 | — | — | ❌ L | -1.00 |
| 2026-10-24 | BKN @ CLE | Spread | BKN +11.5 | +11.5 | +11.5 | = sin mov. | -0.00 | — | — | ✅ W | +0.89 |
| 2026-10-24 | BKN @ CLE | Total | Under 228.5 | 228.5 | 228.5 | = sin mov. | -0.00 | — | — | ❌ L | -1.00 |
| 2026-10-24 | MIL @ PHI | ML | MIL ML | 17.3% | 16.8% | = sin mov. | -0.45 | — | — | ❌ L | -1.00 |
| 2026-10-24 | MIL @ PHI | Spread | MIL +12.5 | +12.5 | +12.5 | = sin mov. | -0.00 | — | — | ✅ W | +0.89 |
| 2026-10-24 | MIL @ PHI | Total | Under 234.5 | 234.5 | 234.5 | = sin mov. | -0.00 | — | — | ❌ L | -1.00 |
| 2026-10-24 | MIA @ CHA | ML | CHA ML | 40.7% | 38.4% | ▼ en contra | -2.31 | — | — | ✅ W | +1.36 |
| 2026-10-24 | MIA @ CHA | Spread | CHA +4.5 | +4.5 | +4.5 | = sin mov. | +0.00 | — | — | ✅ W | +0.87 |
| 2026-10-24 | MIA @ CHA | Total | Under 228.5 | 228.5 | 227.5 | ▲ a favor | +1.00 | — | — | ✅ W | +0.87 |
| 2026-10-23 | LAC @ LAL | ML | LAC ML | 24.9% | 24.9% | = sin mov. | -0.00 | — | — | ❌ L | -1.00 |
| 2026-10-23 | LAC @ LAL | Spread | LAC +8.5 | +8.5 | +8.5 | = sin mov. | -0.00 | — | — | ✅ W | +0.93 |
| 2026-10-23 | LAC @ LAL | Total | Under 225.5 | 225.5 | 225.5 | = sin mov. | -0.00 | — | — | ❌ L | -1.00 |
| 2026-10-23 | MEM @ GS | ML | GS ML | 59.3% | 59.3% | = sin mov. | +0.00 | — | — | ❌ L | -1.00 |
| 2026-10-23 | MEM @ GS | Spread | GS -3.5 | -3.5 | -4.5 | ▲ a favor | +1.00 | — | — | ❌ L | -1.00 |
| 2026-10-23 | MEM @ GS | Total | Under 236.5 | 236.5 | 236.5 | = sin mov. | -0.00 | — | — | ✅ W | +0.93 |
| 2026-10-23 | POR @ SAC | ML | POR ML | 79.1% | 79.1% | = sin mov. | -0.00 | — | — | ✅ W | +0.21 |
| 2026-10-23 | POR @ SAC | Spread | POR -9.5 | -9.5 | -9.5 | = sin mov. | -0.00 | — | — | ❌ L | -1.00 |
| 2026-10-23 | POR @ SAC | Total | Under 231.5 | 231.5 | 231.5 | = sin mov. | -0.00 | — | — | ❌ L | -1.00 |
| 2026-10-23 | HOU @ SA | ML | HOU ML | 36.9% | 37.8% | ▲ a favor | +0.85 | — | — | ✅ W | +1.60 |
| 2026-10-23 | HOU @ SA | Spread | SA -4.5 | -4.5 | -4.5 | = sin mov. | +0.00 | — | — | ❌ L | -1.00 |
| 2026-10-23 | HOU @ SA | Total | Over 224.5 | 224.5 | 224.5 | = sin mov. | +0.00 | — | — | ❌ L | -1.00 |
| 2026-10-23 | NO @ UTAH | ML | NO ML | 49.6% | 49.6% | = sin mov. | -0.00 | — | — | ❌ L | -1.00 |
| 2026-10-23 | NO @ UTAH | Spread | NO +1.5 | +1.5 | +1.5 | = sin mov. | -0.00 | — | — | ✅ W | +0.85 |
| 2026-10-23 | NO @ UTAH | Total | Under 238.5 | 238.5 | 238.5 | = sin mov. | -0.00 | — | — | ❌ L | -1.00 |
| 2026-10-23 | DET @ MIA | ML | DET ML | 53.2% | 54.3% | ▲ a favor | +1.03 | — | — | ✅ W | +0.80 |
| 2026-10-23 | DET @ MIA | Spread | DET -1.5 | -1.5 | -2.5 | ▲ a favor | +1.00 | — | — | ✅ W | +0.87 |
| 2026-10-23 | DET @ MIA | Total | Under 234.5 | 234.5 | 235.5 | ▼ en contra | -1.00 | — | — | ❌ L | -1.00 |
| 2026-10-23 | ATL @ CHA | ML | CHA ML | 43.7% | 43.7% | = sin mov. | +0.00 | — | — | ❌ L | -1.00 |
| 2026-10-23 | ATL @ CHA | Spread | CHA +2.5 | +2.5 | +2.5 | = sin mov. | +0.00 | — | — | ❌ L | -1.00 |
| 2026-10-23 | ATL @ CHA | Total | Under 226.5 | 226.5 | 226.5 | = sin mov. | -0.00 | — | — | ✅ W | +0.91 |
| 2026-10-23 | DAL @ IND | ML | IND ML | 69.6% | 69.6% | = sin mov. | +0.00 | — | — | ❌ L | -1.00 |
| 2026-10-23 | DAL @ IND | Spread | IND -7.5 | -7.5 | -7.5 | = sin mov. | +0.00 | — | — | ❌ L | -1.00 |
| 2026-10-23 | DAL @ IND | Total | Over 239.5 | 239.5 | 241.5 | ▲ a favor | +2.00 | — | — | ❌ L | -1.00 |
| 2026-10-23 | MIN @ ORL | ML | ORL ML | 51.7% | 52.6% | ▲ a favor | +0.87 | — | — | ❌ L | -1.00 |
| 2026-10-23 | MIN @ ORL | Spread | ORL -1.5 | -1.5 | -1.5 | = sin mov. | +0.00 | — | — | ❌ L | -1.00 |
| 2026-10-23 | MIN @ ORL | Total | Under 234.5 | 234.5 | 234.5 | = sin mov. | -0.00 | — | — | ✅ W | +0.89 |
| 2026-10-23 | NY @ BOS | ML | NY ML | 43.7% | 42.8% | ▼ en contra | -0.86 | — | — | ❌ L | -1.00 |
| 2026-10-23 | NY @ BOS | Spread | NY +2.5 | +2.5 | +2.5 | = sin mov. | -0.00 | — | — | ❌ L | -1.00 |
| 2026-10-23 | NY @ BOS | Total | Over 220.5 | 220.5 | 220.5 | = sin mov. | +0.00 | — | — | ❌ L | -1.00 |
| 2026-10-23 | TOR @ WSH | ML | TOR ML | 74.1% | 74.1% | = sin mov. | -0.00 | — | — | ✅ W | +0.29 |
| 2026-10-23 | TOR @ WSH | Spread | TOR -9.5 | -9.5 | -9.5 | = sin mov. | -0.00 | — | — | ✅ W | +0.98 |
| 2026-10-23 | TOR @ WSH | Total | Under 236.5 | 236.5 | 236.5 | = sin mov. | -0.00 | — | — | ✅ W | +0.89 |
