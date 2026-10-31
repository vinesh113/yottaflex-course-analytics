from collections.abc import Iterable
from typing import Any


def deduplicate_events(events: Iterable[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    seen: set[tuple[Any, ...]] = set()
    valid, duplicates = [], []
    for event in events:
        key = (event.get("enrollment_id"), event.get("content_id"), event.get("event_type"), event.get("source_timestamp"))
        target = duplicates if key in seen or str(event.get("is_duplicate")) == "1" else valid
        if target is duplicates:
            duplicates.append(event)
        else:
            seen.add(key)
            valid.append(event)
    return valid, duplicates
