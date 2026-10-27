# Ledger de picks del modelo
_Actualizado: 2026-10-27 17:50 UTC · un pick por partido y mercado (primer snapshot del modelo, con la línea del NBA Odds Tracker en ese momento)._

Picks del workflow de GitHub *Ejecutar modelo* (líneas de ESPN): [github/LEDGER.md](github/LEDGER.md)

**Mercado vs modelo:** ▲ *a favor* = la línea de cierre se movió hacia el número del modelo (CLV positivo); ▼ *en contra* = se alejó; umbral 0.25 pts en spread/total y 0.5 pp de probabilidad en ML. CLV en puntos (spread/total) o en pp de probabilidad sin vig (ML). Spread y total se califican contra la línea del pick a −110; ML al precio del pick.

## Récord

| Grupo | Valor | Picks | Calificados | Récord | WR | Unidades | ROI | CLV medio |
|---|---|---|---|---|---|---|---|---|
| GENERAL | todos | 144 | 144 | 75-69-0 | 52.1% | +2.20 | +1.5% | +0.294 |
| mercado | ml | 48 | 48 | 18-30-0 | 37.5% | -10.74 | -22.4% | +0.008 |
| mercado | spread | 48 | 48 | 28-20-0 | 58.3% | +5.61 | +11.7% | +0.292 |
| mercado | total | 48 | 48 | 29-19-0 | 60.4% | +7.33 | +15.3% | +0.583 |
| movimiento | a favor | 66 | 66 | 36-30-0 | 54.5% | +2.30 | +3.5% | +1.210 |
| movimiento | en contra | 37 | 37 | 17-20-0 | 45.9% | -2.46 | -6.7% | -1.012 |
| movimiento | sin movimiento | 41 | 41 | 22-19-0 | 53.7% | +2.36 | +5.8% | -0.000 |
| mercado × movimiento | ml · a favor | 26 | 26 | 11-15-0 | 42.3% | -5.53 | -21.3% | +0.032 |
| mercado × movimiento | ml · en contra | 15 | 15 | 6-9-0 | 40.0% | -1.56 | -10.4% | -0.030 |
| mercado × movimiento | ml · sin movimiento | 7 | 7 | 1-6-0 | 14.3% | -3.65 | -52.1% | -0.001 |
| mercado × movimiento | spread · a favor | 18 | 18 | 10-8-0 | 55.6% | +1.27 | +7.1% | +1.778 |
| mercado × movimiento | spread · en contra | 11 | 11 | 4-7-0 | 36.4% | -3.40 | -30.9% | -1.636 |
| mercado × movimiento | spread · sin movimiento | 19 | 19 | 14-5-0 | 73.7% | +7.74 | +40.7% | +0.000 |
| mercado × movimiento | total · a favor | 22 | 22 | 15-7-0 | 68.2% | +6.56 | +29.8% | +2.136 |
| mercado × movimiento | total · en contra | 11 | 11 | 7-4-0 | 63.6% | +2.49 | +22.7% | -1.727 |
| mercado × movimiento | total · sin movimiento | 15 | 15 | 7-8-0 | 46.7% | -1.73 | -11.5% | +0.000 |

## CLV y movimiento del mercado hacia el modelo

_% hacia el modelo = picks en que la línea se movió a favor ÷ picks con movimiento (sin contar "sin movimiento"); 50% es lo esperado por azar y `p (azar)` es la probabilidad de ver ese % o más si la línea se moviera al azar. CLV medio por pick con cierre conocido, con su intervalo de confianza del 95%: si el intervalo no incluye 0, el CLV es distinguible del azar._

| Mercado | Con cierre | ▲ a favor | ▼ en contra | % hacia el modelo | p (azar) | CLV medio | IC 95% |
|---|---|---|---|---|---|---|---|
| Spread | 48 | 18 | 11 | 62.1% | 0.132 | +0.29 pts | [-0.14, +0.73] |
| Total | 48 | 22 | 11 | 66.7% | 0.040 | +0.58 pts | [+0.06, +1.10] |
| ML | 48 | 26 | 15 | 63.4% | 0.059 | +0.80 pp | [-0.21, +1.80] |
| **Todos** | 144 | 66 | 37 | 64.1% | 0.003 | — | — |

## Picks

| Fecha | Partido | Mercado | Pick | Línea pick | Cierre | Mercado vs modelo | CLV | Alertas | % público en pick | Resultado | Unidades |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-10-26 | GS @ DEN | ML | GS ML | 28.6% | 28.6% | = sin mov. | -0.00 | — | 12 | ✅ W | +2.35 |
| 2026-10-26 | GS @ DEN | Spread | GS +7.5 | +7.5 | +7.5 | = sin mov. | -0.00 | STEAM | 28 | ✅ W | +0.91 |
| 2026-10-26 | GS @ DEN | Total | Under 235.5 | 235.5 | 236.5 | ▼ en contra | -1.00 | RLM,STEAM | 22 | ❌ L | -1.00 |
| 2026-10-26 | ATL @ HOU | ML | ATL ML | 34.3% | 36.3% | ▲ a favor | +2.06 | RLM | 11 | ❌ L | -1.00 |
| 2026-10-26 | ATL @ HOU | Spread | ATL +5.5 | +5.5 | +4.5 | ▲ a favor | +1.00 | RLM,STEAM | 30 | ❌ L | -1.00 |
| 2026-10-26 | ATL @ HOU | Total | Under 229.5 | 229.5 | 229.5 | = sin mov. | -0.00 | — | 15 | ❌ L | -1.00 |
| 2026-10-26 | CHI @ BOS | ML | CHI ML | 14.2% | 15.3% | ▲ a favor | +1.14 | — | 8 | ❌ L | -1.00 |
| 2026-10-26 | CHI @ BOS | Spread | CHI +13.5 | +13.5 | +14.5 | ▼ en contra | -1.00 | RLM,STEAM | 58 | ❌ L | -1.00 |
| 2026-10-26 | CHI @ BOS | Total | Under 233.5 | 233.5 | 231.5 | ▲ a favor | +2.00 | RLM | 35 | ✅ W | +0.91 |
| 2026-10-26 | DAL @ MIA | ML | DAL ML | 28.6% | 26.6% | ▼ en contra | -2.00 | — | 14 | ✅ W | +2.35 |
| 2026-10-26 | DAL @ MIA | Spread | DAL +7.5 | +7.5 | +8.5 | ▼ en contra | -1.00 | RLM,STEAM | 62 | ✅ W | +0.91 |
| 2026-10-26 | DAL @ MIA | Total | Over 235.5 | 235.5 | 239.5 | ▲ a favor | +4.00 | GRADUAL | 53 | ❌ L | -1.00 |
| 2026-10-26 | WSH @ CHA | ML | CHA ML | 56.3% | 54.3% | ▼ en contra | -2.07 | RLM | 54 | ✅ W | +0.70 |
| 2026-10-26 | WSH @ CHA | Spread | CHA -2.5 | -2.5 | -1.5 | ▼ en contra | -1.00 | STEAM | 35 | ✅ W | +0.87 |
| 2026-10-26 | WSH @ CHA | Total | Under 228.5 | 228.5 | 227.5 | ▲ a favor | +1.00 | RLM | 15 | ✅ W | +0.91 |
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
