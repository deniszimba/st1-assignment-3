
# SmartCare Appointment System

Software Technology 1 — Assignment 3  
Requirements baseline: SmartCare A3 2026 Revision 2

## Overview

SmartCare is a Python appointment management application for a small clinic. It supports patient and practitioner registration, appointment booking, cancellation, lookup and practitioner appointment listing.

The application uses in-memory storage. All records exist only during the current program session and are lost when the program exits.

## Requirements

- Python 3.13 or compatible environment
- pytest 8.3.5 for automated testing
- No additional runtime dependencies

## Setup

Open a terminal in the `project` directory.

Install the development dependency if required:

```sh
python -m pip install -r requirements-dev.txt
```

## Running the application

Run the synthetic demonstration:

```sh
python main.py
```

Launch the interactive menu:

```sh
python main.py --interactive
```

## Interactive menu

| Option | Operation |
|---|---|
| 1 | Register patient |
| 2 | Find patient |
| 3 | Register practitioner |
| 4 | Find practitioner |
| 5 | Book appointment |
| 6 | Cancel appointment |
| 7 | Find appointment |
| 8 | List practitioner appointments |
| 0 | Exit |

Use the date/time format `YYYY-MM-DD HH:MM`.

Appointment listing accepts a practitioner ID and an optional status of `scheduled`, `cancelled` or `completed`. Leaving the status blank includes all appointments for that practitioner.

## Application structure

- `smartcare/domain.py` — Patient, Practitioner and Appointment classes, validation and guarded cancellation.
- `smartcare/data_store.py` — In-memory collections and lookup operations.
- `smartcare/services.py` — Registration, booking, cancellation, lookup and validated practitioner listing.
- `smartcare/queries.py` — Pure appointment filtering and sorting.
- `smartcare/console.py` — Interactive menu, date/time parsing and output formatting.
- `main.py` — Application entry point.
- `tests/` — Automated domain, service, query and workflow tests.

Services use the same SmartCareDataStore instance throughout each interactive session.

## Business rules

- Patient, practitioner and appointment IDs must be unique.
- IDs are trimmed, non-blank and case-sensitive.
- Appointments reference registered Patient and Practitioner objects.
- A practitioner cannot have two SCHEDULED appointments at exactly the same date/time.
- Different practitioners may have appointments at the same time.
- Only SCHEDULED appointments can be cancelled.
- Cancelled appointments remain stored and retrievable during the session.
- Practitioner appointments are ordered by date/time, then appointment ID.
- Invalid operations raise meaningful errors without partially changing the stored state.

## Testing

From the `project` directory, run:

```sh
python -m pytest -q
```

Stage 9 local verification on 31 October 2026:

**70 tests passed in 0.18 seconds.**

Tests cover domain validation, registration, appointment conflicts, cancellation, retained history, pure queries, service listing, interactive workflows and expected error recovery.

The passing suite supports the tested requirements but does not guarantee that every possible input or scenario has been covered.

## Scope and limitations

- Synthetic teaching data only.
- Records are lost when the program exits.
- No SQLite, database, file persistence or saved session data.
- No authentication or real patient information.
- No rescheduling workflow (PG extension only).
- No duration-overlap, patient scheduling-conflict, clinic-hours or past-date restrictions.
- Unexpected programming errors are not silently ignored.

The application follows the undergraduate Assignment 3 pathway: Stages 6, 7, 8, 9 and 12.
