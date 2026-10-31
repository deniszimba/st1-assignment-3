
# Stage 9 activities and evidence

Common UG and PG record. All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage09/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. Use the Stage 9 handout and Overview/revision 2 baseline. Keep responses concise and link accessible artefacts; do not paste entire logs or private peer ratings.

Group: Group 3, Wednesday 4:30–6:30 tutorial.

Members and responsibilities: Denis Zimba led Stage 9 query, service, console, automated test and README work. Andy Hoang led Stage 8 debugging/refactoring. Ahron Singh and Tari Ganas contributed to the earlier Stage 6/7 development and testing. Stage 9 peer review, integration and Stage 12 release remain shared responsibilities; record the actual reviewer and their feedback in H when completed.

Stage 8 integrated SHA, command, working directory and actual result: `e8478d681d17f1a7aae527573e081c6ebe89446b` (merged `main` at the Stage 9 starting point); from `project/`, `python -m pytest -q` → **55 passed in 0.09s**, verified locally on 30 October 2026. Stage 9 began on `feature/stage9-queries` after pulling this checkpoint.

## A. Tutorial activities

### A1 Session state classification

| Information | Required session/domain or transient state? | Requirement or reason |
|---|---|---|
| Patient identity | Required session/domain | Registered ID and name are needed for registration, lookup and appointment relationships (FR-01/02). |
| Appointment history | Required session/domain | Cancelled records must remain retrievable during the session (FR-07/08). |
| Temporary menu choice | Transient interaction | Used to select the current action; it is not a domain record. |
| Practitioner specialty | Required session/domain | A registered practitioner has a validated specialty (FR-03). |
| Debug print output | Transient debug | Diagnostic output is not stored business state. |
| Appointment status | Required session/domain | `SCHEDULED`, `CANCELLED`, `COMPLETED` are part of each appointment's state and filtering/guard rules. |

What is intentionally lost on exit? The shared in-memory `SmartCareDataStore` and its registered patients, practitioners and appointments. Menu inputs and debug output are also transient. The revised baseline retires FR-10 restart persistence: no database or file storage is required.

### A2 Interface and domain data plan

Plan before AI. This replaces schema/key design; no database tables are required.

| Function or component | Explicit inputs and types | Outputs | Responsibility and validation | Domain source / existing constraint |
|---|---|---|---|---|
| `appointment_sort_key` | `appointment: Appointment` | `tuple[datetime, str]` | Purely returns `(date_time, appointment_id)`; no mutation. | `Appointment.date_time`, `appointment_id`; QRY-03, FP-03. |
| `select_appointments` | `appointments: list[Appointment]`, `practitioner_id: str`, `status: AppointmentStatus \| None` | New `list[Appointment]` | Filter by practitioner and optional status, then sort with the named key; assume valid query arguments, no I/O or store access. | `Appointment.practitioner.practitioner_id`, `status`; QRY-01–03, FP-01–03. |
| Service listing | `practitioner_id: str`, `status: AppointmentStatus \| None` | New `list[Appointment]`; may raise `ValueError`/`LookupError` | Validate optional enum and registered practitioner, fetch a fresh store list, delegate to pure query; normalize ID through stored object. | `AppointmentService`, `SmartCareDataStore`, `Practitioner`; QRY-04. |
| Console | Menu selection and text inputs, converted date/time and optional enum | User-facing output; `run_menu() -> None` | Prompt, parse, call existing services, format results and recover from expected errors. | `parse_date_time`, `format_appointment`, three services; UI-01/02. |

Relate patient ID/name, practitioner ID/name/specialty, and appointment ID/actual participants/date_time/status to the existing contracts: `Patient` validates nonblank patient ID/name. `Practitioner` validates ID/name/specialty. `Appointment` validates its ID, while uniqueness is enforced at the store boundary. It references the actual registered `Patient` and `Practitioner` objects, requires a naive minute-precision `datetime`, and stores an `AppointmentStatus` enum. Domain classes own their validation and legal status transitions, the store retains registered identities, services coordinate operations, pure queries only filter/sort and the console handles I/O.

### A3 Responsibility violations

