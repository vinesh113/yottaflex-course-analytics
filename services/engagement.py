from datetime import datetime, timedelta, timezone
from typing import Any

from services.deduplication import deduplicate_events


LEARNING_EVENTS = {"VIDEO_WATCHED", "PDF_OPENED", "QUIZ_STARTED", "QUIZ_COMPLETED"}


def weekly_active_rate(enrollments: list[dict[str, Any]], events: list[dict[str, Any]], week_start: datetime) -> float:
    valid, _ = deduplicate_events(events)
    week_end = week_start + timedelta(days=7)
    active = {
        event["enrollment_id"] for event in valid
        if event.get("event_type") in LEARNING_EVENTS
        and week_start <= datetime.fromisoformat(event["event_timestamp"]).astimezone(timezone.utc) < week_end
    }
    eligible = {row["enrollment_id"] for row in enrollments}
    return round(len(active & eligible) / len(eligible) * 100, 2) if eligible else 0.0
