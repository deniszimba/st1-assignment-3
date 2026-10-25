# Stage 7 Testing and Verification Record

Group/tutorial: Wednesday 4.30 - 6.30 semester 2  Members/cohorts: Tari Ganas Ahron Singh
Requirements baseline: SmartCare A3 Requirements Baseline 2026, revision 2.
Use the same project/. Link actual evidence; keep responses concise. Blank fields are for your group. Copy rows only as needed.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage07/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions.

## A Tutorial Activities

### Activity 1 Requirement to test

For each requirement, propose one positive test, one negative test and the key assertion.

| Requirement | Positive test | Negative test | Key assertion |
|---|---|---|---|
| FR-01 Register patient | Register a patient with a new valid ID and name | Try to register another patient with the same ID | The valid patient is stored; the duplicate raises ValueError and the original record remains unchanged. |
| FR-05 Prevent practitioner conflict | Book the same practitioner at two different times. | Try to book the same practitioner at the exact same date and time. | The different-time bookings succeed; the conflicting booking raises ValueError and is not stored. |
| FR-06 Cancel appointment | Cancel an appointment that has SCHEDULED status. | Try to cancel the same appointment again. | The first cancellation changes the status to CANCELLED; the repeated cancellation raises ValueError. |
| FR-07 Retain cancelled history | Cancel an appointment and then find it again. | Check that a rejected repeated cancellation does not delete the appointment. | The same appointment remains stored with CANCELLED status. |

### Activity 2 Strong or weak assertion

For each, select Strong for stated behaviour or Weak/unclear and explain why. State the behaviour and limits.

`assert True`
Judgement: Weak/unclear  Why: it always passes and does not check any program behaviour

`assert appointment is not None`
Judgement: Weak/unclear  Why: It proves only that an object exists, it dosent check if the appointment is correct or not and dosent have the expected values

`assert appointment.status == AppointmentStatus.CANCELLED`
Judgement: Strong for stated behaviour Why: Because it always directly checks that cancllation changed the appointment status. It does not prove that the appointent remains stored.

`assert len(results) > 0`
Judgement: Weak/unclear Why: It only proves that one result exists not all it does not check weather the correct records were returned.

`assert data_store.find_appointment('A1') is appointment`
Judgement: Strong for stored-object identity. Why: It proves that looking up A1 returns the exact same appointment object A separate assertion is needed to check its status.

### Activity 3 Boundary thinking

Design boundary or edge cases for blank identifiers, whitespace-only names, same-time practitioner bookings, cancelled appointments and invalid status transitions.
For each input/state, expected result and supporting contract:

Blank identifiers ("" or "   "): raise ValueError because identifiers must contain non-whitespace text.

Whitespace-only names ("   "): raise ValueError because names are trimmed and cannot be blank.

Same practitioner booked at the exact same date and time: raise ValueError and leave the stored appointments unchanged because a practitioner cannot have conflicting scheduled appointments.

Different practitioners booked at the same time: allow both bookings because the conflict rule applies only to the same practitioner.

Cancelled appointment: keep it stored with CANCELLED status because cancelled appointment history must be retained.

Cancelling a CANCELLED or COMPLETED appointment: raise ValueError and leave its status unchanged because only a SCHEDULED appointment can be cancelled.

### Activity 4 Critique GitHub Copilot tests

GitHub Copilot generates five tests, all of which pass. Two only assert that objects are not None, one asserts True, and two assume SMS notifications exist. Identify what is wrong and rewrite the test intentions.

| Candidate | What is wrong | Rewritten test intention |
|---|---|---|

| 1 | Only checking that an object is not none does not prove it is the correct paitent | Register a paitnet, find it by ID and assert that the returned object is the same stored paitient with the expected value  |

| 2 | Only checking that an appointmnet is not none does not prove it was booked right | Book an appointment and assert that it is stored with the registerd paitnet, practitioner, date and SCHEDULED status |