| Conceptual case | Violation | Correct boundary and reason |
|---|---|---|
| `Appointment.cancel` reads input | Domain method would depend on user interaction. | Console asks the user; `Appointment.cancel()` enforces the scheduled-to-cancelled transition. |
| Service prints/reads the menu | Business coordination and presentation would be mixed. | Console displays and reads menus; services coordinate validated workflows. |
| Query sorts its source in place | `appointments.sort()` mutates a caller-owned list, breaking required purity. | `sorted(appointments, key=appointment_sort_key)` returns a fresh container. |
| Store prints `Appointment saved` | The data-store boundary would cause UI output. | Store retains/returns objects; console confirms actions to the user. |

### A4 Sorting comparison

For `appointments.sort(key=appointment_sort_key)` and `result = sorted(appointments, key=appointment_sort_key)`, predict source order, return value and result identity. Give a meaningful mutation check: `.sort()` reorders the *source* list in place and returns `None`; `sorted()` leaves the source order unchanged and returns a **different list** containing the same appointment references. Snapshot `before = list(appointments)`, call the query, then assert `appointments == before`, `result is not appointments`, and verify appointment fields and references were not changed. Equal times are ordered by `appointment_id`.

Score-example prediction and explanation of passing the named key: `[('Chen', 5), ('Ali', 8), ('Bea', 8)]`; the original `scores` remains in its original order. `key=score_key` passes the function itself so sorting calls it for each item; `key=score_key()` would call it immediately without a required item argument and is not the correct key parameter.

### A5 Exit question

Explain cancellation versus deletion, and checks for same-session lookup, all-status listing and SCHEDULED-only exclusion: Cancellation changes the **same retained object** to `AppointmentStatus.CANCELLED`, preserving history and identity; it does not delete its ID. After cancelling A1, `find_appointment('A1') is original` and an all-status practitioner list still includes A1, while the `SCHEDULED`-only list omits it. Its practitioner/time conflict is released, so a different new appointment ID can be booked for that slot.

## B. Human design and contracts

Complete before GitHub Copilot. Record any interface/integrity decision and its reasoning: Initial A1/A2 design was recorded in the Stage 9 evidence record. Further human design/test reasoning for A3–A5 and B was consolidated in [`stage09_human_design_notes.md`](stage09_human_design_notes.md), committed as `b279da3` **before the GitHub Copilot review** on 31 October 2026. The implementation and initial tests had already been completed before this consolidated design note; no claim is made that the entire note predates coding.

| Requirement | Input / session data | Operation and responsible component | Expected result or error | Test / evidence |
|---|---|---|---|---|
| QRY-01 | List of appointment objects and practitioner ID | `select_appointments` | Only that practitioner's appointments | `test_only_requested_practitioner_and_order` |
| QRY-02 | Optional `AppointmentStatus` | `select_appointments` | Default every status; explicit enum restricts; no matches -> `[]` | `test_each_explicit_status`, `test_no_matching_status_returns_empty` |
| QRY-03 | `Appointment.date_time`, `appointment_id` | `appointment_sort_key`, `select_appointments` | Ascending time with appointment ID tie-break; source order preserved | `test_sort_key_uses_datetime_then_id`, `test_source_and_objects_unchanged` |
| QRY-04 | Registered practitioner ID and optional enum | `AppointmentService.list_practitioner_appointments` | Known empty -> `[]`; unknown -> `LookupError`; invalid -> `ValueError`; use trimmed stored ID | `test_listing_validation_and_empty_results`, `test_complete_service_workflow` |
| FP-01 | Explicit list/filter inputs | `queries.py` | Repeatable result without I/O, global store or side effects | `test_fresh_list_and_repeatability`; code inspection |
| FP-02 | Unsorted/sorted/empty source list | `select_appointments` | Fresh list with unchanged source and object fields | `test_source_and_objects_unchanged`, `test_fresh_list_and_repeatability` |
| FP-03 | An appointment | Named `appointment_sort_key` | Named key returns required tuple and is actually used by sorting | `test_sort_key_uses_datetime_then_id`, `test_query_uses_named_sort_key` |
| UI-01 | Menu selections, registered IDs, date/time, status | `console.run_menu`, `main.main` | Repeated registration/find/book/cancel/list/exit | `test_console_complete_workflow`, `test_interactive_entry_point`, manual transcript |
| UI-02 | Invalid menu choice/IDs/status/date | Console boundary and services | Meaningful error and continued menu without partial state change | `test_console_error_recovery`, `test_invalid_booking_preserves_state` |
| FR-01–03 | Valid/invalid patient and practitioner details | Domain, services, store | Validated registration and lookup, duplicate rejection | Existing Stage 6–8 tests; Stage 9 service/console workflows |
| FR-04–06 | Registered participant identities, appointment IDs/time/status | Appointment/domain, store, service | Booking with correct references, exact conflict guard, legal cancellation | `test_complete_service_workflow`, earlier regression tests |
| FR-07–09 | Cancelled history, lookup/list results, state | Domain, store, services, queries | Cancelled object retained and findable; correct guarded operations | `test_complete_service_workflow`, `test_service_filters_completed_appointments`, manual cancellation/lookup |

