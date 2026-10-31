from typing import Any


def check_completion(content_percent: float, score: float | None, rule: dict[str, Any]) -> str:
    content_ok = content_percent >= float(rule["minimum_content_percent"])
    assessment_ok = score is not None and score >= float(rule["minimum_assessment_score"])
    if content_ok and (not int(rule.get("require_assessment", 1)) or assessment_ok):
        return "Completed"
    return "In Progress" if content_percent or score is not None else "Not Started"
