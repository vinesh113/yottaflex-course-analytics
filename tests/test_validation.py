from generator.generate_all import generate
from validation.validate_data import validate


def test_validation_report_has_no_unexpected_failures(tmp_path):
    generate("starter", 123, tmp_path)
    import csv
    datasets = {}
    for name in ("learners", "courses", "enrollments", "activity_events", "attempts"):
        with (tmp_path / f"{name}.csv").open(newline="", encoding="utf-8") as handle:
            datasets[name] = list(csv.DictReader(handle))
    report = validate({**datasets, "course_outcomes": []})
    assert report["failed_checks"] == 0