Cover QRY-01–04, FP-01–03, UI-01–02 and relevant FR-01–09. Explain empty versus unknown versus invalid, enum conversion, actual object identity, error handling and unchanged state on rejection: Known practitioner with zero matches -> a fresh empty list. Unknown valid practitioner ID -> `LookupError`; blank/non-string ID and non-enum filter -> `ValueError` (no silent empty result). Console translates `scheduled`, `cancelled`, `completed` strings to the enum and blank to `None`, while direct service callers must supply `AppointmentStatus` or `None`. Booking uses the actual registered participant objects and rejected operations do not reserve IDs or mutate existing records. A cancelled appointment retains its identity and is returned by all-status listing.

## C. Implementation and query verification

| Requirement / test ID | Code location | Case and meaningful assertion | Actual result | Evidence link |
|---|---|---|---|---|
| QRY-03 / `test_sort_key_uses_datetime_then_id` | `project/smartcare/queries.py` | Named key returns `(datetime, appointment_id)`. | Passed | [`test_queries.py`](../project/tests/test_queries.py) |
| QRY-01/03 / `test_only_requested_practitioner_and_order` | `queries.py` | D1 only, sorted A1/A2 by equal-time IDs then A3; excludes D2. | Passed | [`test_queries.py`](../project/tests/test_queries.py) |
| QRY-02 / `test_each_explicit_status` | `queries.py` | Parameterized `SCHEDULED`, `CANCELLED`, `COMPLETED` return matching IDs. | 3 passed | [`test_queries.py`](../project/tests/test_queries.py) |
| QRY-02 / `test_no_matching_status_returns_empty` | `queries.py` | No matches returns fresh `[]`. | Passed | [`test_queries.py`](../project/tests/test_queries.py) |
| FP-01/02 / source and repeatability tests | `queries.py` | Source order and fields unchanged; new lists for empty, already-sorted, unsorted and repeated calls; same object references. | 2 passed | [`test_queries.py`](../project/tests/test_queries.py) |
| FP-03 / `test_query_uses_named_sort_key` | `queries.py` | Monkeypatch tracks calls to named key and verifies A1/A2/A3 ordering. | Passed | [`test_queries.py`](../project/tests/test_queries.py) |
| QRY-04 / `test_listing_validation_and_empty_results` | `services.py` | Known empty, whitespace ID, unknown and invalid IDs, invalid status; no mutation. | Passed | [`test_workflows.py`](../project/tests/test_workflows.py) |
| QRY-04 / `test_complete_service_workflow` | `services.py` and store | Conflict rejection, different practitioner, retained cancellation, filtered listing, freed slot, object identity. | Passed | [`test_workflows.py`](../project/tests/test_workflows.py) |
| Copilot follow-up / `test_service_filters_completed_appointments` | `services.py` | Stored COMPLETED object returned for matching enum; missing SCHEDULED omitted; stored ID trimmed. | Passed | [`test_stage9_review.py`](../project/tests/test_stage9_review.py) |

Include practitioner isolation, every enum status/default all, equal-time ID tie-break, named-key reuse, repeated calls, empty/already-sorted fresh lists, unchanged source order/fields, known-empty/unknown/invalid service cases and retained history.

Purity explanation from code inspection, including absence of hidden state and I/O: `appointment_sort_key` reads two properties and returns a tuple. `select_appointments` uses only its supplied list, practitioner ID and optional enum, constructs a filtered list, and calls `sorted(..., key=appointment_sort_key)`. It does not call the store or services, print, read input, mutate the input list or assign to an `Appointment`. Its new result list may contain the same object references.