| 3 | make sure that true always passes and does not test any behaviour | Cancel a scheduled appointment and make sure that its status changes to CANCELLED. |

| 4 | SMS notifications are not part of the SmartCare requirements, so this test invents behaviour | Attempt a conflicting booking and assert that it raises ValueError and does not change the stored appointments |

| 5 | SMS notifications are not implemented or required, so this test cannot verify an approved requirement | Cancel an appointment and assert that the same appointment remains retrievable with CANCELLED status. |

### Tutorial exit question

Why can 100% code coverage coexist with poor software verification?
100% code coverage only shows that every line of code was executed. It does not prove that the tests checked the correct requirements, used meaningful assertions, covered important input boundaries or detected incorrect results. Weak tests can execute all the code while proving very little.

## B Requirement to Test Traceability Matrix

Assign TEST IDs before implementation or generation. Use canonical AC IDs with their actual meaning; quote supporting revision 2 contracts when no canonical AC is assigned. Blank-ID validation is not AC-01.2. Identify supplied versus student-authored evidence.

| Requirement | Acceptance criterion | Test ID | Test type | Test name / location | Expected behaviour | Result / observed status | Supplied or student-authored |
|---|---|---|---|---|---|---|---|

| FR-01 | AC-01.1: Valid patient data with an unused ID is stored | T7-S01 | Service | test_register_patient_stores_valid_patient in tests/test_services.py | The paitent is then stored sucsessfully | Passed | Tari - stage 7

| FR-01 | AC-01.2: An existing patient ID is rejected| T7-S02 | Service | test_duplicate_patient_id_is_rejected_without_change in tests/test_services.py | Value error is then raised and the original patient remains stored | Passed | Tari - stage 7

| FR-03 | Practitioner ID, name and specialty cannot be blank. | T7-D02 | Domain | test_practitioner_rejects_blank_required_fields in tests/test_domain.py | A blank required field raises ValueError | Passed | Tari - stage 7

| FR-04 | A new appointment starts as SCHEDULED. | T7-D03 | Domain | test_new_appointment_starts_scheduled in tests/test_domain.py | The new appointment has SCHEDULED status | Passed | Tari - stage 7

| FR-05 | AC-04.1: The same practitioner at the same time conflicts. | T7-S03 | Service | test_same_practitioner_exact_time_is_rejected in tests/test_services.py | The conflicting booking raises ValueError. | Passed | Tari - stage 7

| FR-05 | AC-04.2: Different practitioners can use the same time. | T7-S04 | Service | test_different_practitioner_same_time_is_allowed in tests/test_services.py | Both appointments are stored | Passed | Tari - stage 7

| FR-06 | AC-05.1: Cancelling a scheduled appointment changes it to CANCELLED. | T7-D04 | Domain | test_cancel_changes_status in tests/test_domain.py | Status changes to CANCELLED | Passed | Tari - stage 7

| FR-06 | AC-05.3: Repeated cancellation is rejected. | T7-D05 | Domain | test_repeated_cancel_is_rejected_without_change in tests/test_domain.py | The second cancellation raises ValueError | Passed | Tari - stage 7

| FR-06 | Only a SCHEDULED appointment can be cancelled. | T7-D06 | Domain | test_completed_appointment_cannot_be_cancelled in tests/test_domain.py | Cancelling a completed appointment raises ValueError. | Passed | Tari - stage 7

| FR-07 | AC-05.2: Cancelled history remains retrievable. | T7-S05 | Service | test_cancelled_appointment_is_kept_in_history in tests/test_services.py | The cancelled appointment remains stored. | Passed in the 33-test baseline | Passed | Tari - stage 6

| FR-01 | Required-ID contract | T7-D01 | Domain | test_blank_patient_id_is_rejected in tests/test_domain.py | A blank patient ID raises ValueError | Passed | Tari |

| FR-04 | Appointment validation contract | T7-D07 | Domain | test_appointment_rejects_invalid_values in tests/test_domain.py | Invalid appointment values raise ValueError | Passed | Tari |

