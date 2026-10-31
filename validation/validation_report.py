import json
from pathlib import Path

from validation.validate_data import validate


def write_report(datasets: dict, path: Path) -> dict:
    report = validate(datasets)
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report
