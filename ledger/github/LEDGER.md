# Ledger de picks — workflow de GitHub
_Actualizado: 2026-10-25 03:00 UTC · un pick por partido y mercado (primer snapshot del modelo, con la línea de DraftKings del NBA Odds Tracker (o de ESPN si el partido no está en el tracker) en ese momento)._

Generado por el workflow *Ejecutar modelo* (modelo sin mezcla). El cierre y el movimiento a favor / en contra se toman al liquidar de la misma fuente que la línea del pick. Ledger de la PC local: [../LEDGER.md](../LEDGER.md)

**Mercado vs modelo:** ▲ *a favor* = la línea de cierre se movió hacia el número del modelo (CLV positivo); ▼ *en contra* = se alejó; umbral 0.25 pts en spread/total y 0.5 pp de probabilidad en ML. CLV en puntos (spread/total) o en pp de probabilidad sin vig (ML). Spread y total se califican contra la línea del pick a −110; ML al precio del pick.

## Récord

| Grupo | Valor | Picks | Calificados | Récord | WR | Unidades | ROI | CLV medio |
|---|---|---|---|---|---|---|---|---|
| GENERAL | todos | 75 | 33 | 12-21-0 | 36.4% | -10.85 | -32.9% | +0.091 |
| mercado | ml | 25 | 11 | 4-7-0 | 36.4% | -4.09 | -37.2% | +0.002 |
| mercado | spread | 25 | 11 | 4-7-0 | 36.4% | -3.38 | -30.7% | +0.182 |
| mercado | total | 25 | 11 | 4-7-0 | 36.4% | -3.38 | -30.7% | +0.091 |
| movimiento | a favor | 6 | 6 | 3-3-0 | 50.0% | +0.27 | +4.5% | +0.671 |
| movimiento | en contra | 2 | 2 | 0-2-0 | 0.0% | -2.00 | -100.0% | -0.504 |
| movimiento | pendiente | 42 | 0 | 0-0-0 | — | +0.00 | — | — |
| movimiento | sin movimiento | 25 | 25 | 9-16-0 | 36.0% | -9.12 | -36.5% | -0.000 |
| mercado × movimiento | ml · a favor | 3 | 3 | 2-1-0 | 66.7% | +1.40 | +46.7% | +0.009 |
| mercado × movimiento | ml · en contra | 1 | 1 | 0-1-0 | 0.0% | -1.00 | -100.0% | -0.009 |
| mercado × movimiento | ml · pendiente | 14 | 0 | 0-0-0 | — | +0.00 | — | — |
| mercado × movimiento | ml · sin movimiento | 7 | 7 | 2-5-0 | 28.6% | -4.49 | -64.2% | -0.000 |
| mercado × movimiento | spread · a favor | 2 | 2 | 1-1-0 | 50.0% | -0.13 | -6.5% | +1.000 |
| mercado × movimiento | spread · pendiente | 14 | 0 | 0-0-0 | — | +0.00 | — | — |
| mercado × movimiento | spread · sin movimiento | 9 | 9 | 3-6-0 | 33.3% | -3.25 | -36.1% | +0.000 |
| mercado × movimiento | total · a favor | 1 | 1 | 0-1-0 | 0.0% | -1.00 | -100.0% | +2.000 |
| mercado × movimiento | total · en contra | 1 | 1 | 0-1-0 | 0.0% | -1.00 | -100.0% | -1.000 |
| mercado × movimiento | total · pendiente | 14 | 0 | 0-0-0 | — | +0.00 | — | — |
| mercado × movimiento | total · sin movimiento | 9 | 9 | 4-5-0 | 44.4% | -1.38 | -15.3% | +0.000 |

## CLV y movimiento del mercado hacia el modelo

_% hacia el modelo = picks en que la línea se movió a favor ÷ picks con movimiento (sin contar "sin movimiento"); 50% es lo esperado por azar y `p (azar)` es la probabilidad de ver ese % o más si la línea se moviera al azar. CLV medio por pick con cierre conocido, con su intervalo de confianza del 95%: si el intervalo no incluye 0, el CLV es distinguible del azar._

| Mercado | Con cierre | ▲ a favor | ▼ en contra | % hacia el modelo | p (azar) | CLV medio | IC 95% |
|---|---|---|---|---|---|---|---|
| Spread | 11 | 2 | 0 | 100.0% | 0.250 | +0.18 pts | [-0.06, +0.42] |
| Total | 11 | 1 | 1 | 50.0% | 0.750 | +0.09 pts | [-0.32, +0.50] |
| ML | 11 | 3 | 1 | 75.0% | 0.312 | +0.17 pp | [-0.15, +0.49] |
| **Todos** | 33 | 6 | 2 | 75.0% | 0.145 | — | — |

## Picks

