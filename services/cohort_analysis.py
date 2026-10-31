from collections import defaultdict
from typing import Any


def compare_cohorts(enrollments: list[dict[str, Any]], outcomes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    outcome_by_key = {(o["learner_id"], o["course_id"]): o for o in outcomes}
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for enrollment in enrollments:
        grouped[enrollment["cohort_id"]].append(outcome_by_key.get((enrollment["learner_id"], enrollment["course_id"]), {}))
    return [{"cohort_id": cohort, "students": len(rows),
             "completed": sum(row.get("completion_status") == "Completed" for row in rows),
             "completion_rate": round(sum(row.get("completion_status") == "Completed" for row in rows) / len(rows) * 100, 2)}
            for cohort, rows in sorted(grouped.items()) if rows]
