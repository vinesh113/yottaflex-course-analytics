# Data dictionary

| Entity | Primary key | Important fields |
|---|---|---|
| Learner | learner_id | name, email, status |
| Course | course_id | course_name, duration_days, reporting_timezone |
| Enrollment | enrollment_id | learner_id, course_id, cohort_id, enrolled_at |
| ContentItem | content_id | course_id, content_type, is_required, parent_content_id |
| ActivityEvent | event_id | enrollment_id, event_type, timestamps, is_duplicate |
| Assessment | assessment_id | course_id, total_marks, passing_marks |
| Attempt | attempt_id | learner_id, assessment_id, score, status |
| CompletionRule | rule_id | course_id, content and score thresholds |
| Cohort | cohort_id | cohort_name |
| CourseOutcome | outcome_id | learner_id, course_id, completion_status |
