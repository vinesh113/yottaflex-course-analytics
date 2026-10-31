PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS learners (
  learner_id TEXT PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL UNIQUE, status TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS courses (
  course_id TEXT PRIMARY KEY, course_name TEXT NOT NULL, duration_days INTEGER NOT NULL,
  reporting_timezone TEXT NOT NULL DEFAULT 'UTC'
);
CREATE TABLE IF NOT EXISTS cohorts (
  cohort_id TEXT PRIMARY KEY, cohort_name TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS enrollments (
  enrollment_id TEXT PRIMARY KEY, learner_id TEXT NOT NULL REFERENCES learners,
  course_id TEXT NOT NULL REFERENCES courses, cohort_id TEXT NOT NULL REFERENCES cohorts,
  enrolled_at TEXT NOT NULL, status TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS content_items (
  content_id TEXT PRIMARY KEY, course_id TEXT NOT NULL REFERENCES courses,
  content_name TEXT NOT NULL, content_type TEXT NOT NULL, is_required INTEGER NOT NULL,
  parent_content_id TEXT REFERENCES content_items
);
CREATE TABLE IF NOT EXISTS activity_events (
  event_id TEXT PRIMARY KEY, enrollment_id TEXT NOT NULL REFERENCES enrollments,
  learner_id TEXT NOT NULL REFERENCES learners, course_id TEXT NOT NULL REFERENCES courses,
  event_type TEXT NOT NULL, content_id TEXT REFERENCES content_items, event_timestamp TEXT NOT NULL,
  source_timestamp TEXT NOT NULL, device_type TEXT NOT NULL, is_duplicate INTEGER NOT NULL DEFAULT 0,
  anomaly_code TEXT
);
CREATE TABLE IF NOT EXISTS assessments (
  assessment_id TEXT PRIMARY KEY, course_id TEXT NOT NULL REFERENCES courses,
  assessment_name TEXT NOT NULL, total_marks INTEGER NOT NULL, passing_marks INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS attempts (
  attempt_id TEXT PRIMARY KEY, learner_id TEXT NOT NULL REFERENCES learners,
  assessment_id TEXT NOT NULL REFERENCES assessments, attempted_at TEXT NOT NULL,
  score REAL NOT NULL, status TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS completion_rules (
  rule_id TEXT PRIMARY KEY, course_id TEXT NOT NULL UNIQUE REFERENCES courses,
  minimum_content_percent REAL NOT NULL, minimum_assessment_score REAL NOT NULL,
  require_assessment INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS course_outcomes (
  outcome_id TEXT PRIMARY KEY, learner_id TEXT NOT NULL REFERENCES learners,
  course_id TEXT NOT NULL REFERENCES courses, completion_percent REAL NOT NULL,
  assessment_score REAL, completion_status TEXT NOT NULL, calculated_at TEXT NOT NULL
);