| FR-05 | Revision 2 conflict rule | T7-S06 | Service | test_cancelled_appointment_releases_practitioner_slot in tests/test_services.py | A cancelled booking does not occupy the time slot | Passed | Tari |

| FR-01 | Validation contract: "IDs are strings, trimmed, non-blank"; required names are non-blank | T7-D08 | Domain | test_valid_patient_stores_trimmed_values in tests/test_domain.py | A valid Patient keeps its trimmed ID and name | Passed | Ahron - stage 7 follow-up |

| FR-03 | Validation contract: IDs trimmed; required name and specialty non-blank | T7-D09 | Domain | test_valid_practitioner_stores_trimmed_values in tests/test_domain.py | A valid Practitioner keeps its trimmed ID, name and specialty | Passed | Ahron - stage 7 follow-up |

| FR-01 | Validation contract: "Required names and specialty are non-blank" | T7-D10 | Domain | test_blank_patient_name_is_rejected in tests/test_domain.py | A blank or spaces-only patient name raises ValueError | Passed | Ahron - stage 7 follow-up |

| FR-04 | Datetime contract: "local naive datetime values at minute precision"; "Timezone-aware values and nonzero seconds/microseconds are invalid" | T7-D11 | Domain | test_appointment_rejects_seconds_or_timezone in tests/test_domain.py | Seconds, microseconds or a timezone raise ValueError | Passed | Ahron - stage 7 follow-up |

| FR-04 | AC-03.2: Booking an unknown patient or practitioner is rejected | T7-S07 | Service | test_booking_unknown_practitioner_is_rejected_without_change in tests/test_services.py | LookupError is raised and the stored appointments are unchanged | Passed | Ahron - stage 7 follow-up |

## C Test Design

Use descriptive test names such as test_cancel_changes_status() or test_blank_patient_id_is_rejected(). Explain what new evidence each case adds.

| Test ID | Requirement | Acceptance criterion | Positive / Negative / Boundary | Test intention | Observable result expected | Added evidence beyond supplied tests |
|---|---|---|---|---|---|---|

| T7-S01 | FR-01 | AC-01.1 | Positive | Register a valid patient. | The same patient is stored and returned. | Directly checks successful patient storage. |

| T7-S02 | FR-01 | AC-01.2 | Negative | Register the same patient ID twice. | ValueError is raised and the original remains stored. | Checks that duplicates cannot overwrite data. |

| T7-D01 | FR-01 | Required-ID contract | Boundary | Create a patient with a blank ID. | ValueError is raised. | Directly checks domain validation. |

| T7-D02 | FR-03 | Required-field contract | Boundary | Create a practitioner with a blank required field. | ValueError is raised. | Checks practitioner validation. |

| T7-D03 | FR-04 | Initial-status contract | Positive | Create a valid appointment. | Its status is SCHEDULED. | Checks the domain’s starting status. |

| T7-S03 | FR-05 | AC-04.1 | Negative / Boundary | Book the same practitioner at the same time. | ValueError is raised and the original booking remains. | Checks the exact conflict rule. |

| T7-S04 | FR-05 | AC-04.2 | Positive / Boundary | Book different practitioners at the same time. | Both bookings are stored. | Checks the permitted alternative. |

| T7-D04 | FR-06 | AC-05.1 | Positive | Cancel a scheduled appointment. | Status becomes CANCELLED. | Checks the valid cancellation transition. |

| T7-D05 | FR-06 | AC-05.3 | Negative | Cancel an appointment twice. | The second attempt raises ValueError. | Checks the repeated-cancellation guard. |

| T7-D06 | FR-06 | Status-guard contract | Negative | Cancel a completed appointment. | ValueError is raised and status stays COMPLETED. | Checks that only scheduled appointments can be cancelled. |

| T7-S05 | FR-07 | AC-05.2 | Positive | Find an appointment after cancellation. | The same cancelled appointment remains stored. | Existing Stage 6 test proves retained history. |

