from collections import Counter
from typing import Any


def validate(datasets: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    learners = {r["learner_id"] for r in datasets["learners"]}
    courses = {r["course_id"] for r in datasets["courses"]}
    enrollments = datasets["enrollments"]
    checks = [
        ("learner_ids_unique", len(learners) == len(datasets["learners"])),
        ("course_ids_unique", len(courses) == len(datasets["courses"])),
        ("enrollment_foreign_keys", all(e["learner_id"] in learners and e["course_id"] in courses for e in enrollments)),
        ("activity_enrollment_references", all(e["enrollment_id"] in {x["enrollment_id"] for x in enrollments} or e.get("anomaly_code") == "UNENROLLED_ACTIVITY" for e in datasets["activity_events"])),
        ("assessment_scores_valid", all(0 <= int(a["score"]) <= 100 for a in datasets["attempts"])),
        ("duplicate_event_counted", bool(sum(1 for e in datasets["activity_events"] if str(e.get("is_duplicate")) == "1"))),
    ]
    return {"records_checked": sum(len(rows) for rows in datasets.values()), "checks": [{"name": n, "passed": p} for n, p in checks],
            "failed_checks": sum(not p for _, p in checks), "duplicate_records": sum(1 for e in datasets["activity_events"] if str(e.get("is_duplicate")) == "1")}
