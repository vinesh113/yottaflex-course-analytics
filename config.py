from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"


@dataclass(frozen=True)
class Scale:
    learners: int
    courses: int
    enrollments: int
    activities: int


SCALES = {
    "starter": Scale(100, 10, 300, 5_000),
    "full": Scale(20_000, 500, 100_000, 2_000_000),
}

SEED = 20261022
REPORTING_TIMEZONE = "UTC"