| T7-D07 | FR-04 | Appointment validation contract | Negative | Create appointments using invalid patient, practitioner, date or status values. | ValueError is raised. | Checks appointment input validation. |

| T7-S06 | FR-05 | Revision 2 conflict rule | Boundary | Cancel a booking and reuse the same practitioner and time. | The new booking succeeds and both appointments remain stored. | Checks that a cancelled booking does not occupy the slot. |

| T7-D08 | FR-01 | Validation contract (trimmed IDs, required name) | Positive / Boundary | Create a Patient with spaces around the ID and name. | The stored ID is "P1" and the name is "Alex Example". | No earlier test checked a valid Patient's stored values directly. |

| T7-D09 | FR-03 | Validation contract (trimmed ID, required name and specialty) | Positive / Boundary | Create a Practitioner with spaces around every field. | The stored ID, name and specialty are trimmed. | No earlier test checked a valid Practitioner's stored values directly. |

| T7-D10 | FR-01 | Validation contract (required names non-blank) | Negative / Boundary | Create a Patient with an empty and a spaces-only name. | ValueError is raised for each. | Earlier tests only checked a blank patient ID, not a blank name. |

| T7-D11 | FR-04 | Datetime contract (naive, minute precision) | Negative / Boundary | Create an Appointment at 9:00:30, at 9:00 plus microseconds, and at 9:00 UTC. | ValueError is raised for each. | Earlier tests only used a non-datetime value; this checks the precise datetime boundary. |

| T7-S07 | FR-04 | AC-03.2 | Negative | Book a registered patient with an unknown practitioner ID. | LookupError is raised and only the original appointment remains. | The supplied test only covered an unknown patient. |

## D Arrange Act Assert Record

Arrange test data; act on one meaningful behaviour; assert the required observable outcome. Use the specific current exception with pytest.raises where needed.

| Test ID | Arrange | Act | Assert | Why meaningful / why assertion proves criterion |
|---|---|---|---|---|

|  T7-S01 | Create a fresh store and PatientService. | Register a valid patient. | The returned patient is the same object found in the store. | Proves that valid registration stores the patient. |

| T7-S02 | Register patient P1 in a fresh store. | Try to register P1 again. | ValueError is raised and only the original patient remains. | Proves duplicate registration is rejected without overwriting data. |

| T7-D01 | Prepare a blank patient ID. | Construct a Patient. | pytest.raises(ValueError) catches the rejection. | Proves that patient IDs cannot be blank. |

| T7-D02 | Prepare blank practitioner ID, name or specialty values. | Construct a Practitioner for each case. | Each case raises ValueError. | Proves all required practitioner fields are validated. |

| T7-D03 | Create valid patient, practitioner and date/time values. | Construct an Appointment. | Its status is AppointmentStatus.SCHEDULED. | Proves the required initial appointment status. |

| T7-S03 | Store one scheduled appointment for a practitioner. | Book the same practitioner at the same time. | ValueError is raised and only the original appointment remains. | Proves the exact conflict rule and unchanged state. |

| T7-S04 | Register one patient and two practitioners. | Book both practitioners at the same time. | Both appointments are stored with the correct practitioners. | Proves different practitioners may use the same time. |

| T7-D04 | Create a scheduled appointment. | Call cancel(). | Status becomes AppointmentStatus.CANCELLED. | Proves the valid cancellation transition. |

| T7-D05 | Create and cancel an appointment once. | Call cancel() again. | ValueError is raised and status remains CANCELLED. | Proves repeated cancellation is rejected without changing state. |

| T7-D06 | Create an appointment with COMPLETED status. | Call cancel(). | ValueError is raised and status remains COMPLETED. | Proves only scheduled appointments can be cancelled. |

| T7-S05 | Create and store a scheduled appointment. | Cancel it through AppointmentService, then find it again. | Lookup returns the same appointment with CANCELLED status. | Proves cancelled history remains stored and retrievable. |

