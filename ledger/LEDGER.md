# Ledger de picks del modelo
_Actualizado: 2026-10-24 15:00 UTC · un pick por partido y mercado (primer snapshot del modelo, con la línea del NBA Odds Tracker en ese momento)._

Picks del workflow de GitHub *Ejecutar modelo* (líneas de ESPN): [github/LEDGER.md](github/LEDGER.md)

**Mercado vs modelo:** ▲ *a favor* = la línea de cierre se movió hacia el número del modelo (CLV positivo); ▼ *en contra* = se alejó; umbral 0.25 pts en spread/total y 0.5 pp de probabilidad en ML. CLV en puntos (spread/total) o en pp de probabilidad sin vig (ML). Spread y total se califican contra la línea del pick a −110; ML al precio del pick.

## Récord

| Grupo | Valor | Picks | Calificados | Récord | WR | Unidades | ROI | CLV medio |
|---|---|---|---|---|---|---|---|---|
| GENERAL | todos | 84 | 84 | 47-37-0 | 56.0% | +6.01 | +7.2% | +0.515 |
| mercado | ml | 28 | 28 | 12-16-0 | 42.9% | -5.14 | -18.4% | +0.011 |
| mercado | spread | 28 | 28 | 17-11-0 | 60.7% | +4.71 | +16.8% | +0.857 |
| mercado | total | 28 | 28 | 18-10-0 | 64.3% | +6.43 | +23.0% | +0.679 |
| movimiento | a favor | 46 | 46 | 28-18-0 | 60.9% | +7.08 | +15.4% | +1.317 |
| movimiento | en contra | 19 | 19 | 10-9-0 | 52.6% | +0.71 | +3.7% | -0.910 |
| movimiento | sin movimiento | 19 | 19 | 9-10-0 | 47.4% | -1.78 | -9.4% | +0.000 |
| mercado × movimiento | ml · a favor | 16 | 16 | 9-7-0 | 56.2% | +0.67 | +4.2% | +0.036 |
| mercado × movimiento | ml · en contra | 9 | 9 | 3-6-0 | 33.3% | -2.81 | -31.2% | -0.032 |
| mercado × movimiento | ml · sin movimiento | 3 | 3 | 0-3-0 | 0.0% | -3.00 | -100.0% | +0.000 |
| mercado × movimiento | spread · a favor | 16 | 16 | 10-6-0 | 62.5% | +3.27 | +20.4% | +1.812 |
| mercado × movimiento | spread · en contra | 2 | 2 | 1-1-0 | 50.0% | -0.05 | -2.4% | -2.500 |
| mercado × movimiento | spread · sin movimiento | 10 | 10 | 6-4-0 | 60.0% | +1.49 | +14.9% | +0.000 |
| mercado × movimiento | total · a favor | 14 | 14 | 9-5-0 | 64.3% | +3.14 | +22.4% | +2.214 |
| mercado × movimiento | total · en contra | 8 | 8 | 6-2-0 | 75.0% | +3.57 | +44.6% | -1.500 |
| mercado × movimiento | total · sin movimiento | 6 | 6 | 3-3-0 | 50.0% | -0.27 | -4.5% | +0.000 |

## CLV y movimiento del mercado hacia el modelo

_% hacia el modelo = picks en que la línea se movió a favor ÷ picks con movimiento (sin contar "sin movimiento"); 50% es lo esperado por azar y `p (azar)` es la probabilidad de ver ese % o más si la línea se moviera al azar. CLV medio por pick con cierre conocido, con su intervalo de confianza del 95%: si el intervalo no incluye 0, el CLV es distinguible del azar._

| Mercado | Con cierre | ▲ a favor | ▼ en contra | % hacia el modelo | p (azar) | CLV medio | IC 95% |
|---|---|---|---|---|---|---|---|
| Spread | 28 | 16 | 2 | 88.9% | 0.001 | +0.86 pts | [+0.27, +1.44] |
| Total | 28 | 14 | 8 | 63.6% | 0.143 | +0.68 pts | [-0.02, +1.38] |
| ML | 28 | 16 | 9 | 64.0% | 0.115 | +1.06 pp | [-0.41, +2.52] |
| **Todos** | 84 | 46 | 19 | 70.8% | 0.001 | — | — |

## Picks

| Fecha | Partido | Mercado | Pick | Línea pick | Cierre | Mercado vs modelo | CLV | Alertas | % público en pick | Resultado | Unidades |
|---|---|---|---|---|---|---|---|---|---|---|---|
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
