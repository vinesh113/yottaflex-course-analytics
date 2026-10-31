# Database schema

`database/schema.sql` defines the ten entities and foreign-key relationships. Learners
and courses are related many-to-many through enrollments. Activities belong to an
enrollment, assessments belong to courses, attempts belong to learners and assessments,
and outcomes are calculated from the source records and completion rules.
