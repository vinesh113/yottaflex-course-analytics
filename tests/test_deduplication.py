from services.deduplication import deduplicate_events


def test_duplicate_is_excluded_but_retained():
    rows = [
        {"event_id": "1", "enrollment_id": "e", "content_id": "c", "event_type": "VIDEO_WATCHED", "source_timestamp": "t"},
        {"event_id": "2", "enrollment_id": "e", "content_id": "c", "event_type": "VIDEO_WATCHED", "source_timestamp": "t"},
    ]
    valid, duplicates = deduplicate_events(rows)
    assert [row["event_id"] for row in valid] == ["1"]
    assert [row["event_id"] for row in duplicates] == ["2"]