| T7-D07 | Prepare invalid patient, practitioner, date and status values. | Construct an Appointment with each invalid value. | Each case raises ValueError. | Proves invalid appointment values are rejected. |

| T7-S06 | Create and cancel a scheduled appointment. | Book the same practitioner at the same time again. | The new booking succeeds, the first stays CANCELLED and both remain stored. | Proves a cancelled booking releases the time slot without deleting history. |

| T7-D08 | Prepare an ID and name with surrounding spaces. | Construct a Patient. | patient_id is "P1" and name is "Alex Example". | Proves valid patient data is stored, using the trimming rule. |

| T7-D09 | Prepare an ID, name and specialty with surrounding spaces. | Construct a Practitioner. | All three stored values are trimmed. | Proves valid practitioner data is stored, using the trimming rule. |

| T7-D10 | Prepare an empty and a spaces-only name (parametrised). | Construct a Patient with each. | pytest.raises(ValueError) for each case. | Proves the required-name rule, which no earlier test checked. |

| T7-D11 | Prepare a patient and practitioner, and three invalid datetimes (parametrised). | Construct an Appointment with each datetime. | pytest.raises(ValueError) for each case. | Proves the minute-precision, timezone-free datetime rule at its exact boundary. |

| T7-S07 | Fresh store with one SCHEDULED appointment A1. | Book A2 for P1 with unknown practitioner D9. | pytest.raises(LookupError); the store still lists only A1, still SCHEDULED. | Proves AC-03.2 for practitioners and that the rejected booking left state unchanged. |

## E Domain Test Evidence

Cover Patient/Practitioner construction and validation; Appointment construction, initial status, cancellation and illegal/repeated transitions. Preserve the four reference intentions described in handout Part C.

| Test ID | Behaviour | Test file/function | Result |
|---|---|---|---|

| T7-D01 | Blank patient ID is rejected | tests/test_domain.py::test_blank_patient_id_is_rejected | Passed |

| T7-D02 | Blank practitioner fields are rejected | tests/test_domain.py::test_practitioner_rejects_blank_required_fields | Passed |

| T7-D03 | New appointment starts as SCHEDULED | tests/test_domain.py::test_new_appointment_starts_scheduled | Passed |

| T7-D04 | Cancellation changes status | tests/test_domain.py::test_cancel_changes_status | Passed |

| T7-D05 | Repeated cancellation is rejected | tests/test_domain.py::test_repeated_cancel_is_rejected_without_change | Passed |

| T7-D06 | Completed appointment cannot be cancelled | tests/test_domain.py::test_completed_appointment_cannot_be_cancelled | Passed |

| T7-D07 | Invalid appointment values are rejected | tests/test_domain.py::test_appointment_rejects_invalid_values | Passed |

| T7-D08 | Valid Patient keeps trimmed ID and name | tests/test_domain.py::test_valid_patient_stores_trimmed_values | Passed |

| T7-D09 | Valid Practitioner keeps trimmed ID, name and specialty | tests/test_domain.py::test_valid_practitioner_stores_trimmed_values | Passed |

| T7-D10 | Blank or spaces-only patient name is rejected | tests/test_domain.py::test_blank_patient_name_is_rejected | Passed (2 cases) |

| T7-D11 | Seconds, microseconds or timezone are rejected | tests/test_domain.py::test_appointment_rejects_seconds_or_timezone | Passed (3 cases) |
## F Service Test Evidence

Use fresh shared SmartCareDataStore state, registered objects and completed Stage 6 services.

| Test ID | Behaviour | Requirement / criterion | Test file/function | Result |
|---|---|---|---|---|

| T7-S01 | Valid patient registration is stored | FR-01 / AC-01.1 | `tests/test_services.py::test_register_patient_stores_valid_patient` | Passed |

| T7-S02 | Duplicate patient ID is rejected without changing the original | FR-01 / AC-01.2 | `tests/test_services.py::test_duplicate_patient_id_is_rejected_without_change` | Passed |

