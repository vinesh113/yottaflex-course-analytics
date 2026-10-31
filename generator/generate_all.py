from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from config import DATA_DIR, SCALES, SEED

EVENT_TYPES = ("LOGIN", "VIDEO_WATCHED", "PDF_OPENED", "QUIZ_STARTED", "QUIZ_COMPLETED")
DEVICES = ("web", "ios", "android")


def _write(path: Path, rows: list[dict[str, Any]]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]) if rows else [])
        writer.writeheader()
        writer.writerows(rows)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return digest


def generate(scale: str = "starter", seed: int = SEED, output_dir: Path = DATA_DIR) -> dict[str, Any]:
    if scale not in SCALES:
        raise ValueError(f"Unknown scale {scale!r}; choose one of {sorted(SCALES)}")
    counts = SCALES[scale]
    rng = random.Random(seed)
    now = datetime(2026, 1, 31, 23, 30, tzinfo=timezone.utc)
    learners = [
        {"learner_id": f"LRN-{i:06d}", "name": f"Student_{i:06d}",
         "email": f"student_{i:06d}@example.test", "status": "Active" if i % 11 else "Inactive"}
        for i in range(1, counts.learners + 1)
    ]
    cohorts = [
        {"cohort_id": f"COH-{i:03d}", "cohort_name": month}
        for i, month in enumerate(("January 2026", "February 2026", "March 2026"), 1)
    ]
    courses = [
        {"course_id": f"CRS-{i:06d}", "course_name": f"Course {i:03d}",
         "duration_days": 20 + i % 41, "reporting_timezone": "UTC"}
        for i in range(1, counts.courses + 1)
    ]
    contents: list[dict[str, Any]] = []
    for course in courses:
        for position in range(1, 6):
            contents.append({
                "content_id": f"CNT-{len(contents) + 1:07d}", "course_id": course["course_id"],
                "content_name": f"{course['course_name']} Module {position}",
                "content_type": "Video" if position % 2 else "PDF", "is_required": 1,
                "parent_content_id": "",
            })
    contents_by_course: dict[str, list[dict[str, Any]]] = {}
    for content in contents:
        contents_by_course.setdefault(content["course_id"], []).append(content)
    rules = [{
        "rule_id": f"RULE-{course['course_id']}", "course_id": course["course_id"],
        "minimum_content_percent": 80, "minimum_assessment_score": 40,
        "require_assessment": 1,
    } for course in courses]
    assessments = [{
        "assessment_id": f"ASM-{i:07d}", "course_id": course["course_id"],
        "assessment_name": f"{course['course_name']} Final", "total_marks": 100,
        "passing_marks": 40,
    } for i, course in enumerate(courses, 1)]
    enrollments: list[dict[str, Any]] = []
    for i in range(counts.enrollments):
        learner = learners[i % len(learners)]
        course = courses[(i * 17 + rng.randrange(len(courses))) % len(courses)]
        start = datetime(2026, 1, 1, tzinfo=timezone.utc) + timedelta(days=i % 60)
        enrollments.append({
            "enrollment_id": f"ENR-{i + 1:07d}", "learner_id": learner["learner_id"],
            "course_id": course["course_id"], "cohort_id": cohorts[i % len(cohorts)]["cohort_id"],
            "enrolled_at": start.isoformat(), "status": "Active",
        })
    enrollment_by_id = {row["enrollment_id"]: row for row in enrollments}
    activities: list[dict[str, Any]] = []
    for i in range(counts.activities):
        enrollment = enrollments[i % len(enrollments)]
        course_contents = contents_by_course[enrollment["course_id"]]
        content = course_contents[(i * 13 + rng.randrange(len(course_contents))) % len(course_contents)]
        event_time = now - timedelta(days=rng.randrange(45), hours=rng.randrange(24), minutes=rng.randrange(60))
        activities.append({
            "event_id": f"EVT-{i + 1:09d}", "enrollment_id": enrollment["enrollment_id"],
            "learner_id": enrollment["learner_id"], "course_id": enrollment["course_id"],
            "event_type": EVENT_TYPES[i % len(EVENT_TYPES)], "content_id": content["content_id"],
            "event_timestamp": event_time.isoformat(), "source_timestamp": event_time.isoformat(),
            "device_type": DEVICES[i % len(DEVICES)], "is_duplicate": 0, "anomaly_code": "",
        })
    attempts: list[dict[str, Any]] = []
    for i, enrollment in enumerate(enrollments):
        if i % 3:
            assessment = assessments[courses.index(next(c for c in courses if c["course_id"] == enrollment["course_id"]))]
            score = 35 + (i * 19) % 66
            attempts.append({
                "attempt_id": f"ATT-{len(attempts) + 1:08d}", "learner_id": enrollment["learner_id"],
                "assessment_id": assessment["assessment_id"], "attempted_at": enrollment["enrolled_at"],
                "score": score, "status": "Passed" if score >= 40 else "Failed",
            })
    learning_events_by_enrollment: dict[str, int] = {}
    for event in activities:
        if event["event_type"] in ("VIDEO_WATCHED", "PDF_OPENED"):
            learning_events_by_enrollment[event["enrollment_id"]] = learning_events_by_enrollment.get(event["enrollment_id"], 0) + 1
    outcomes: list[dict[str, Any]] = []
    assessment_course = {assessment["assessment_id"]: assessment["course_id"] for assessment in assessments}
    attempts_by_course_learner = {(a["learner_id"], assessment_course[a["assessment_id"]]): a["score"] for a in attempts}
    for enrollment in enrollments:
        event_count = learning_events_by_enrollment.get(enrollment["enrollment_id"], 0)
        content_percent = min(100, event_count * 20)
        score = attempts_by_course_learner.get((enrollment["learner_id"], enrollment["course_id"]))
        complete = content_percent >= 80 and score is not None and score >= 40
        outcomes.append({
            "outcome_id": f"OUT-{len(outcomes) + 1:07d}", "learner_id": enrollment["learner_id"],
            "course_id": enrollment["course_id"], "completion_percent": content_percent,
            "assessment_score": "" if score is None else score,
            "completion_status": "Completed" if complete else ("In Progress" if event_count else "Not Started"),
            "calculated_at": now.isoformat(),
        })
    ground_truth = [
        {"scenario_id": "GT-001", "scenario": "Duplicate events", "record_id": "EVT-000000002",
         "expected_label": "DUPLICATE_EVENT", "expected_decision": "Exclude from engagement"},
        {"scenario_id": "GT-002", "scenario": "Unenrolled activity", "record_id": "EVT-000000003",
         "expected_label": "UNENROLLED_ACTIVITY", "expected_decision": "Reject activity"},
        {"scenario_id": "GT-003", "scenario": "Completion before assessment", "record_id": "OUT-0000001",
         "expected_label": "INVALID_COMPLETION", "expected_decision": "Keep In Progress"},
        {"scenario_id": "GT-004", "scenario": "Timezone shift", "record_id": "EVT-000000004",
         "expected_label": "TIMEZONE_BOUNDARY", "expected_decision": "Use course reporting timezone"},
    ]
    # Inject deterministic, traceable exceptions after baseline generation.
    if len(activities) >= 4:
        activities[1].update(learner_id=activities[0]["learner_id"], course_id=activities[0]["course_id"],
                             enrollment_id=activities[0]["enrollment_id"], event_type=activities[0]["event_type"],
                             content_id=activities[0]["content_id"], event_timestamp=activities[0]["event_timestamp"],
                             source_timestamp=activities[0]["source_timestamp"], is_duplicate=1, anomaly_code="DUPLICATE_EVENT")
        activities[2].update(enrollment_id="ENR-INVALID", course_id="CRS-INVALID", anomaly_code="UNENROLLED_ACTIVITY")
        activities[3]["event_timestamp"] = "2026-01-10T23:30:00-05:00"
        activities[3]["anomaly_code"] = "TIMEZONE_BOUNDARY"
    if outcomes:
        outcomes[0].update(completion_status="Completed", assessment_score="", anomaly_code="INVALID_COMPLETION")
    output_dir.mkdir(parents=True, exist_ok=True)
    datasets = {
        "learners": learners, "courses": courses, "cohorts": cohorts, "enrollments": enrollments,
        "content_items": contents, "activity_events": activities, "assessments": assessments,
        "attempts": attempts, "completion_rules": rules, "course_outcomes": outcomes,
        "ground_truth": ground_truth,
    }
    manifest = {"seed": seed, "scale": scale, "generated_at": now.isoformat(), "reporting_timezone": "UTC", "files": {}}
    for name, rows in datasets.items():
        manifest["files"][name] = {"rows": len(rows), "sha256": _write(output_dir / f"{name}.csv", rows)}
    manifest["counts"] = {name: len(rows) for name, rows in datasets.items()}
    (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate deterministic course analytics data.")
    parser.add_argument("--scale", choices=sorted(SCALES), default="starter")
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--output-dir", type=Path, default=DATA_DIR)
    args = parser.parse_args()
    print(json.dumps(generate(args.scale, args.seed, args.output_dir), indent=2))
