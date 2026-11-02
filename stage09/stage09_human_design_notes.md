
# Stage 9 — Human Design Notes

Prepared before the Stage 9 GitHub Copilot review. The initial implementation and tests were completed before this consolidated note.

## A3 Responsibility violations

| Conceptual case | Violation | Correct boundary and reason |
|---|---|---|
| Appointment.cancel reads input | Domain logic would depend on user interaction. | The console collects input; Appointment.cancel handles the guarded status change. |
| Service prints/reads the menu | The service would mix business operations with presentation. | The console handles menus while services coordinate domain operations. |
| Query sorts its source in place | Changing the supplied collection breaks purity. | Use sorted() to return a new list without changing the source. |
| Store prints Appointment saved | Data storage would produce a user-interface side effect. | The store manages objects; the console displays confirmation. |

## A4 Sorting comparison

`appointments.sort(key=appointment_sort_key)` changes the original list and returns None.

`result = sorted(appointments, key=appointment_sort_key)` creates a new sorted list without modifying the source.

To check for mutation, save `original_order = list(appointments)` before sorting and assert `appointments == original_order` afterwards. Also check `result is not appointments`.

The score example produces:

`[('Chen', 5), ('Ali', 8), ('Bea', 8)]`

The original scores list remains unchanged. Passing `key=score_key` supplies the function for sorting; calling `score_key()` immediately would not provide the required function.

## A5 Cancellation and retained history

Cancellation changes the existing appointment's status to CANCELLED rather than deleting it. The same stored object must remain retrievable through lookup and all-status practitioner listing.

An explicit SCHEDULED filter must exclude a cancelled appointment. The cancellation also releases that practitioner's time slot for a new booking.

## B. Human design and contracts

Our design uses the existing domain objects and shared SmartCareDataStore. Services validate registration and coordinate operations. Pure queries process explicitly supplied appointments. The console handles user interaction and converts status text into AppointmentStatus values.

| Requirement | Input / session data | Responsible operation | Expected result or error | Test / evidence |
|---|---|---|---|---|
| QRY-01 | Appointment list, practitioner ID | select_appointments | Only matching practitioner appointments | test_only_requested_practitioner_and_order |
| QRY-02 | Optional AppointmentStatus | select_appointments | Default all statuses; explicit enum filtering | test_each_explicit_status |
| QRY-03 | Appointment date/time and ID | appointment_sort_key | Ascending date/time, then ID | test_sort_key_uses_datetime_then_id |
| QRY-04 | Registered practitioner ID and status | AppointmentService listing | Empty list for no matches, LookupError for unknown ID, ValueError for invalid inputs | test_listing_validation_and_empty_results |
| FP-01 | Explicit query arguments | queries.py | Repeatable results without hidden state or I/O | test_fresh_list_and_repeatability; code inspection |
| FP-02 | Source appointment list | select_appointments | Fresh result list; source and objects unchanged | test_source_and_objects_unchanged |
| FP-03 | Named sorting function | appointment_sort_key | Reusable key actually used by sorting | test_query_uses_named_sort_key |
| UI-01 | Valid menu commands | console.run_menu | Registration, lookup, booking, cancellation and listing | test_console_complete_workflow |
| UI-02 | Invalid menu inputs | console.run_menu | Show meaningful errors, recover and continue | test_console_error_recovery |
| FR-01–03 | Patient and practitioner details | Domain, services, store | Validated registration and lookup | Existing service tests and workflow tests |
| FR-04–06 | Registered objects, appointment IDs and times | Domain and AppointmentService | Valid booking, conflict rejection and guarded cancellation | test_complete_service_workflow |
| FR-07–09 | Appointment identity, status and history | Domain, store, service and query | Retain cancellation history and enforce required appointment rules | test_complete_service_workflow |

### Validation and integrity decisions

- A known practitioner with no appointments returns a new empty list.
- An unknown practitioner raises LookupError.
- An invalid or blank practitioner ID raises ValueError.
- A non-enum status supplied directly to the service raises ValueError.
- The console converts valid status text into AppointmentStatus; blank means all.
- Appointments reference the actual registered Patient and Practitioner objects.
- Duplicate IDs, failed bookings and rejected cancellation must not partially change stored state.
- Only a SCHEDULED appointment may be cancelled.
- Different practitioners may have appointments at the same time.
- Cancelled appointments remain accessible during the current session.
- All records are intentionally lost when the application exits.

### Human verification before Copilot

Our latest local full-suite run reported 70 passing tests in 0.18 seconds.

Passing tests support the tested behaviour, but they do not establish that every input has been covered or prove purity without code inspection.

Copilot will be asked to review the actual implementation and tests. Its suggestions will be evaluated against the requirements and observed evidence, not accepted automatically.