| T7-S03 | Same practitioner at the same time is rejected | FR-05 / AC-04.1 | `tests/test_services.py::test_same_practitioner_exact_time_is_rejected` | Passed |

| T7-S04 | Different practitioners at the same time are allowed | FR-05 / AC-04.2 | `tests/test_services.py::test_different_practitioner_same_time_is_allowed` | Passed |

| T7-S05 | Cancelled appointment remains stored | FR-07 / AC-05.2 | `tests/test_services.py::test_cancelled_appointment_is_kept_in_history` | Passed |

| T7-S06 | Cancelled appointment releases the practitioner’s time slot | FR-05 / Revision 2 conflict rule | `tests/test_services.py::test_cancelled_appointment_releases_practitioner_slot` | Passed |

| T7-S07 | Booking an unknown practitioner is rejected without change | FR-04 / AC-03.2 | `tests/test_services.py::test_booking_unknown_practitioner_is_rejected_without_change` | Passed |
## G Negative and Boundary Cases

Connect cases to actual contracts and verify unchanged state after rejection.

| Behaviour | Boundary/invalid input | Expected result | Test ID |
|---|---|---|---|

| Required fields | Empty or spaces-only patient or practitioner details | `ValueError` is raised and no invalid object is created | T7-D01, T7-D02 |

| Appointment values | Invalid patient, practitioner, date or status | `ValueError` is raised | T7-D07 |

| Patient registration | A duplicate ID with extra spaces | `ValueError` is raised and the original patient stays unchanged | T7-S02 |

| Booking conflict | Same time with the same practitioner, then with a different practitioner | Same practitioner is rejected; different practitioner is allowed | T7-S03, T7-S04 |

| Cancelled booking slot | Book the same practitioner and time after cancellation | The new booking succeeds and both appointments remain stored | T7-S06 |

| Appointment cancellation | Cancel an already cancelled or completed appointment | `ValueError` is raised and the status stays unchanged | T7-D05, T7-D06 |

| Required names | Empty or spaces-only patient name | `ValueError` is raised | T7-D10 |

| Trimmed fields | ID, name and specialty with surrounding spaces | Values are stored trimmed | T7-D08, T7-D09 |

| Appointment time | Seconds, microseconds or a timezone on the datetime | `ValueError` is raised | T7-D11 |

| Booking participants | Registered patient with an unknown practitioner ID | `LookupError` is raised and the stored appointments are unchanged | T7-S07 |

## H GitHub Copilot Test Design

Select ONE real acceptance criterion. Complete human-first fields before using Copilot. Do not require an accepted generated test.

Requirement: FR-05 Prevent practitioner conflict
Acceptance criterion: AC-04.1 and AC-04.2 quote: "Conflict means the same practitioner, exact datetime and an existing SCHEDULED appointment. A different practitioner at the same time is allowed, and a cancelled booking does not occupy the slot.”
Behaviour to test: Reject an exact time conflict without changing stored appoinmtnets Allow a different practitioner or a cancelled slot.
Human first test idea/categories: Test the same practitioner at the exact same time, a different practitioner at the same time, and reuse of a cancelled slot.
Prompt and purpose: Ask Copilot for FR-05 test ideas and compare them with my own test ideas.

For each significant candidate, copy this entry as needed:
- Copilot test idea/candidate: Reject the same practitioner at the exact same time without changing the original appointment
- What it claims to verify: The conflict raises ValueError and stored data remains unchanged.
- Requirement trace: FR-05 / AC-04.1
- Assertion quality: Strong, but some suggested assertions were repetitive.
- Human critique: The stored list assertion already proves that A2 was not saved. I kept the test focused and added a check that the original status remains SCHEDULED.
- Decision: Modify
- Reason: The status assertion adds useful unchanged state evidence without copying unnecessary assertions.
- Final test reference if accepted/modified: `tests/test_services.py::test_same_practitioner_exact_time_is_rejected`
- Actual verification result: Passed, 1 test passed.

