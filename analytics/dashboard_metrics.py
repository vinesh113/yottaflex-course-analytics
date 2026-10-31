from typing import Any

from services.anomaly_detection import detect_anomalies
from services.cohort_analysis import compare_cohorts


def metrics(datasets: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    outcomes = datasets["course_outcomes"]
    completed = sum(o["completion_status"] == "Completed" for o in outcomes)
    anomalies = detect_anomalies(datasets["activity_events"], {e["enrollment_id"] for e in datasets["enrollments"]}, outcomes)
    return {
        "learners": len(datasets["learners"]), "courses": len(datasets["courses"]),
        "enrollments": len(datasets["enrollments"]), "activities": len(datasets["activity_events"]),
        "completion_rate": round(completed / len(outcomes) * 100, 2) if outcomes else 0,
        "exceptions": len(anomalies), "cohorts": compare_cohorts(datasets["enrollments"], outcomes),
        "exception_breakdown": {label: sum(a["label"] == label for a in anomalies) for label in
                                ("DUPLICATE_EVENT", "UNENROLLED_ACTIVITY", "INVALID_COMPLETION", "TIMEZONE_BOUNDARY")},
    }
