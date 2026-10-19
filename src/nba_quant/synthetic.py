"""Liga sintética en el esquema canónico (mismo que produce `ingestion/espn.py`).

Sirve para tests deterministas y para el demo offline de extremo a extremo cuando no hay
red. Los equipos tienen fuerzas latentes conocidas, así que los tests pueden verificar que
el pipeline las recupera (Kalman/Ridge) y que el motor de Markov reproduce los marcadores.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy.stats import norm

from nba_quant.teams import TEAM_GEO

PERIOD_SEC = 720.0
PLAYERS_PER_TEAM = 8
STARTERS = 5
BASE_PPP_LOGIT = {"three": 0.355, "two": 0.53, "rim": 0.66}


@dataclass(frozen=True)
class SyntheticLeague:
    games: pd.DataFrame
    pbp: pd.DataFrame
    player_box: pd.DataFrame
    odds: pd.DataFrame
    officials: pd.DataFrame
    strengths: pd.DataFrame  # verdad: off/def en pts/100 vs liga


class _GameWriter:
    """Acumula eventos de un partido manteniendo marcador, reloj y secuencia."""

    def __init__(self, gid: str, home: str, away: str) -> None:
        self.gid, self.home, self.away = gid, home, away
        self.rows: list[dict] = []
        self.score = {home: 0, away: 0}
        self.seq = 0

    def add(self, period: int, clock: float, team: str | None, etype: str, **kw: object) -> None:
        self.seq += 1
        pts = kw.pop("points", 0)
        if team is not None and pts:
            self.score[team] += int(pts)
        row = {
            "game_id": self.gid, "event_idx": self.seq, "play_id": f"{self.gid}{self.seq}", "period": period,
            "clock_sec": round(max(clock, 0.0), 1), "team": team, "event_type": etype, "subtype": kw.pop("subtype", etype),
            "text": kw.pop("text", ""), "made": False, "shot_value": 0, "shot_distance": np.nan, "x": np.nan, "y": np.nan,
            "is_offensive_rebound": False, "is_team_rebound": False, "is_steal": False, "is_shooting_foul": False,
            "ft_num": np.nan, "ft_total": np.nan, "ft_technical": False, "ft_flagrant": False, "assisted": False,
            "shot_style": None, "player_id": None, "player2_id": None, "home_wp": None, "wallclock": None,
            "home_team": self.home, "away_team": self.away,
        }
        row.update(kw)
        row["home_score"], row["away_score"] = self.score[self.home], self.score[self.away]
        self.rows.append(row)


def _simulate_game(rng: np.random.Generator, w: _GameWriter, strength: dict[str, tuple[float, float]],
                   players: dict[str, list[str]], pace: float) -> dict[str, dict[str, float]]:
    """Proceso de posesiones simple pero completo: tiros por zona, TL, pérdidas, rebotes, and-1."""
    stats = {t: {p: {"pts": 0.0, "blk": 0.0} for p in players[t]} for t in (w.home, w.away)}
    offense = w.home if rng.random() < 0.5 else w.away
    sec_per_poss = 2880.0 / (2 * pace)
    for period in range(1, 5):
        clock = PERIOD_SEC
        w.add(period, clock, offense, "jumpball", subtype="Jumpball")
        while clock > 0:
            defense = w.away if offense == w.home else w.home
            edge = (strength[offense][0] + strength[defense][1]) / 100.0  # Δppp vs liga
            transition = rng.random() < 0.16
            clock -= rng.uniform(2, 5.5) if transition else rng.uniform(7, 2 * sec_per_poss - 7)
            if clock <= 0:
                break
            if rng.random() < 0.03:
                w.add(period, clock, offense, "timeout", subtype="Full Timeout")
            while True:  # segmentos: termina en absorción o vuelve tras rebote ofensivo
                shooter = players[offense][int(rng.integers(0, STARTERS))]
                u = rng.random()
                if u < 0.13 - edge * 0.1:
                    steal = rng.random() < 0.55
                    w.add(period, clock, offense, "turnover", subtype="Bad Pass Turnover" if steal else "Traveling",
                          text="bad pass (steal)" if steal else "traveling", is_steal=steal, player_id=shooter)
                    break
                if u < 0.23:
                    w.add(period, clock, defense, "foul", subtype="Shooting Foul", is_shooting_foul=True,
                          player_id=players[defense][int(rng.integers(0, STARTERS))])
                    last_made = False
                    for k in (1, 2):
                        last_made = bool(rng.random() < 0.78)
                        w.add(period, clock, offense, "free_throw", subtype=f"Free Throw - {k} of 2", made=last_made,
                              shot_value=1, ft_num=float(k), ft_total=2.0, player_id=shooter, points=int(last_made))
                        stats[offense][shooter]["pts"] += last_made
                    if last_made:
                        break
                    made = None
                else:
                    zone = rng.choice(["three", "two", "rim"], p=[0.40, 0.22, 0.38])
                    value = 3 if zone == "three" else 2
                    dist = {"three": rng.uniform(23, 27), "two": rng.uniform(8, 20), "rim": rng.uniform(0, 3.5)}[zone]
                    ang = rng.uniform(-np.pi / 2, np.pi / 2)
                    p_make = np.clip(BASE_PPP_LOGIT[zone] + edge * 0.45, 0.05, 0.95)
                    made = bool(rng.random() < p_make)
                    style = "catch_shoot" if (zone == "three" and rng.random() < 0.6) else ("drive" if zone == "rim" else "pull_up")
                    assisted = made and rng.random() < 0.6
                    w.add(period, clock, offense, "shot", subtype="Jump Shot", made=made, shot_value=value,
                          shot_distance=float(dist), x=float(dist * np.sin(ang)), y=float(abs(dist * np.cos(ang))),
                          assisted=assisted, shot_style=style, player_id=shooter,
                          player2_id=players[offense][int(rng.integers(0, STARTERS))] if assisted else None,
                          points=value if made else 0)
                    if made:
                        stats[offense][shooter]["pts"] += value
                        if value == 2 and rng.random() < 0.07:  # and-1
                            ft_made = bool(rng.random() < 0.78)
                            w.add(period, clock, defense, "foul", subtype="Shooting Foul", is_shooting_foul=True,
                                  player_id=players[defense][0])
                            w.add(period, clock, offense, "free_throw", subtype="Free Throw - 1 of 1", made=ft_made,
                                  shot_value=1, ft_num=1.0, ft_total=1.0, player_id=shooter, points=int(ft_made))
                            stats[offense][shooter]["pts"] += ft_made
                        break
                    if zone == "rim" and rng.random() < 0.08:
                        stats[defense][players[defense][4]]["blk"] += 1
                # fallo (tiro o último TL): rebote
                if rng.random() < 0.25:
                    w.add(period, clock, offense, "rebound", subtype="Offensive Rebound", is_offensive_rebound=True,
                          player_id=players[offense][int(rng.integers(0, STARTERS))])
                    clock -= rng.uniform(1, 4)
                    if clock <= 0:
                        break
                    continue
                w.add(period, clock, defense, "rebound", subtype="Defensive Rebound",
                      player_id=players[defense][int(rng.integers(0, STARTERS))])
                break
            offense = w.away if offense == w.home else w.home
        w.add(period, 0.0, None, "period_end", subtype="End Period")
    return stats


def _synthetic_odds(games: pd.DataFrame, true_margins: list[tuple[str, float]], rng: np.random.Generator,
                    season: int) -> list[dict]:
    """Mercado sintético *eficiente con ruido*: spread = −(a + b·margen_verdadero) + ruido, con
    (a, b) ajustados por MCO a los márgenes realmente simulados; total = media de liga + ruido."""
    tm = pd.DataFrame(true_margins, columns=["game_id", "true"]).merge(games, on="game_id")
    actual = tm["home_score"] - tm["away_score"]
    b, a = np.polyfit(tm["true"], actual, 1)
    mean_total = float((tm["home_score"] + tm["away_score"]).mean())
    sd_margin = float((actual - (a + b * tm["true"])).std())
    rows = []
    for gid, true in zip(tm["game_id"], tm["true"]):
        exp = a + b * true
        spread = float(np.round(-(exp + rng.normal(0, 1.0)) * 2) / 2)
        total = float(np.round((mean_total + rng.normal(0, 2.0)) * 2) / 2)
        p_home = float(np.clip(norm.cdf(-spread / sd_margin), 0.02, 0.98))
        fair_h = -100 * p_home / (1 - p_home) if p_home > 0.5 else 100 * (1 - p_home) / p_home
        fair_a = -100 * (1 - p_home) / p_home if p_home < 0.5 else 100 * p_home / (1 - p_home)
        vig = lambda ml: ml - 10  # noqa: E731  (restar 10 a ambos lados ≈ 4-5% de margen)
        rows.append({"game_id": gid, "season": season, "provider": "SynthBook", "spread_open": spread + 0.5,
                     "spread_close": spread, "spread_home_odds_close": -110.0, "spread_away_odds_close": -110.0,
                     "total_open": total - 1.0, "total_close": total, "over_odds_close": -110.0,
                     "under_odds_close": -110.0, "home_ml_open": vig(fair_h), "home_ml_close": vig(fair_h),
                     "away_ml_open": vig(fair_a), "away_ml_close": vig(fair_a)})
    return rows


def generate_league(n_teams: int = 6, n_rounds: int = 4, seed: int = 7, season: int = 2026) -> SyntheticLeague:
    rng = np.random.default_rng(seed)
    teams = list(TEAM_GEO)[:n_teams]
    off = rng.normal(0, 4, n_teams)
    dfn = rng.normal(0, 4, n_teams)
    strength = {t: (float(off[i] - off.mean()), float(dfn[i] - dfn.mean())) for i, t in enumerate(teams)}
    players = {t: [f"{t}{j}" for j in range(PLAYERS_PER_TEAM)] for t in teams}
    pace = {t: float(rng.normal(99, 2.5)) for t in teams}
    day = pd.Timestamp(f"{season - 1}-10-22")
    games, pbp, box, odds, offs = [], [], [], [], []
    true_margins: list[tuple[str, float]] = []
    gnum = 0
    refs = [f"Ref {i}" for i in range(9)]
    for _ in range(n_rounds):
        pairs = [(h, a) for h in teams for a in teams if h != a]
        rng.shuffle(pairs)
        for k in range(0, len(pairs), max(1, n_teams // 2)):
            for h, a in pairs[k:k + max(1, n_teams // 2)]:
                gnum += 1
                gid = f"S{season}{gnum:05d}"
                w = _GameWriter(gid, h, a)
                stats = _simulate_game(rng, w, strength, players, (pace[h] + pace[a]) / 2)
                ev = pd.DataFrame(w.rows).assign(season=season, game_date=day)
                pbp.append(ev)
                games.append({"game_id": gid, "season": season, "season_type": 2, "game_date": day,
                              "home_team": h, "away_team": a, "home_score": w.score[h], "away_score": w.score[a],
                              "n_periods": 4, "neutral_site": False, "venue": f"{h} Arena", "venue_city": h,
                              "attendance": 18000})
                # margen "verdadero" en unidades de rating; se re-escala al mundo simulado más abajo
                true_margins.append((gid, (strength[h][0] + strength[a][1]) - (strength[a][0] + strength[h][1])))
                for i, r in enumerate(rng.choice(refs, 3, replace=False)):
                    offs.append({"game_id": gid, "season": season, "official": r, "order": i})
                for t in (h, a):
                    for j, pid in enumerate(players[t]):
                        st = stats[t][pid]
                        box.append({"game_id": gid, "season": season, "team": t, "player_id": pid,
                                    "player_name": f"Player {pid}", "position": "C" if j == 4 else "G",
                                    "starter": j < STARTERS, "minutes": 34.0 if j < STARTERS else 9.0,
                                    "pts": st["pts"], "blk": st["blk"], "fga": 0.0, "fta": 0.0, "tov": 0.0})
            day += pd.Timedelta(days=2)
    odds = _synthetic_odds(pd.DataFrame(games), true_margins, rng, season)
    truth = pd.DataFrame([{"team": t, "true_off": o, "true_def": d, "pace": pace[t]} for t, (o, d) in strength.items()])
    return SyntheticLeague(pd.DataFrame(games), pd.concat(pbp, ignore_index=True), pd.DataFrame(box),
                           pd.DataFrame(odds), pd.DataFrame(offs), truth)