What the tests do and do not establish: Automated assertions confirm the covered filtering/order/non-mutation cases and repeatability on synthetic fixtures. They cannot establish purity for *all possible inputs* or prove the absence of hidden side effects without code inspection. The complete local suite after Copilot follow-up was **74 passed in 0.12 seconds** on 31 October 2026, from `project/` with `python -m pytest -q`.

## D. Integrated console and workflow evidence

| Scenario / acceptance ID | Reproducible inputs / artefact | Expected result | Observed result and state check | Evidence link |
|---|---|---|---|---|
| UI-01 full menu workflow | Scripted `run_menu()` input: register P1/D1/D2; find P1/D1; book A1; reject A2 for D1 at same time; find A2 absent; book A2 with D2; cancel/find A1; list D1 all/SCHEDULED; book A3 into freed slot; list again; exit. | Continuous working menu, valid relationships, correct conflict and cancellation/list results. | `test_console_complete_workflow` passed, including output checks. Manual interactive run separately confirmed registration, booking A1, conflict rejection, A2 not found, A1 cancellation, A1 retained on lookup, then exit. | [`test_workflows.py`](../project/tests/test_workflows.py); manual VS Code terminal run on 30 Oct 2026 |
| UI-02 invalid-input recovery | Scripted input: unknown choice, blank ID, duplicate patient, unknown booking participant, invalid/malformed calendar date, unknown appointment, repeated cancellation, invalid status, subsequent valid actions. | Meaningful errors, no crash and menu continues. | `test_console_error_recovery`, `test_invalid_booking_preserves_state` and strict parser test passed. A failed conflict booking left A2 absent in the manual session. | [`test_workflows.py`](../project/tests/test_workflows.py) |
| Automated service workflow | Fresh store, P1, D1/D2, A1 at `2026-10-01 09:00` and conflicting A2, then D2 booking, cancellation, filtering, new D1 booking at freed time. | Identity preserved, conflict rejected without mutation, retained history and correct filters. | `test_complete_service_workflow` passed; same object returned by lookup/cancellation. | [`test_workflows.py`](../project/tests/test_workflows.py) |

Include registration/find, booking, conflict rejection, different-practitioner booking, cancellation, retrieval, listing/filtering, freed slot and exit; duplicate/unknown/blank IDs, malformed/impossible date, invalid status, unknown choice and repeated cancellation. Identify before/after state and subsequent successful action: `test_console_complete_workflow` and `test_console_error_recovery` run the **real menu function** with reproducible input and assert its output. Service tests also check before/after store contents. Manual checks used lowercase patient ID `p1` (IDs are case-sensitive): it was registered, A1 booked for p1/D1, same-practitioner/time A2 rejected, A2 lookup returned "Appointment not found", A1 cancelled, and A1 lookup returned the same ID/status in the same session. The session exited normally. The manual run did *not* separately demonstrate every menu option; scripted menu tests cover the additional cases.

Copilot follow-up: [`test_stage9_review.py`](../project/tests/test_stage9_review.py) additionally verifies a COMPLETED filter through the service, ascending console display, and `main.py` demo/interactive dispatch. Four tests passed as part of the 74-test total.

## E. GitHub Copilot review and human decisions