- Copilot test idea/candidate: Allow a different practitioner at the same time.
- What it claims to verify: Both appointments can be stored at the same time when the practitioners differ.
- Requirement trace: FR-05 / AC-04.2
- Assertion quality: Strong and checks the stored appointments.
- Human critique: This duplicates the human written T7-S04 test.
- Decision: Reject
- Reason: It adds no new evidence because the test already exists.
- Final test reference if accepted/modified: Not retained.
- Actual verification result: Copilot candidate not run. Existing T7-S04 passed in the full suite.

- Copilot test idea/candidate: Allow reuse of a practitioner’s time after cancellation.
- What it claims to verify: A cancelled appointment does not occupy the time slot.
- Requirement trace: FR-05 / Revision 2 conflict rule
- Assertion quality: Strong and checks both appointment statuses and storage.
- Human critique: This duplicates the human written T7-S06 test.
- Decision: Reject
- Reason: It adds no new evidence because the test already exists.
- Final test reference if accepted/modified: Not retained.
- Actual verification result: Copilot candidate not run. Existing T7-S06 passed in the full suite.

Before accepting: traces to a requirement/criterion; can fail for the right reason; assertion checks required behaviour; no invented business rule; no unnecessary private implementation dependence. Reject/modify weak assertions, invented requirements, excessive mocking, duplicates, wrong exceptions, obsolete architecture and unnecessary dependencies.

## I Weak Copilot Test Reflection

Which Copilot-generated test looked convincing but was weak? One of the ones that stood out to me were The same practitioner conflict candidate it looked convincing but it repeted the same checks

Why was it weak? It was much longer than it should of been and it basically duplicated my existing human written test

How did you strengthen it? I kept the ValueError and and stored list checks then added an assertion that the original appointment remains SCHEDULED

