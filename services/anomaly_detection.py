from typing import Any

from services.deduplication import deduplicate_events


def detect_anomalies(events: list[dict[str, Any]], enrollment_ids: set[str], outcomes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    _, duplicates = deduplicate_events(events)
    findings = [{"record_id": e["event_id"], "label": "DUPLICATE_EVENT", "decision": "Exclude from engagement"} for e in duplicates]
    findings.extend({"record_id": e["event_id"], "label": "UNENROLLED_ACTIVITY", "decision": "Reject activity"}
                    for e in events if e.get("enrollment_id") not in enrollment_ids)
    findings.extend({"record_id": o["outcome_id"], "label": "INVALID_COMPLETION", "decision": "Keep In Progress"}
                    for o in outcomes if o.get("completion_status") == "Completed" and o.get("assessment_score") in ("", None))
    findings.extend({"record_id": e["event_id"], "label": "TIMEZONE_BOUNDARY", "decision": "Use course reporting timezone"}
                    for e in events if e.get("anomaly_code") == "TIMEZONE_BOUNDARY")
    return findings
