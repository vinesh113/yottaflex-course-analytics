from services.completion import check_completion


RULE = {"minimum_content_percent": 90, "minimum_assessment_score": 40, "require_assessment": 1}


def test_completion_requires_assessment():
    assert check_completion(100, None, RULE) == "In Progress"
    assert check_completion(90, 40, RULE) == "Completed"


def test_completion_requires_both_thresholds():
    assert check_completion(89, 99, RULE) == "In Progress"
    assert check_completion(99, 39, RULE) == "In Progress"