Accepted / modified / rejected test decisions and evidence: Candidate 1 was modified. Candidates 2 and 3 were rejected as duplicates. See [Section H](#h-github-copilot-test-design). The modified test passed: 1 passed.

## J Regression Run

Run python -m pytest from project/. Retain all accumulated tests. Record the tested SHA accurately.

| Command | Working directory | Code SHA | Passed | Failed | Failure summary | Product defect / test defect / unresolved | Evidence and interpretation |
|---|---|---|---|---|---|---|---|
| python3 -m pytest | project/ | 9b422491b8de003eef0517866e26de5a5315e4b1 | 33 | 0 | None | No defect identified | Baseline before Stage 7 changes; all existing tests passed |
| python3 -m pytest | project/ | d7ea23b5c8d2f9dccb0478bd78e3c8b027442be6 | 45 | 0 | None | No defect identified | All Stage 7 and existing regression tests passed |

| python -m pytest | project/ | bda3c29443a86f7e2f746893fe7a1ab871a59022 | 53 | 0 | None | No defect identified | Follow-up tests from the PR #8 review (T7-D08 to T7-D11, T7-S07) added; all accumulated tests retained |

Individual test runs and changed-order independence evidence:
- `python3 -m pytest tests/test_domain.py::test_blank_patient_id_is_rejected`: 1
- `python3 -m pytest tests/test_services.py::test_cancelled_appointment_releases_practitioner_slot`: 1

passed.
- Service test followed by domain test: 2 passed.
- Domain test followed by service test: 2 passed.
- Modified T7-S03 test: 1 passed. 

Optional tutor-led demonstration notes: [optional; leave blank if not used]
A meaningful test should detect a relevant incorrect result. Students do not have to perform the demonstration or submit failure/restoration evidence for assessment. The tutor restores the example and reruns its tests. This is not a Stage 8     fault activity.
Requirement → test → failure/observation → diagnosis → change → verification: [concise links where applicable]

## K What the Suite Still Does Not Prove

What does your test suite still not prove? It still does not prove its performance or existing user behaviour or date persistence after the program closes.

Coverage if used: Not used

Which uncovered areas matter, and why does coverage percentage alone not establish correctness? Performance and persistence are not tested coverage only was shown when which code ran not whether the correct behaviour was checked

Optional fixtures/parametrisation used and why, if any: No new pytest fixtures or parametrisation were used

## L Git and Review Evidence

Use links rather than copying GitHub history. Continue the Stage 6 workflow; no commit/PR count, conflict or individual test quota is imposed.

| Issue/task | Branch | PR | Reviewer | Key feedback | Outcome |
|---|---|---|---|---|---|

| Stage 7 testing and verification | feature/stage7-testing | [PR #8](https://github.com/deniszimba/st1-assignment-3/pull/8) | Ahron Singh (typicalgeezer42) | Ran 45 tests successfully and identified four missing behaviours, recorded in [Issue #9](https://github.com/deniszimba/st1-assignment-3/issues/9). | Approved and merged as `3e5e528049989f6730dcb64ec93ca9cc856318e0` |

| [Issue #9](https://github.com/deniszimba/st1-assignment-3/issues/9) | feature/stage7-missing-tests | [PR #10](https://github.com/deniszimba/st1-assignment-3/pull/10) | Tari Ganas (`tariganas225-bit`) | Ran 53 tests and confirmed T7-D08 to T7-D11 and T7-S07 matched their requirements. The workbook rows went directly to main in `f4b62e9` instead of through PR #10. | Approved and merged as `3f896bc4c8ba4a260f4142e5f283234b91180314` |

## M Contribution Evidence

Record actual work in test design, implementation, review, traceability, diagnosis, necessary fixes and integration. Do not include confidential peer ratings.

| Member | Actual contribution | Evidence link |
|---|---|---|

| Tari Ganas | Designed test cases and IDs, implemented T7-D01 to T7-D07 and T7-S01 to T7-S06, ran targeted, changed-order and full regression tests, evaluated Copilot suggestions, recorded traceability, and reviewed PR #10. | [PR #8](https://github.com/deniszimba/st1-assignment-3/pull/8), [PR #10 review](https://github.com/deniszimba/st1-assignment-3/pull/10) |

| Ahron Singh | Reviewed PR #8, identified missing behaviours, recorded Issue #9, implemented T7-D08 to T7-D11 and T7-S07, added their workbook rows, and verified the 53-test suite. | [PR #8 review](https://github.com/deniszimba/st1-assignment-3/pull/8), [Issue #9](https://github.com/deniszimba/st1-assignment-3/issues/9), [PR #10](https://github.com/deniszimba/st1-assignment-3/pull/10), [commit f4b62e9](https://github.com/deniszimba/st1-assignment-3/commit/f4b62e9) |

## N Formative Questions

1. What question does verification answer?
Verification checks if the software has met its specific requirements

2. What question does validation answer?
Validation is making sute the softwae is actually correct and it meets the users actual needs

3. What is a unit test?
A unit test checks one small part of the program independently.

4. What is a pytest fixture?
A pytest fixture provides reusable test setup data.

5. What is parametrisation in pytest?
Parametrisation runs the same test with different inputs and expected results.

6. What is regression testing?
regression testing is when you check if the existing behaviour still work after changes

7. What does code coverage tell us, and what does it not prove?
Code coverage tells us which code was executed, it does not prove weather the requirements or results are correct

8. What makes an assertion weak?
An assertion is weak when it can pass without proving the required behaviour

9. What is the appropriate role of GitHub Copilot as a test assistant?
Copilot can suggest test ideas but humans must check the requirements assertions and results

10. What is the Stage 7 engineering rule?
Every test must trace to a requirement and detect a relevant incorrect result

## O Stage Completion

Tested Stage 7 main SHA: `3f896bc4c8ba4a260f4142e5f283234b91180314`
Full-suite result: `python3 -m pytest` in `project/`: 53 passed, 0 failed
Unresolved defects and effect on baseline: None
Clean working tree and integration evidence: PR #10 was merged; Tari pulled main and confirmed 53 passed
Stage 8 handover status: Ready; no Stage 8 work started
All tutorial/formative responses and traceability/Copilot decisions complete: Confirmed
