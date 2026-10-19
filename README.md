# NBA Quant — motor cuantitativo NBA

Pipeline de producción en Python 3.10+ que va de PBP crudo a un tear sheet de mercado:

```
ESPN (PBP + WP + cuotas + árbitros) ─┐
The Odds API / nba_api / B-Ref / Kaggle ─┤─> Data lake Parquet + DuckDB ─> NBAAdvancedFeaturePipeline (A-G)
                                       ┘        data/lake/<tabla>/season=YYYY      │
                                                                                   ▼
       Kalman (θ off/def) + Ridge (rival) ─> TeamProfile ─> Cadena de Markov por posesión
                                                                 │
   Clases 2-5 (L5, históricos, ineficiencias, dinámicos) ─> escenarios Mejor/Normal/Peor
                                                                 ▼
          Monte Carlo 7 bloques × 50k + Markov 100k ─> Shin/Power ─> RAE ─> Tear sheet
```

## Instalación y uso

```bash
pip install -e .[dev]
```

```bash
python -m nba_quant.cli ingest --start 2025-10-21 --end 2026-06-20
```

```bash
python -m nba_quant.cli simulate --date 2026-10-20 --seasons 2026
```

```bash
python -m nba_quant.cli backtest --seasons 2026
```

```bash
python -m nba_quant.cli demo
```

`demo` (o `python src/nba_quant/cli.py` sin argumentos) corre todo el pipeline sobre una liga
sintética, sin red. `NBA_QUANT_HOME` cambia la carpeta del lake (por defecto `./data`).
`ODDS_API_KEY` activa The Odds API; sin ella se usan las cuotas de apertura/cierre de ESPN.

## Fuentes de datos

| Fuente | Estado | Qué aporta |
|---|---|---|
| ESPN API pública | **primaria**, sin auth | PBP con coordenadas, WP por jugada, sustituciones, box, árbitros, arena, cuotas apertura/cierre, lesiones, plantillas |
| ESPN API core | relleno (`backfill_odds`) | cuotas de cierre históricas (ESPN BET) cuando el summary ya no trae `pickcenter`; se excluyen los proveedores "Live" (cuotas durante el partido) |
| stats.nba.com / cdn.nba.com (nba_api) | opcional | tracking oficial agregado (drives, pases, hustle, velocidad, defensa del aro). **Bloquea muchas IPs** (timeout/403 desde esta máquina); el pipeline sigue sin esas columnas `trk_*` |
| The Odds API | opcional (`ODDS_API_KEY`) | cuotas en vivo multi-casa |
| Basketball-Reference | opcional | tablas de temporada, 3.5 s entre peticiones y reintento con huella TLS ante 403 |
| Kaggle | opcional (`kaggle.json`) | datasets de tracking descargados por el usuario |

## Módulos

| Spec | Módulo |
|---|---|
| Spec 1 A–G / spec 2 taxonomía | `features/pipeline.py` (`NBAAdvancedFeaturePipeline`), `team_game.py`, `player_metrics.py`, `shot_quality.py`, `adjustment.py` |
| PBP, posesiones, lineups | `processing/pbp.py`, `possessions.py`, `lineups.py` |
| Bayes / Kalman (regímenes 1-10, 11-20, 21+, Q-inflation) | `models/kalman.py` |
| Cadena de Markov + CMP + prórroga | `models/markov.py` |
| Clase 1 ingesta | `ingestion/engine.py` (`DataIngestionLayer`), `espn.py`, `sources.py` |
| Clases 2, 3, 5 | `simulation/context.py` |
| Clase 4 | `simulation/inefficiencies.py` (calibración Ridge centrada en priors) |
| Clase 6 | `simulation/monte_carlo.py` |
| Clase 7 | `simulation/financial.py`, `models/devig.py` |
| Orquestación y backtest | `simulation/slate.py`, `cli.py` |

Salida del pipeline de features: DataFrame indexado por `[season, game_date, team]`, ~385
columnas **pre-partido** (sólo usan partidos anteriores), sin nulos, más `target_*` con el
resultado real para entrenar XGBoost / regresión.

## Cobertura de la taxonomía de métricas

Implementado desde PBP (ESPN): ratings off/def/net (total, half-court, transición, clutch,
sin garbage time, low-leverage WP∈[0.05,0.95]), eFG%/TS%, pace y pace neutral, segundos por
posesión por origen, early/late clock, Four Factors (+ ajustados por rival vía Ridge), xeFG/qSQ
(logística con cross-fitting) y shot making, distribución por zonas y Moreyball, esquina 3,
pull-up 3, % asistido, USG%/True Usage y concentración, rim protection con ancla en pista vs
banco, OREB%/DREB%, putbacks, segundas oportunidades, puntos en pintura, scoring possession
rate, ATO PPP, live/dead TOV, puntos concedidos tras robo, 3PT luck, FT luck (FT% previo de
cada tirador), On/Off de la estrella, gestión de faltas del entrenador, descanso/B2B/3-en-4.

