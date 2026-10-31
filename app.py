from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, render_template, send_from_directory

from analytics.dashboard_metrics import metrics
from config import DATA_DIR
from generator.generate_all import generate


def load_data(data_dir: Path = DATA_DIR) -> dict[str, list[dict[str, Any]]]:
    if not (data_dir / "manifest.json").exists():
        generate("starter", output_dir=data_dir)
    datasets: dict[str, list[dict[str, Any]]] = {}
    for path in data_dir.glob("*.csv"):
        with path.open(newline="", encoding="utf-8") as handle:
            datasets[path.stem] = list(csv.DictReader(handle))
    return datasets


app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html", metrics=metrics(load_data()))


@app.get("/api/metrics")
def api_metrics():
    return jsonify(metrics(load_data()))


@app.get("/exports/<path:filename>")
def export_file(filename: str):
    return send_from_directory(DATA_DIR, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
