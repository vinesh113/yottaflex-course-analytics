# YottaFlex Course Analytics

A reproducible Course Analytics and Learner Engagement System built with Python and Flask.
The default local mode uses CSV files and needs no database server. `database/schema.sql`
contains the relational schema for all ten required entities and can be loaded into SQLite.

## Quick start

```powershell
python -m pip install -r requirements.txt
python -m generator.generate_all --scale starter --seed 20261022
python -m pytest
python app.py
```

Open `http://127.0.0.1:5000`. The API is available at `/api/metrics`; CSV exports are
available under `/exports/<filename>`.

## Data generation

`starter` generates 100 learners, 10 courses, 300 enrollments and 5,000 activities.
`full` uses the assessment targets: 20,000 learners, 500 courses, 100,000 enrollments and
2,000,000 activities. Both use the same fixed-seed generation path:

```powershell
python -m generator.generate_all --scale full --seed 20261022
```

The generator writes CSV files plus `manifest.json` containing row counts and SHA-256
checksums. Four labelled scenarios are retained in `ground_truth.csv`: duplicate events,
unenrolled activity, completion before assessment, and timezone boundary handling.

## Metric definitions

* **Active enrollment:** at least one valid, deduplicated learning event
  (`VIDEO_WATCHED`, `PDF_OPENED`, `QUIZ_STARTED`, or `QUIZ_COMPLETED`) in the UTC
  seven-day reporting window.
* **Completion:** required content percentage and a passing assessment score are both
  satisfied. A required assessment cannot be skipped.
* **Duplicate:** same enrollment, content, event type, and source timestamp. Original
  rows remain present and are marked/excluded rather than deleted.
* **Cohort rate:** completed outcomes divided by all enrollments in the cohort, using the
  same rules and reporting window.

## Project map

`generator/` creates related synthetic records; `services/` contains business rules;
`validation/` produces data quality checks; `analytics/` exposes dashboard metrics;
`database/schema.sql` defines the ten entities; `tests/` covers reproducibility and
negative scenarios.
