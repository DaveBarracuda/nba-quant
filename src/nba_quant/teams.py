"""Metadatos estáticos de franquicias: huso horario, altitud y coordenadas de arena.

Se usan para fatiga circadiana (jet-lag), efecto altitud y distancia de viaje.
"""

from __future__ import annotations

import math

# abbr -> (utc_offset_horas_invierno, altitud_pies, lat, lon)
TEAM_GEO: dict[str, tuple[int, int, float, float]] = {
    "ATL": (-5, 1050, 33.757, -84.396),
    "BOS": (-5, 20, 42.366, -71.062),
    "BKN": (-5, 30, 40.683, -73.975),
    "CHA": (-5, 750, 35.225, -80.839),
    "CHI": (-6, 600, 41.881, -87.674),
    "CLE": (-5, 650, 41.496, -81.688),
    "DAL": (-6, 430, 32.790, -96.810),
    "DEN": (-7, 5280, 39.749, -105.008),
    "DET": (-5, 600, 42.341, -83.055),
    "GS": (-8, 10, 37.768, -122.388),
    "HOU": (-6, 50, 29.751, -95.362),
    "IND": (-5, 715, 39.764, -86.155),
    "LAC": (-8, 100, 33.945, -118.343),
    "LAL": (-8, 300, 34.043, -118.267),
    "MEM": (-6, 340, 35.138, -90.051),
    "MIA": (-5, 10, 25.781, -80.188),
    "MIL": (-6, 620, 43.045, -87.917),
    "MIN": (-6, 830, 44.979, -93.276),
    "NO": (-6, 10, 29.949, -90.082),
    "NY": (-5, 30, 40.751, -73.994),
    "OKC": (-6, 1200, 35.463, -97.515),
    "ORL": (-5, 100, 28.539, -81.384),
    "PHI": (-5, 40, 39.901, -75.172),
    "PHX": (-7, 1100, 33.446, -112.071),
    "POR": (-8, 50, 45.532, -122.667),
    "SAC": (-8, 30, 38.580, -121.500),
    "SA": (-6, 650, 29.427, -98.438),
    "TOR": (-5, 250, 43.643, -79.379),
    "UTAH": (-7, 4226, 40.768, -111.901),
    "WSH": (-5, 30, 38.898, -77.021),
}

# Normaliza abreviaturas de otras fuentes (nba_api / B-Ref) al estándar interno (ESPN).
ABBR_ALIASES: dict[str, str] = {
    "GSW": "GS", "NOP": "NO", "NYK": "NY", "SAS": "SA", "UTA": "UTAH", "WAS": "WSH",
    "BRK": "BKN", "CHO": "CHA", "PHO": "PHX", "NJN": "BKN", "NOH": "NO",
}

HIGH_ALTITUDE_FT = 4000


def normalize_abbr(abbr: str) -> str:
    """Convierte cualquier abreviatura conocida al estándar interno (ESPN)."""
    key = (abbr or "").strip().upper()
    return ABBR_ALIASES.get(key, key)


def haversine_miles(a: str, b: str) -> float:
    """Distancia de vuelo aproximada entre las arenas de dos equipos."""
    if a not in TEAM_GEO or b not in TEAM_GEO:
        return 0.0
    _, _, lat1, lon1 = TEAM_GEO[a]
    _, _, lat2, lon2 = TEAM_GEO[b]
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = p2 - p1, math.radians(lon2 - lon1)
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 3958.8 * 2 * math.asin(math.sqrt(h))


def tz_offset(team: str) -> int:
    return TEAM_GEO.get(team, (-5, 0, 0.0, 0.0))[0]


def altitude_ft(team: str) -> int:
    return TEAM_GEO.get(team, (-5, 0, 0.0, 0.0))[1]
