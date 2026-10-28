# Ledger de picks — workflow de GitHub
_Actualizado: 2026-10-28 19:11 UTC · un pick por partido y mercado (primer snapshot del modelo, con la línea de DraftKings del NBA Odds Tracker (o de ESPN si el partido no está en el tracker) en ese momento)._

Generado por el workflow *Ejecutar modelo* (modelo sin mezcla). El cierre y el movimiento a favor / en contra se toman al liquidar de la misma fuente que la línea del pick. Ledger de la PC local: [../LEDGER.md](../LEDGER.md)

**Mercado vs modelo:** ▲ *a favor* = la línea de cierre se movió hacia el número del modelo (CLV positivo); ▼ *en contra* = se alejó; umbral 0.25 pts en spread/total y 0.5 pp de probabilidad en ML. CLV en puntos (spread/total) o en pp de probabilidad sin vig (ML). Spread y total se califican contra la línea del pick a −110; ML al precio del pick.

## Récord

| Grupo | Valor | Picks | Calificados | Récord | WR | Unidades | ROI | CLV medio |
|---|---|---|---|---|---|---|---|---|
| GENERAL | todos | 153 | 117 | 48-69-0 | 41.0% | -24.61 | -21.0% | -0.035 |
| mercado | ml | 51 | 39 | 13-26-0 | 33.3% | -13.29 | -34.1% | -0.003 |
| mercado | spread | 51 | 39 | 19-20-0 | 48.7% | -2.70 | -6.9% | -0.103 |
| mercado | total | 51 | 39 | 16-23-0 | 41.0% | -8.61 | -22.1% | +0.000 |
| movimiento | a favor | 23 | 23 | 14-9-0 | 60.9% | +4.65 | +20.2% | +0.789 |
| movimiento | en contra | 29 | 29 | 6-23-0 | 20.7% | -17.73 | -61.1% | -0.768 |
| movimiento | pendiente | 36 | 0 | 0-0-0 | — | +0.00 | — | — |
| movimiento | sin movimiento | 65 | 65 | 28-37-0 | 43.1% | -11.53 | -17.7% | -0.000 |
| mercado × movimiento | ml · a favor | 9 | 9 | 6-3-0 | 66.7% | +3.59 | +39.9% | +0.016 |
| mercado × movimiento | ml · en contra | 13 | 13 | 2-11-0 | 15.4% | -9.40 | -72.3% | -0.020 |
| mercado × movimiento | ml · pendiente | 12 | 0 | 0-0-0 | — | +0.00 | — | — |
| mercado × movimiento | ml · sin movimiento | 17 | 17 | 5-12-0 | 29.4% | -7.49 | -44.1% | -0.000 |
| mercado × movimiento | spread · a favor | 5 | 5 | 3-2-0 | 60.0% | +0.61 | +12.2% | +1.000 |
| mercado × movimiento | spread · en contra | 7 | 7 | 2-5-0 | 28.6% | -3.14 | -44.8% | -1.286 |
| mercado × movimiento | spread · pendiente | 12 | 0 | 0-0-0 | — | +0.00 | — | — |
| mercado × movimiento | spread · sin movimiento | 27 | 27 | 14-13-0 | 51.9% | -0.17 | -0.6% | +0.000 |
| mercado × movimiento | total · a favor | 9 | 9 | 5-4-0 | 55.6% | +0.45 | +5.0% | +1.444 |
| mercado × movimiento | total · en contra | 9 | 9 | 2-7-0 | 22.2% | -5.20 | -57.8% | -1.444 |
| mercado × movimiento | total · pendiente | 12 | 0 | 0-0-0 | — | +0.00 | — | — |
| mercado × movimiento | total · sin movimiento | 21 | 21 | 9-12-0 | 42.9% | -3.87 | -18.4% | +0.000 |

## CLV y movimiento del mercado hacia el modelo

_% hacia el modelo = picks en que la línea se movió a favor ÷ picks con movimiento (sin contar "sin movimiento"); 50% es lo esperado por azar y `p (azar)` es la probabilidad de ver ese % o más si la línea se moviera al azar. CLV medio por pick con cierre conocido, con su intervalo de confianza del 95%: si el intervalo no incluye 0, el CLV es distinguible del azar._

| Mercado | Con cierre | ▲ a favor | ▼ en contra | % hacia el modelo | p (azar) | CLV medio | IC 95% |
|---|---|---|---|---|---|---|---|
| Spread | 39 | 5 | 7 | 41.7% | 0.806 | -0.10 pts | [-0.32, +0.11] |
| Total | 39 | 9 | 9 | 50.0% | 0.593 | +0.00 pts | [-0.34, +0.34] |
| ML | 39 | 9 | 13 | 40.9% | 0.857 | -0.32 pp | [-0.85, +0.22] |
| **Todos** | 117 | 23 | 29 | 44.2% | 0.834 | — | — |

## Picks

