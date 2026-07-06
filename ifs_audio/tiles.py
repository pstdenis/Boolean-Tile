import numpy as np

TILE_SIX = [
    {
        "name": "FALSE",
        "bits": (0, 0, 0, 0),
        "walsh": np.array([4, 0, 0, 0], dtype=np.float64),
        "family": "drone",
        "desc": "DC only, no sound",
    },
    {
        "name": "A",
        "bits": (0, 0, 1, 1),
        "walsh": np.array([0, 0, 4, 0], dtype=np.float64),
        "family": "pure",
        "desc": "pure Shepard — ~F (ratio φ² ≈ 2.618)",
    },
    {
        "name": "B",
        "bits": (0, 1, 0, 1),
        "walsh": np.array([0, 4, 0, 0], dtype=np.float64),
        "family": "pure",
        "desc": "pure Shepard — ~G♯ (ratio φ ≈ 1.618)",
    },
    {
        "name": "XOR",
        "bits": (0, 1, 1, 0),
        "walsh": np.array([0, 0, 0, 4], dtype=np.float64),
        "family": "pure",
        "desc": "pure Shepard — ~C♯ (ratio φ³ ≈ 4.236)",
    },
    {
        "name": "AND",
        "bits": (0, 0, 0, 1),
        "walsh": np.array([2, 2, 2, -2], dtype=np.float64),
        "family": "chord",
        "desc": "4-note chord (all 4 Walsh components)",
    },
    {
        "name": "OR",
        "bits": (0, 1, 1, 1),
        "walsh": np.array([-2, 2, 2, 2], dtype=np.float64),
        "family": "chord",
        "desc": "4-note chord (all 4 Walsh components)",
    },
]

TILE_MAP = {t["name"]: t for t in TILE_SIX}
TILE_NAMES = [t["name"] for t in TILE_SIX]