Human design completed before AI: [`stage09_human_design_notes.md`](stage09_human_design_notes.md), commit [`b279da3`](https://github.com/deniszimba/st1-assignment-3/commit/b279da3). This note was committed and pushed before the review; see B for the honest timing relative to the earlier implementation.

Actual prompt/context supplied: On 31 October 2026 GitHub Copilot Chat was asked to act as a SmartCare query/console integration reviewer, inspect `queries.py`, `services.py`, `console.py`, `main.py`, `test_queries.py`, `test_workflows.py` and the human design note, and assess (1) purity/non-mutation, (2) boundaries, (3) validation/recovery, (4) identity/enums/ordering, (5) retained history/integrity, (6) missing tests. The prompt instructed: no redesigned domain/storage/frameworks, separate observed evidence from optional improvements, rank Critical/Important/Optional, cite evidence, and **do not edit files**. It noted 70 local tests passed before this review.

Actual response: GitHub Copilot reported **"Critical: None found. Important: None found."** It identified four **Optional** areas: (i) non-atomic concurrent booking, explicitly out of scope for the current single-threaded menu; (ii) missing service workflow test for COMPLETED status; (iii) missing explicit assertion of console listing display order; (iv) missing `main.py` entry-point dispatch tests. It stated the existing query/service/console contracts aligned, and explicitly said it **had not rerun the tests**. This is the actual local Copilot Chat output shared on 31 October 2026, summarized here; save the Chat transcript/screenshot as supplementary evidence if requested.

| AI finding | Code/test evidence | Severity | Accept/Modify/Reject and reason | Change or no change | Actual verification |
|---|---|---|---|---|---|
| Booking check is not atomic under simultaneous concurrent requests | `AppointmentService.book_appointment` checks conflict before insertion. Existing console uses one thread and the baseline has no concurrency rule. | Optional | **Reject as out of scope**: locks/transactions would add unrequired complexity, not fix an assessed single-threaded defect. | No change. | Existing conflict tests and scripted workflow pass; concurrency not claimed as tested. |
| COMPLETED service filtering not explicitly tested | Query fixture tests `COMPLETED`, but service workflow initially checked only SCHEDULED/CANCELLED. | Optional | **Accept**: small evidence gap at service delegation boundary. | Added `test_service_filters_completed_appointments`. | Passed in 74-test suite. |
| Console presentation order not asserted | Query/service tests checked sorting, not rendered menu order. | Optional | **Accept**: straightforward output regression assertion. | Added `test_console_displays_appointments_in_sorted_order`. | Passed in 74-test suite. |
| Demo versus `--interactive` dispatch untested | `main.py` branches on parsed argument; earlier suite lacked dispatch assertions. | Optional | **Accept**: small, focused coverage addition without redesign. | Added `test_interactive_entry_point` and `test_default_demo_entry_point`. | Both passed in 74-test suite. |

Responsibility check: Domain objects own valid fields, identity and guarded cancellation; the data store owns in-memory collections and registration relationships; services coordinate and validate workflows; `queries.py` filters/sorts supplied objects without side effects; `console.py` parses, prompts, formats and catches only expected user errors; `main.py` dispatches the chosen mode. No persistence or rescheduling was introduced.

## F. Required reflections

1. Which integration concern was architectural rather than a filtering/sorting detail? **Maintaining one shared in-memory store and proper domain/service/query/console boundaries.** Recreating a store per menu choice, letting a query directly read storage, or moving validation into the UI would break the application regardless of sorting correctness.

2. Which Copilot suggestion did you reject as over-engineering, and why? **Making conflict checking atomic for concurrent requests.** Copilot presented it as optional, not a current defect; the assessed interface is a single-threaded console and the baseline has no concurrency requirement, so extra locking/transactions would be unnecessary scope expansion.

3. How did you prove cancelled appointments remain retrievable and listable in the same session? **Manual menu run:** cancel A1, then find A1 and observe `cancelled`. **Automated workflow:** assert cancellation returns the same object, `find_appointment('A1') is a1`, default practitioner listing includes A1, explicit `CANCELLED` includes it and `SCHEDULED` excludes it; test a new booking in the freed D1 slot.

## G. Ten formative answers

1. What makes `select_appointments` pure, and what side effect breaks purity? It uses only supplied arguments and returns a new result without changing inputs or performing I/O. Calling `appointments.sort()` on the caller's list, printing or modifying appointment statuses would break purity.

2. Which explicit inputs are needed, and why avoid a global store? A list of `Appointment` objects, practitioner ID, and optional `AppointmentStatus`. A global store would hide dependencies, reduce reuse and make results depend on unrelated state.

3. How can a new list reuse `Appointment` objects safely? Create a new container with `sorted()`/filtering while retaining object references without assigning to their fields. The query reads objects; guarded status changes remain in domain/service operations.

4. Why use a named key, and what breaks equal-time ties? `appointment_sort_key` makes ordering reusable/testable; sort by `(date_time, appointment_id)`, so the appointment ID breaks identical-time ties.

5. How do default and explicit status filters differ? `status=None` includes all statuses, including CANCELLED/COMPLETED. A supplied `AppointmentStatus` returns only matching appointments; a no-match result is `[]`.

6. How do empty, unknown practitioner and invalid filter cases differ? A registered practitioner with no matches returns a fresh `[]`; an unknown valid ID raises `LookupError`; blank/wrong-type IDs or a non-enum status raise `ValueError`.

7. Which console errors recover, and how is unchanged state checked? Invalid choice, duplicate/blank/unknown IDs, bad calendar input, booking conflict, repeated cancellation and invalid status show an error and return to the menu. Assert store lists/identities and absent rejected IDs remain unchanged, then perform a valid action afterward.

8. What is data integrity for registered participants, conflicts and history? Appointments reference the actual registered participant objects; unique IDs are enforced; only exact simultaneous SCHEDULED bookings for the same practitioner conflict; cancelled appointments retain identity/history and release the slot.

9. What is Copilot's review role, and who verifies findings? Copilot offers evidence-linked, severity-ranked suggestions; the human engineer checks the requirements/code/tests, accepts or rejects suggestions, implements warranted changes and reruns tests. It is not proof or a substitute for a teammate's review.

10. How do pure functions and OOP responsibilities work together? Domain objects enforce their own invariants, services orchestrate work with the shared store, pure functions transform supplied collections into new ordered views, and the console alone controls the interaction; UI input should not define domain rules.

## H. Review, completion and common handover

Issues and bounded branches: Stage 9 work is on [`feature/stage9-queries`](https://github.com/deniszimba/st1-assignment-3/tree/feature/stage9-queries), branched from integrated Stage 8 `e8478d6`. **No Stage 9 issue IDs have yet been supplied/verified; create or link bounded issues before final integration if required by the group Git workflow.** Code/test/README commit [`94b9c0b`](https://github.com/deniszimba/st1-assignment-3/commit/94b9c0b), human design commit [`b279da3`](https://github.com/deniszimba/st1-assignment-3/commit/b279da3), Copilot follow-up tests commit [`41beaa1`](https://github.com/deniszimba/st1-assignment-3/commit/41beaa1).

PR/diff and another-member human reviewer: **PENDING** — as of this record, the branch has been pushed but no Stage 9 PR or teammate review has been verified. Add actual PR URL and reviewer after it occurs.

Review responses and Copilot comparison: Copilot findings, human decisions and resulting four passing follow-up tests are documented in E. **PENDING** — record the actual teammate's feedback, any response/change and review timing; do not claim approval in advance.

Integrated common Stage 9 SHA: **PENDING merge and verification.** This is not yet an integrated `main` SHA.

Full regression command, working directory, actual count/result and evidence: From `project/`, `python -m pytest -q` → **74 passed in 0.12s** on 31 October 2026 (local VS Code terminal screenshot). Re-run after human review and after merge; add the final verified integrated result here.

README run instructions and scope/limitations: [`project/README.md`](../project/README.md) documents `python main.py`, `python main.py --interactive`, `python -m pytest -q`, menu choices, status input, session-only data and unsupported features.

Unresolved issues and support/action: Stage 9 branch work and tests are complete locally and pushed, but PR review/merge, integrated-SHA recording and final handover verification remain open. Stage 8 preparer asset and record clean-up are the Stage 8 owner's separate follow-up; do not accidentally include or alter those files on this Stage 9 branch.

UG common candidate / PG future branch plan: The four members follow the UG pathway 6 → 7 → 8 → 9 → 12. After Stage 9 peer review and merging, preserve the integrated common `main` SHA for Stage 12. PG Stages 10/11 are not required for this group.

- [x] Query contracts, purity, new lists and named-key ordering verified.
- [x] Service empty/unknown/invalid cases and cancellation history verified.
- [x] Every console command and invalid-input recovery demonstrated in scripted real-menu tests; key registration/booking/cancellation/lookup operations additionally exercised manually.
- [x] Query and workflow tests plus all previous tests pass; actual local evidence recorded.
- [ ] Human design, Copilot critique, **teammate review** and integration recorded honestly (design/Copilot done; teammate review/merge pending).
- [x] Reflections and ten formative responses completed in this record.
- [x] README updated; earlier Stage 6–8 source, tests and records preserved on this branch.
- [ ] Common SHA protected for UG Stage 12 (pending PR review, merge, and post-merge testing).

No persistence, rescheduling or assurance implementation is part of Stage 9. UG: 6→7→8→9→12. PG: 6→7→8→9→10→11→12. Mixed groups keep one repository and protect the common candidate.