| Fecha | Partido | Mercado | Pick | Línea pick | Cierre | Mercado vs modelo | CLV | Alertas | % público en pick | Resultado | Unidades |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-10-28 | LAL @ LAC | ML | LAC ML | 37.8% | — | … pendiente | — | — | 9 | pendiente | — |
| 2026-10-28 | LAL @ LAC | Spread | LAL -4.5 | -4.5 | — | … pendiente | — | — | 63 | pendiente | — |
| 2026-10-28 | LAL @ LAC | Total | Under 229.5 | 229.5 | — | … pendiente | — | — | 18 | pendiente | — |
| 2026-10-28 | OKC @ DAL | ML | OKC ML | 65.7% | — | … pendiente | — | — | 88 | pendiente | — |
| 2026-10-28 | OKC @ DAL | Spread | OKC -5.5 | -5.5 | — | … pendiente | — | — | 67 | pendiente | — |
| 2026-10-28 | OKC @ DAL | Total | Under 227.5 | 227.5 | — | … pendiente | — | — | 18 | pendiente | — |
| 2026-10-28 | SA @ UTAH | ML | UTAH ML | 16.8% | — | … pendiente | — | — | 3 | pendiente | — |
| 2026-10-28 | SA @ UTAH | Spread | SA -13.5 | -13.5 | — | … pendiente | — | — | 66 | pendiente | — |
| 2026-10-28 | SA @ UTAH | Total | Under 233.5 | 233.5 | — | … pendiente | — | — | 16 | pendiente | — |
| 2026-10-28 | DEN @ NO | ML | NO ML | 37.8% | — | … pendiente | — | — | 9 | pendiente | — |
| 2026-10-28 | DEN @ NO | Spread | NO +4.5 | +4.5 | — | … pendiente | — | — | 45 | pendiente | — |
| 2026-10-28 | DEN @ NO | Total | Under 241.5 | 241.5 | — | … pendiente | — | — | 20 | pendiente | — |
| 2026-10-28 | GS @ MIN | ML | GS ML | 39.6% | — | … pendiente | — | — | 24 | pendiente | — |
| 2026-10-28 | GS @ MIN | Spread | MIN -3.5 | -3.5 | — | … pendiente | — | — | 66 | pendiente | — |
| 2026-10-28 | GS @ MIN | Total | Under 227.5 | 227.5 | — | … pendiente | — | — | 9 | pendiente | — |
| 2026-10-28 | HOU @ MIL | ML | HOU ML | 74.1% | — | … pendiente | — | — | 95 | pendiente | — |
| 2026-10-28 | HOU @ MIL | Spread | HOU -8.5 | -8.5 | — | … pendiente | — | — | 72 | pendiente | — |
| 2026-10-28 | HOU @ MIL | Total | Over 226.5 | 226.5 | — | … pendiente | — | — | 91 | pendiente | — |
| 2026-10-28 | NY @ CHI | ML | NY ML | 70.5% | — | … pendiente | — | — | 93 | pendiente | — |
| 2026-10-28 | NY @ CHI | Spread | NY -6.5 | -6.5 | — | … pendiente | — | — | 80 | pendiente | — |
| 2026-10-28 | NY @ CHI | Total | Under 232.5 | 232.5 | — | … pendiente | — | — | 21 | pendiente | — |
| 2026-10-28 | ORL @ TOR | ML | ORL ML | 36.9% | — | … pendiente | — | — | 16 | pendiente | — |
| 2026-10-28 | ORL @ TOR | Spread | TOR -4.5 | -4.5 | — | … pendiente | — | — | 74 | pendiente | — |
| 2026-10-28 | ORL @ TOR | Total | Under 223.5 | 223.5 | — | … pendiente | — | — | 12 | pendiente | — |
| 2026-10-28 | CHA @ DET | ML | CHA ML | 28.6% | — | … pendiente | — | — | 8 | pendiente | — |
| 2026-10-28 | CHA @ DET | Spread | CHA +7.5 | +7.5 | — | … pendiente | — | — | 21 | pendiente | — |
| 2026-10-28 | CHA @ DET | Total | Over 212.5 | 212.5 | — | … pendiente | — | — | 85 | pendiente | — |
| 2026-10-28 | MIA @ ATL | ML | ATL ML | 55.1% | — | … pendiente | — | — | 62 | pendiente | — |
| 2026-10-28 | MIA @ ATL | Spread | ATL -1.5 | -1.5 | — | … pendiente | — | — | 47 | pendiente | — |
| 2026-10-28 | MIA @ ATL | Total | Under 241.5 | 241.5 | — | … pendiente | — | — | 30 | pendiente | — |
| 2026-10-28 | PHI @ IND | ML | IND ML | 29.5% | — | … pendiente | — | — | 13 | pendiente | — |
| 2026-10-28 | PHI @ IND | Spread | IND +7.5 | +7.5 | — | … pendiente | — | — | 23 | pendiente | — |
| 2026-10-28 | PHI @ IND | Total | Under 234.5 | 234.5 | — | … pendiente | — | — | 24 | pendiente | — |
| 2026-10-28 | WSH @ CLE | ML | CLE ML | 76.6% | — | … pendiente | — | — | 93 | pendiente | — |
| 2026-10-28 | WSH @ CLE | Spread | CLE -10.5 | -10.5 | — | … pendiente | — | — | 70 | pendiente | — |
| 2026-10-28 | WSH @ CLE | Total | Under 239.5 | 239.5 | — | … pendiente | — | — | 23 | pendiente | — |
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
