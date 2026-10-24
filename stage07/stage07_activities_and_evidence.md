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
| [complete] | [complete] | [complete] | [complete] | [complete] | [complete] |

## M Contribution Evidence

Record actual work in test design, implementation, review, traceability, diagnosis, necessary fixes and integration. Do not include confidential peer ratings.

| Member | Actual contribution | Evidence link |
|---|---|---|
| [complete] | [complete] | [complete] |

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

Tested Stage 7 main SHA: [complete]
Full-suite result: [complete]
Unresolved defects and effect on baseline: [complete or none]
Clean working tree and integration evidence: [complete]
Stage 8 handover status: [complete; no Stage 8 work assigned]
All tutorial/formative responses and traceability/Copilot decisions complete: [confirm]