| Fecha | Partido | Mercado | Pick | Línea pick | Cierre | Mercado vs modelo | CLV | Alertas | % público en pick | Resultado | Unidades |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-10-25 | MEM @ SAC | ML | SAC ML | 40.7% | — | … pendiente | — | — | 0 | pendiente | — |
| 2026-10-25 | MEM @ SAC | Spread | SAC +3.5 | +3.5 | — | … pendiente | — | — | 0 | pendiente | — |
| 2026-10-25 | MEM @ SAC | Total | Under 236.5 | 236.5 | — | … pendiente | — | — | 100 | pendiente | — |
| 2026-10-25 | LAC @ OKC | ML | LAC ML | 13.2% | — | … pendiente | — | — | 100 | pendiente | — |
| 2026-10-25 | LAC @ OKC | Spread | LAC +14.5 | +14.5 | — | … pendiente | — | — | 100 | pendiente | — |
| 2026-10-25 | LAC @ OKC | Total | Under 221.5 | 221.5 | — | … pendiente | — | — | 100 | pendiente | — |
| 2026-10-25 | ORL @ NY | ML | NY ML | 72.6% | — | … pendiente | — | — | 0 | pendiente | — |
| 2026-10-25 | ORL @ NY | Spread | NY -7.5 | -7.5 | — | … pendiente | — | — | 0 | pendiente | — |
| 2026-10-25 | ORL @ NY | Total | Under 225.5 | 225.5 | — | … pendiente | — | — | 100 | pendiente | — |
| 2026-10-25 | TOR @ MIN | ML | TOR ML | 45.7% | — | … pendiente | — | — | 100 | pendiente | — |
| 2026-10-25 | TOR @ MIN | Spread | TOR +2.5 | +2.5 | — | … pendiente | — | — | 100 | pendiente | — |
| 2026-10-25 | TOR @ MIN | Total | Under 231.5 | 231.5 | — | … pendiente | — | — | 100 | pendiente | — |
| 2026-10-25 | IND @ BKN | ML | BKN ML | 33.1% | — | … pendiente | — | — | 0 | pendiente | — |
| 2026-10-25 | IND @ BKN | Spread | BKN +6.5 | +6.5 | — | … pendiente | — | — | 0 | pendiente | — |
| 2026-10-25 | IND @ BKN | Total | Under 232.5 | 232.5 | — | … pendiente | — | — | 100 | pendiente | — |
| 2026-10-25 | LAL @ UTAH | ML | UTAH ML | 31.5% | — | … pendiente | — | — | 0 | pendiente | — |
| 2026-10-25 | LAL @ UTAH | Spread | LAL -6.5 | -6.5 | — | … pendiente | — | — | 100 | pendiente | — |
| 2026-10-25 | LAL @ UTAH | Total | Under 235.5 | 235.5 | — | … pendiente | — | — | 100 | pendiente | — |
| 2026-10-24 | GS @ PHX | ML | GS ML | 23.4% | — | … pendiente | — | — | — | pendiente | — |
| 2026-10-24 | GS @ PHX | Spread | GS +9.5 | +9.5 | — | … pendiente | — | — | — | pendiente | — |
| 2026-10-24 | GS @ PHX | Total | Over 221.5 | 221.5 | — | … pendiente | — | — | — | pendiente | — |
| 2026-10-24 | NO @ DEN | ML | NO ML | 20.4% | — | … pendiente | — | — | — | pendiente | — |
| 2026-10-24 | NO @ DEN | Spread | NO +11.5 | +11.5 | — | … pendiente | — | — | — | pendiente | — |
| 2026-10-24 | NO @ DEN | Total | Under 239.5 | 239.5 | — | … pendiente | — | — | — | pendiente | — |
| 2026-10-24 | HOU @ ATL | ML | HOU ML | 50.4% | — | … pendiente | — | — | — | pendiente | — |
| 2026-10-24 | HOU @ ATL | Spread | HOU -1.5 | -1.5 | — | … pendiente | — | — | — | pendiente | — |
| 2026-10-24 | HOU @ ATL | Total | Under 227.5 | 227.5 | — | … pendiente | — | — | — | pendiente | — |
| 2026-10-24 | SA @ DAL | ML | DAL ML | 13.7% | — | … pendiente | — | — | — | pendiente | — |
| 2026-10-24 | SA @ DAL | Spread | DAL +14.5 | +14.5 | — | … pendiente | — | — | — | pendiente | — |
| 2026-10-24 | SA @ DAL | Total | Under 229.5 | 229.5 | — | … pendiente | — | — | — | pendiente | — |
| 2026-10-24 | WSH @ CHI | ML | CHI ML | 54.3% | — | … pendiente | — | — | — | pendiente | — |
| 2026-10-24 | WSH @ CHI | Spread | CHI -2.5 | -2.5 | — | … pendiente | — | — | — | pendiente | — |
| 2026-10-24 | WSH @ CHI | Total | Under 244.5 | 244.5 | — | … pendiente | — | — | — | pendiente | — |
| 2026-10-24 | BKN @ CLE | ML | BKN ML | 20.0% | — | … pendiente | — | — | — | pendiente | — |
| 2026-10-24 | BKN @ CLE | Spread | BKN +11.5 | +11.5 | — | … pendiente | — | — | — | pendiente | — |
| 2026-10-24 | BKN @ CLE | Total | Under 228.5 | 228.5 | — | … pendiente | — | — | — | pendiente | — |
| 2026-10-24 | MIL @ PHI | ML | MIL ML | 17.3% | — | … pendiente | — | — | — | pendiente | — |
| 2026-10-24 | MIL @ PHI | Spread | MIL +12.5 | +12.5 | — | … pendiente | — | — | — | pendiente | — |
| 2026-10-24 | MIL @ PHI | Total | Under 234.5 | 234.5 | — | … pendiente | — | — | — | pendiente | — |
| 2026-10-24 | MIA @ CHA | ML | CHA ML | 40.7% | — | … pendiente | — | — | — | pendiente | — |
| 2026-10-24 | MIA @ CHA | Spread | CHA +4.5 | +4.5 | — | … pendiente | — | — | — | pendiente | — |
| 2026-10-24 | MIA @ CHA | Total | Under 228.5 | 228.5 | — | … pendiente | — | — | — | pendiente | — |
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
