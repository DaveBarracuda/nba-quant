# Ledger de picks — workflow de GitHub
_Actualizado: 2026-10-27 17:50 UTC · un pick por partido y mercado (primer snapshot del modelo, con la línea de DraftKings del NBA Odds Tracker (o de ESPN si el partido no está en el tracker) en ese momento)._

Generado por el workflow *Ejecutar modelo* (modelo sin mezcla). El cierre y el movimiento a favor / en contra se toman al liquidar de la misma fuente que la línea del pick. Ledger de la PC local: [../LEDGER.md](../LEDGER.md)

**Mercado vs modelo:** ▲ *a favor* = la línea de cierre se movió hacia el número del modelo (CLV positivo); ▼ *en contra* = se alejó; umbral 0.25 pts en spread/total y 0.5 pp de probabilidad en ML. CLV en puntos (spread/total) o en pp de probabilidad sin vig (ML). Spread y total se califican contra la línea del pick a −110; ML al precio del pick.

## Récord

| Grupo | Valor | Picks | Calificados | Récord | WR | Unidades | ROI | CLV medio |
|---|---|---|---|---|---|---|---|---|
| GENERAL | todos | 105 | 105 | 44-61-0 | 41.9% | -19.52 | -18.6% | -0.030 |
| mercado | ml | 35 | 35 | 12-23-0 | 34.3% | -10.45 | -29.9% | -0.003 |
| mercado | spread | 35 | 35 | 18-17-0 | 51.4% | -0.65 | -1.9% | -0.114 |
| mercado | total | 35 | 35 | 14-21-0 | 40.0% | -8.42 | -24.0% | +0.029 |
| movimiento | a favor | 20 | 20 | 12-8-0 | 60.0% | +4.58 | +22.9% | +0.806 |
| movimiento | en contra | 24 | 24 | 5-19-0 | 20.8% | -14.63 | -60.9% | -0.802 |
| movimiento | sin movimiento | 61 | 61 | 27-34-0 | 44.3% | -9.48 | -15.5% | -0.000 |
| mercado × movimiento | ml · a favor | 8 | 8 | 5-3-0 | 62.5% | +3.43 | +42.9% | +0.015 |
| mercado × movimiento | ml · en contra | 11 | 11 | 2-9-0 | 18.2% | -7.40 | -67.2% | -0.022 |
| mercado × movimiento | ml · sin movimiento | 16 | 16 | 5-11-0 | 31.2% | -6.49 | -40.6% | -0.000 |
| mercado × movimiento | spread · a favor | 4 | 4 | 3-1-0 | 75.0% | +1.61 | +40.2% | +1.000 |
| mercado × movimiento | spread · en contra | 6 | 6 | 2-4-0 | 33.3% | -2.14 | -35.6% | -1.333 |
| mercado × movimiento | spread · sin movimiento | 25 | 25 | 13-12-0 | 52.0% | -0.12 | -0.5% | +0.000 |
| mercado × movimiento | total · a favor | 8 | 8 | 4-4-0 | 50.0% | -0.46 | -5.7% | +1.500 |
| mercado × movimiento | total · en contra | 7 | 7 | 1-6-0 | 14.3% | -5.09 | -72.7% | -1.571 |
| mercado × movimiento | total · sin movimiento | 20 | 20 | 9-11-0 | 45.0% | -2.87 | -14.3% | +0.000 |

## CLV y movimiento del mercado hacia el modelo

_% hacia el modelo = picks en que la línea se movió a favor ÷ picks con movimiento (sin contar "sin movimiento"); 50% es lo esperado por azar y `p (azar)` es la probabilidad de ver ese % o más si la línea se moviera al azar. CLV medio por pick con cierre conocido, con su intervalo de confianza del 95%: si el intervalo no incluye 0, el CLV es distinguible del azar._

| Mercado | Con cierre | ▲ a favor | ▼ en contra | % hacia el modelo | p (azar) | CLV medio | IC 95% |
|---|---|---|---|---|---|---|---|
| Spread | 35 | 4 | 6 | 40.0% | 0.828 | -0.11 pts | [-0.34, +0.11] |
| Total | 35 | 8 | 7 | 53.3% | 0.500 | +0.03 pts | [-0.34, +0.39] |
| ML | 35 | 8 | 11 | 42.1% | 0.820 | -0.33 pp | [-0.90, +0.24] |
| **Todos** | 105 | 20 | 24 | 45.5% | 0.774 | — | — |

## Picks

| Fecha | Partido | Mercado | Pick | Línea pick | Cierre | Mercado vs modelo | CLV | Alertas | % público en pick | Resultado | Unidades |
|---|---|---|---|---|---|---|---|---|---|---|---|
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