Requiere datos que no son gratuitos (no se inventan; las columnas aparecen sólo si se aportan):
coberturas de pick-and-roll (drop/blitz/switch…), zona vs individual, distancia de ayuda y
recuperación, separación en el instante del tiro, distancia del defensor por tiro
(contested/open; se usa si llega `defender_distance` vía Kaggle/tracking), asistencias
secundarias y pass-to-assist (vía `trk_passing_*` de nba_api cuando es accesible).

## Validación (temporada 2025-26 real, 1.161 partidos, point-in-time)

Modelo base (Kalman + Ridge) con el calibrador de sesgos activado:

| Métrica | Modelo | Cierre del mercado |
|---|---|---|
| Acierto de ganador | 68.1% | — |
| Brier | 0.208 | 0.197 |
| MAE margen | 11.57 | 11.19 |
| MAE total | 15.41 | 14.58 |
| ATS | 49.6% | — |
| Sesgo margen local / total playoffs | +0.35 / −0.03 | — |

La pila de contexto está validada en `data/reports/context_calibration_report.md`: mejora al
modelo base pero no al cierre.

## Garantías point-in-time (sin fugas)

- `tests/test_leakage.py`: test de truncamiento. Calcula las features con todos los datos y
  cortando en una fecha D; ninguna feature anterior a D puede cambiar. Pasa también sobre los
  datos reales de 2025-26 (384 columnas, 0 con fuga).
- El modelo xFG se re-entrena cada 14 días sólo con tiros anteriores (`ShotQualityModel`, modo
  `expanding`); la imputación usa referencias de liga de fechas ≤ la del partido. Las filas
  del arranque del dataset sin ningún pasado quedan marcadas en `is_cold_imputed`.
- Los partidos con PBP incompleto (marcador reconstruido ≠ oficial) no alimentan los ratings;
  los targets salen del marcador oficial.
- Las cuotas incoherentes (favorito ML ≠ favorito spread, totales fuera de rango) se anulan.
- La μ de liga y los priors de la temporada siguiente sólo aprenden de temporada regular.

## Calibrador de sesgos (`simulation/bias.py`)

Para cada fecha, y con partidos anteriores, estima la ventaja de campo (que pasa de 2.4 a
~1.9 pts/100 en 2025-26) y los factores de anotación de temporada regular y de playoffs
(prior 0.95). Se aplican como `hca` y como multiplicador del ritmo en todas las simulaciones;
`SlateSimulator.bias_correction = False` lo desactiva.

## Prior de plantilla y mezcla con el mercado

- **Plantillas** (`ingest_rosters`, tabla `rosters`): plantillas actuales de ESPN. Al empezar
  una temporada, `features/roster.py` calcula el RAPM de la anterior (Ridge sobre pares de
  quintetos) y, para cada equipo, la continuidad (minutos retenidos) y el ΔRAPM entre la
  rotación del año pasado y la plantilla actual. El Kalman arranca en
  `retención·(θ + ΔRAPM)`, con más incertidumbre cuanto menor es la continuidad. Sólo se usa
  una foto de plantilla tomada antes del primer partido de temporada regular.
- **Mezcla** (`simulation/blend.py`, `simulate --blend`): para cada fecha, con partidos
  anteriores, ajusta `w` en `margen = w·modelo + (1−w)·cierre` (y lo mismo para el total) y
  desplaza toda la distribución simulada a esa media.

Resultado con 2024-25 + 2025-26 (`data/reports/roster_blend_report_v2.md`, backtest
point-in-time desde el primer partido; cuotas de cierre de ESPN para ~100% de los partidos):

| 2025-26, arranque oct-nov (297 partidos) | Brier ML | LogLoss spread | MAE margen | ATS |
|---|---|---|---|---|
| Modelo sin temporada previa | 0.211 | 0.716 | 10.79 | 51.5% |
| Modelo con 2024-25 | 0.199 | 0.709 | 10.41 | 47.5% |
| Modelo con 2024-25 + plantilla | 0.196 | 0.705 | 10.37 | 50.2% |
| Mezcla | 0.195 | 0.694 | 10.10 | 49.5% |
| Cierre | 0.191 | 0.693 | 10.10 | — |

La temporada previa y el prior de plantilla mejoran claramente el arranque del modelo, pero
ninguna variante supera al cierre. El peso aprendido del modelo en la mezcla termina en ~0.06
(margen) y ~0.07 (total) sobre 2.625 partidos.

## Advertencias

- `scenario_shift = 0.20` (±20% de pts/100, como pide el spec) equivale a ~2 desviaciones
  típicas del ORtg de un partido: los bloques Mejor/Peor son colas extremas. Para uso real,
  0.05–0.08 es más realista (`SimulationConfig.scenario_shift`).
- Al inicio de temporada el prior es el estado final de la anterior (retención 70%). Sin
  `continuity` (minutos retenidos) ni `ΔRAPM` de altas/bajas, el modelo no ve el mercado de
  fichajes: las señales "EXPLOTABLE" de las primeras semanas no son fiables.
- Los efectos de las ineficiencias (letdown, lookahead, jet-lag…) parten de priors y se
  recalibran con el residuo ATS; con una sola temporada siguen dominados por el prior.
