# Ledger de picks — workflow de GitHub
_Actualizado: 2026-11-03 19:22 UTC · un pick por partido y mercado (primer snapshot del modelo, con la línea de DraftKings del NBA Odds Tracker (o de ESPN si el partido no está en el tracker) en ese momento)._

Generado por el workflow *Ejecutar modelo* (modelo sin mezcla). El cierre y el movimiento a favor / en contra se toman al liquidar de la misma fuente que la línea del pick. Ledger de la PC local: [../LEDGER.md](../LEDGER.md)

**Mercado vs modelo:** ▲ *a favor* = la línea de cierre se movió hacia el número del modelo (CLV positivo); ▼ *en contra* = se alejó; umbral 0.25 pts en spread/total y 0.5 pp de probabilidad en ML. CLV en puntos (spread/total) o en pp de probabilidad sin vig (ML). Spread y total se califican contra la línea del pick a −110; ML al precio del pick.

## Récord

| Grupo | Valor | Picks | Calificados | Récord | WR | Unidades | ROI | CLV medio |
|---|---|---|---|---|---|---|---|---|
| GENERAL | todos | 267 | 267 | 112-155-0 | 41.9% | -52.34 | -19.6% | -0.064 |
| mercado | ml | 89 | 89 | 28-61-0 | 31.5% | -34.63 | -38.9% | +0.000 |
| mercado | spread | 89 | 89 | 38-51-0 | 42.7% | -16.43 | -18.5% | -0.169 |
| mercado | total | 89 | 89 | 46-43-0 | 51.7% | -1.27 | -1.4% | -0.022 |
| movimiento | a favor | 66 | 66 | 33-33-0 | 50.0% | -0.65 | -1.0% | +0.843 |
| movimiento | en contra | 64 | 64 | 18-46-0 | 28.1% | -29.02 | -45.3% | -1.135 |
| movimiento | sin movimiento | 137 | 137 | 61-76-0 | 44.5% | -22.67 | -16.5% | +0.000 |
| mercado × movimiento | ml · a favor | 28 | 28 | 12-16-0 | 42.9% | -2.33 | -8.3% | +0.022 |
| mercado × movimiento | ml · en contra | 23 | 23 | 3-20-0 | 13.0% | -16.76 | -72.9% | -0.027 |
| mercado × movimiento | ml · sin movimiento | 38 | 38 | 13-25-0 | 34.2% | -15.54 | -40.9% | +0.000 |
| mercado × movimiento | spread · a favor | 13 | 13 | 6-7-0 | 46.2% | -1.73 | -13.3% | +1.308 |
| mercado × movimiento | spread · en contra | 18 | 18 | 6-12-0 | 33.3% | -6.57 | -36.5% | -1.778 |
| mercado × movimiento | spread · sin movimiento | 58 | 58 | 26-32-0 | 44.8% | -8.13 | -14.0% | +0.000 |
| mercado × movimiento | total · a favor | 25 | 25 | 15-10-0 | 60.0% | +3.41 | +13.6% | +1.520 |
| mercado × movimiento | total · en contra | 23 | 23 | 9-14-0 | 39.1% | -5.68 | -24.7% | -1.739 |
| mercado × movimiento | total · sin movimiento | 41 | 41 | 22-19-0 | 53.7% | +1.01 | +2.5% | +0.000 |

## CLV y movimiento del mercado hacia el modelo

_% hacia el modelo = picks en que la línea se movió a favor ÷ picks con movimiento (sin contar "sin movimiento"); 50% es lo esperado por azar y `p (azar)` es la probabilidad de ver ese % o más si la línea se moviera al azar. CLV medio por pick con cierre conocido, con su intervalo de confianza del 95%: si el intervalo no incluye 0, el CLV es distinguible del azar._

| Mercado | Con cierre | ▲ a favor | ▼ en contra | % hacia el modelo | p (azar) | CLV medio | IC 95% |
|---|---|---|---|---|---|---|---|
| Spread | 89 | 13 | 18 | 41.9% | 0.859 | -0.17 pts | [-0.41, +0.08] |
| Total | 89 | 25 | 23 | 52.1% | 0.443 | -0.02 pts | [-0.32, +0.27] |
| ML | 89 | 28 | 23 | 54.9% | 0.288 | +0.00 pp | [-0.57, +0.57] |
| **Todos** | 267 | 66 | 64 | 50.8% | 0.465 | — | — |

## Picks

| Fecha | Partido | Mercado | Pick | Línea pick | Cierre | Mercado vs modelo | CLV | Alertas | % público en pick | Resultado | Unidades |
|---|---|---|---|---|---|---|---|---|---|---|---|
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
