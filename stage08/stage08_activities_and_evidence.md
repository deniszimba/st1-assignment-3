# Stage 8 activities and evidence

UG and PG | One evolving group project | Complete this blank record using the Stage 8 handout.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage08/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. The Stage 8 preparation utility is supplied or run by teaching staff when Stage 8 begins. Follow your tutor’s controlled workflow and the handout. If temporarily supplied, keep it outside the repository in a sibling Stage_8_Assets/ folder; exclude it from Git and the final submission.

Group/tutorial: [complete] Wednesday 4:30 - 6:30, Group 3.
Members and UG/PG cohorts: [complete] Andy Hoang, Denis Zimba, Tari Ganas and Ahron Singh
Record owner / contribution links for each member: [complete]
Owner: ANDY HOANG


Use concise results and accessible artefact links rather than copying entire logs. Keep human-first entries before consulting GitHub Copilot. Link shared evidence once; do not repeat it across sections. No entries below are specimen answers or claimed results.

## A. Tutorial activities

### A.1 Classify all five statements
For each, choose symptom, evidence or hypothesis/opinion, and explain your reason. These are discussion statements, not confirmed diagnoses.
- Appointment disappears after cancellation.
- The data-store removal path is probably being called.
- The failing test shows store.find_appointment('A1') returns None.
- The service layer is badly designed.
- Traceback points to smartcare/services.py line 42 in the example.
The example line number is illustrative; inspect the actual line in your run. The removal hypothesis must be tested against the current project, which has no public delete operation.

Response and reason: [complete]
1. Symptom: “Appointment disappears after cancellation” describes observable behaviour without explaining why it happened.


2. Hypothesis: “The data-store removal path is probably being called” proposes a possible cause without evidence. It is uncertain because the current project has no public delete operation.

3. Evidence: A failing test showing `store.find_appointment('A1')` returns `None` is a concrete observed value. It does not prove why the value is `None`.


4. Hypothesis: “The service layer is badly designed” is a broad judgement without a measurable observation or comparison with a requirement.

5. Evidence: A traceback location provides evidence about the executed path and where the problem surfaced. It does not prove that the referenced line introduced the faulty state.

### A.2 Build a debugging record
Choose the cancelled-history scenario or a same-practitioner/time booking. Before changing code, record expected behaviour, observed behaviour, minimal reproduction, a hypothesis and evidence to inspect. Use a requirement to justify the expectation. Keep the initial hypothesis even if later evidence disproves it.

Response and reason: [complete]
Scenario: F8-02 cancelled appointment history.

Expected behaviour: FR-06, FR-07, FR-08, BR-07 and AC-05.2 require cancellation to retain the same A1 object with the 'CANCELLED' status, therefore both list and lookup operations needs to always find it.

Observed behaviour: At the prepared commit, cancellation changed the A1 to 'CANCELLED' and 'list_appointments()` retained the same object, but `find_appointment('A1')` returned `None`. Service lookup therefore raised `LookupError`.

Minimal reproduction:
1. Create a fresh shared 'SmartCareDataStore'
2. Register patient P1 and practitioner D1.
3. Book appointment A1
4. Cancel A1
5. Inspect A1's status
6. Inspect 'list_appointments()'
7. Call the data-store lookup
8. Call the service lookup
9. Attempt cancellation again. 

Inital hypothesis: The cancellation operation probably changes A1 to `CANCELLED` without deleting it, but `SmartCareDataStore.find_appointment` may be filtering out appointments with `CANCELLED` status. This is plausible because `list_appointments()` still contains the original A1 object while lookup returns `None`. To distinguish this from deletion or replacement, I will compare the original object’s identity with the object in `list_appointments()` and inspect the conditions inside `find_appointment`.

### A.3 Test defect or product defect
A test expects cancelled appointments to be deleted, but FR-07 says history must be retained. What should be changed? Explain why. Also decide whether a test expecting different practitioners at the same time to conflict reflects AC-04.2. Do not assume every failing test is correct.

Response and reason: [complete]
A test expecting a cancelled appointment to be properly deleted has a test defect, as FR-07 and AC-05.2 both require that a cancelled appointment history to be retained. Therefore the correct and most optimal test should assert that cancellation returns and retains the same object with the 'CANCELLED' status. 

A test that expects different practitioners at the same date and time to conflict would also have a test defect under AC-04.2, as the conflict rule applies only to other 'SCHEDULED' appointments for the same practitioner at the exact same date and time. But different practitioners at that time are permitted. 

### A.4 Refactoring smell hunt
Consider a hypothetical 70-line AppointmentService method containing duplicate status strings, direct collection manipulation, printing, validation and four nested conditionals. Identify the smells and propose small refactorings that preserve required behaviour. The direct collection work replaces the old storage-specific scenario; use the existing SmartCareDataStore boundary. Do not implement an extra architecture.
Classify these proposed changes as refactoring, repair or feature: rename appt to appointment; extract a repeated conflict helper; add rescheduling; restore retained cancellation lookup; replace a magic status string with the existing enum. Explain the behaviour that must remain unchanged.

Response and reason: [complete]
This hypothetical method would contain numerous code smells like:

1. Long method
2. Duplicate status strings
3. Mixed responsibilities
4. Direct collection manipulation
5. Printing inside service logic
6. Repeated validation
7. Deeply nested conditionals

The small behaviour-perserving refactorings within this hypothical code would be:
1. Rename unclear local variables.
2. Replace magic status strings with the already existing 'AppointmentStatus' enum.
3. Extract the genuine repeated conflict logic.
4. Reduce the unnecessary nesting.
5. Keep the already existing 'SmartCareDataStore' boundary.
6. Keep printing at the console boundary.

Classifications:
- Rename `appt` to `appointment`: **refactoring**.
- Extract repeated conflict logic without changing its rule: refactoring.
- Add rescheduling: **feature**.
- Restore retained cancellation lookup: repair.
- Replace a magic status string with the existing enum: refactoring.

Behaviours that must always remain unchanged are valiation, exception categories, object identity, stored collection contents, guarded cancellation, retained histroy and the exact practitioner-conflict rule. 



### A.5 Traceback and hypothesis ranking
Using one actual failure, identify its exception/assertion, expected and observed values, test line, application call path and supporting requirement. List three plausible causes and rank them by fit with the available evidence. For each cause, name a check that could distinguish it from the others. Explain why a traceback alone does not establish the cause.

Response and reason: [complete]
Actual F8-02 failure:

- Assertion: `data_store.find_appointment('A1') is appointment`.
- Expected value: the original cancelled A1 object.
- Observed value: `None`.
- Test location: `tests/test_regressions.py::test_f8_02_cancelled_appointment_remains_retrievable`.
- Application call path: test -> `AppointmentService.cancel_appointment` -> `Appointment.cancel`; later lookup -> `AppointmentService.find_appointment` -> `SmartCareDataStore.find_appointment` -> `None` -> `LookupError`.
- Supporting requirements: FR-07, FR-08 and AC-05.2.

Ranked possible causes:

1. Lookup hides a retained cancelled object. 
   Check: compare `list_appointments()` with `find_appointment('A1')` and inspect the lookup condition.

2. Cancellation deletes or replaces A1. 
   Check: compare the stored object’s identity before and after cancellation.

3. The test expectation is incorrect.  
   Check: compare the expectation with FR-07, FR-08 and AC-05.2.

A traceback establishes the path taken and where a problem surfaced. It does not establish which earlier decision caused the incorrect state.
### A.6 Exit question
Why is changing code immediately after seeing a failure often a poor debugging strategy?

Response and reason: [complete]
Changing code immediately after noticing a failure can destroy helpful evidence, address a symtom rather than the deep rooted cause, hide a defective test or setup problem and could introduce another defect. A proper software engineer should first always reproduce the failure, establish expected behaviour and record a testable hypothesis and inspect evidence that distinguishes them.


Classification responses (1–5, each with reason): [complete] 
1. Symptom: Describes the observed disappearance after cancellation.
2. Hypothesis: Suggests an unverified removal cause.
3. Evidence: Records the actual `None` lookup result.
4. Opinion: Makes a broad claim without supporting evidence.
5. Evidence: Identifies where the failure surfaced, not necessarily its cause.
Tutorial debugging record — expected; observed; reproduction; hypothesis; evidence to inspect: [complete]
Expected: A cancelled appointment remaining stored and retrievable under FR-07 and AC-05.2
Observed: A1 remains listed but lookup returned a 'None'.
Reproduction: Book A1, then cancel it then compare the list and lookup results.
Hypothesis: Lookup filters cancelled appointments, inspect 'find_appointment', object identity and cancellation behaviour. 

Traceback — exception/assertion; expected/observed values; test line; call path; requirement; ranked causes and discriminating checks: [complete]
`test_cancelled_appointment_is_kept_in_history` expected the same A1 object but received `LookupError` at `services.py:137`. Call path: test -> service lookup -> store lookup -> `None`. FR-07 and AC-05.2 require retained history. Ranked causes: lookup filtering, deletion/replacement, or an incorrect test expectation. Compare list identity, inspect lookup conditions and check the requirements.

## B. Stage 7 baseline and safe preparation

- Stage 7 code SHA and requirement baseline: [complete]
Stage 7 tested code SHA `3f896bc4c8ba4a260f4142e5f283234b91180314`; SmartCare A3 Requirements Baseline 2026, revision 2.

- Baseline test command / working directory / observed result / evidence: [complete]
`python3 -m pytest -q` from `project/` passed all 53 accumulated tests before preparation. The utility reported preflight PASS at clean preparation SHA `80a17f921929fd32a8738df9ad44806caa23a6c8`.


- Clean preparation SHA if a record-only commit followed Stage 7: [complete]
`80a17f921929fd32a8738df9ad44806caa23a6c8`.

- Branch and preparer / how teammates obtained this branch: [complete]
Andy Hoang prepared and pushed `debug/stage08`.

- Downloaded tool version, source SHA256 and --check outcome: [complete]
The utility-reported baseline source SHA256 was `b4a1993e878c59a9df5e9055320702b2d318c5b6055bb1693a3afc25cd8fd375`. `--check` reported `preflight PASS`

- --apply and --verify output summaries / artefact references: [complete]
`--apply` reported `PREPARED: F8-01 practitioner conflict; F8-02 retained-history lookup`. Its two diagnostic probes, `test_f8_01_conflict` and `test_f8_02_history`, failed as expected. The utility recorded backup and hash information in `.stage8_faults`. `--verify` reported exactly two expected failures and confirmed that both approved symptom signatures were present.

- Bounded diff inspected and recovery location (not committed): [complete]
The prepared commit changed only `project/smartcare/data_store.py`, with 11 additions and 18 deletions. The utility and its supplied archive were moved outside the repository to `/Users/andyhoang/Stage_8_Assets/` and `/Users/andyhoang/Stage_8_Assets.zip`. Prepared diff: [Stage 8 debug setup](https://github.com/deniszimba/st1-assignment-3/commit/b05c90b760b350ddc01b288c81b8bd1a2e3f89c7).


- Prepared faulty-state commit SHA: [complete]
`b05c90b760b350ddc01b288c81b8bd1a2e3f89c7`.


- Preparation or recovery issues and resolution, if any: [complete]
The first `--check` command was run while the terminal was already inside `project/` but also passed `project` as the target. The utility correctly refused because it searched for the nonexistent nested path `project/project/smartcare/data_store.py`. After returning to the repository root with `cd ..`, `--check`, `--apply` and `--verify` all completed successfully. No restoration or recovery was required.

- Initial prepared full-suite command / result / key failures: [complete]
`python3 -m pytest -q` from `project/` produced `48 passed, 5 failed`. The failures were `test_cancelled_appointment_is_kept_in_history`, `test_repeated_cancellation_rejected_without_change`, `test_same_practitioner_exact_time_is_rejected`, `test_different_practitioner_same_time_is_allowed` and `test_conflict_rule_and_different_practitioner`. All five failures correspond to the two prepared defects.

## C. F8-01 diagnosis and repair

- Symptom / observed behaviour: [complete]
The faulty code allowed for a second appointment for the same practitioner at the exact same time, this caused it to incorrectly reject a different practitiooner at that time.

- Expected behaviour and requirement: [complete]
AC-04.2 requires a conflict only when the same practitioner already has a scheduled appointment at that exact date and time, so that different practitioners can be booked at the same time. 

- Minimal synthetic reproduction steps: [complete]
Register patients P1 and P2 and practitioners D1 and D2. Book A1 for D1 at 09:00, attempt A2 for D1 at 09:00 and then attempt A3 for D2 at 09:00.

- Meaningful failing test path/name and exact relevant failure: [complete]
python3 -m pytest '/Users/andyhoang/st1-assignment-3/project/test_regressions.py'::test_f8_01_practitioner_conflict_rule -v failed with "DID NOT RAISE <class 'ValueError'> 
- Human hypothesis and intended checks: see E, F8-01.
The practitioner comparison may be reversed. Inspect has_practitioner_conflict() and compare the practitioner IDs used in its condition.

- Supported root cause and inspected code/runtime evidence: [complete after diagnosis]
The method used 'practitioner_id != practitioner_id, which detected different practitioners rather than checking if they are the same practitioner.

- Smallest justified fix / diff / why other behaviour is preserved: [complete]
Changed the != to ==, and all other conflict conditions remained unmodifed. 

- Repair SHA / focused verification result: [complete]
- 9059737469c089044d3843bbcf23fe3de67e31a7, and focused test result: 1 passed in 0.01s.
## D. F8-02 diagnosis and repair

- Symptom / observed behaviour: [complete]
A cancelled appointment remained in the 'list_appointments()' but the 'find_appointment("A1") returned none, the service lookup would therefore raise LookupError.

- Expected behaviour and requirement: [complete]
FR-07 and AC-05.2 requires a cancelled appointment to remain stored and retrivable as history, so repeated cancellation must still be rejected

- Minimal synthetic reproduction steps: [complete]
Register P1 and D1, then book A1 then cancel A1 and confirm whether its cancelled or not. Then compare 'list_appointments()' with 'failed_appointments("A1") and then finally attempt cancellation again.

- Meaningful failing test path/name and exact relevant failure: [complete]
python3 -m pytest '/Users/andyhoang/st1-assignment-3/project/test_regressions py'::test_f8_02_cancelled_appointment_remains_retrievable -v failed as "find_appointment("A1") returned None instead of the original appointment.

- Human hypothesis and intended checks: see E, F8-02.
The lookup method may filter cancelled appointments. Compare the stored object’s identity before and after cancellation and inspect find_appointment().

- Supported root cause and inspected code/runtime evidence: [complete after diagnosis]
The 'find_appointment' required 'appointment.status.value != "cancelled"' This condition hid cancelled appointments despite the fact that appointment remained stored.

- Smallest justified fix / diff / why other behaviour is preserved: [complete]
Remove only the cancelled-status condition. Blank-ID validation, ID matching, object identity and unknown-ID behaviour remain unchanged.

- Repair SHA / focused verification result: [complete]
bac6afe36e5dfeb881a9561f968142c16906d154 and focused test result: 1 passed in 0.01s. The full suite produced 55 passed in 0.04s, and the repair was pushed successfully.
## E. Human-first hypotheses

Complete both entries BEFORE Copilot. C/D supply observed/expected/reproduction/test; retain those initial facts and link them here.


### F8-01 human entry
Likely cause and why plausible: [complete]
The practitioner-ID comparison within 'has_practitioner_conflict() may be reversed, this is a possible outcome as the system allowed the same practitioner to be booked twice at the same time whilst still incorrectly rejecting a different practitioner. These opposite results heavily showcase that the equality comparison was reversed.

Evidence intended to inspect / competing explanation / discriminating check: [complete]
By inspecting the practitioner-ID condition within the 'has_practitioner_conflict()', it can be checked whether the stored practitioner is compared using the '==' or '!=', and by reproducing bookings for the same and different practitiners whilst keeping the same date, time and status unchanged this will showcase whether changing only the practitioner ID changes the results correctly. 

A completing explaination is that the date/time or scheduled status comparison is incorrect. Another plausible reason could be that the regression test does not match AC-04.2, so therefore by holding the time and status as a constant whilst changing only the practitioner ID, it can compare the expected results with AC-04.2 to distinguish a product defect from a test defect.

Member and saved sequence/time or commit showing this preceded consultation: [complete]
Andy Hoang recorded this hypothesis as the human-first F8-01 diagnosis. The saved commit should demonstrate the order of work, 9059737469c089044d3843bbcf23fe3de67e31a7.


### F8-02 human entry
Likely cause and why plausible: [complete]
The likely cause is that the 'find_appointment' filters out appointments with cancelled status. But the original A1 object still remains visible through the 'list_appointments' after cancellation. However, lookup using the same appointment ID returned 'None', this is a key differnce that suggests that the problem is within the lookup filtering rather than the deletion/

Evidence intended to inspect / competing explanation / discriminating check: [complete]
By comparing the appointment objects identity before and after cancellation, it allows us to inspect every condition inside 'find_appointment()' for a status-based restriction. We can then compare the results of 'list_appointments' and 'find_appointments("A1"), this evidence will be determental to show whether the appointment remains stored but is hidden during lookup. 

A competing explaination would be that cancellation deletes or replaces the appointment object. Another plausible outcome would be that the retained-history test contains an incorrect explaination. Therefore we can compare the object identity and stored collection contents before and after cancellation, we can also check FR-07 and AC-05.2 to confirm the required behaviour.

Member and saved sequence/time or commit showing this preceded consultation: [complete]
Andy Hoang recorded this hypothesis as the human-first F8-02 diagnosis. A commit SHA should provide evidence of this sequence, bac6afe36e5dfeb881a9561f968142c16906d154.

## F. GitHub Copilot prompts, findings and human decisions

Use the full handout prompt separately for BOTH defects, after E. Keep each actual prompt or accessible reference; include observed behaviour, expected behaviour, reproduction, failing test, human hypothesis, relevant code, three ranked causes and discriminating checks, with the no-rewrite/no-invented-requirements constraints.

### F8-01 Copilot review
Actual prompt / output reference and member: [complete]
Andy Hoang submitted the F8-01 diagnostic prompt containing the observed behaviour, AC-04.2 expectation, reproduction steps, failing regression test, human hypothesis and relevant conflict code. Copilot was then instructed to rank the three possible causes and identify distinguishing evidence without rewriting the application or inventing requirements. The output can be seen in the 'AI review ouput' folder seen within stage08. 

The prompt used was:
"Observed behaviour:
The system allows the same practitioner to be booked twice at the exact same time. It incorrectly rejects a different practitioner at that time.

Expected behaviour:
Under FR-05, AC-04.1 and AC-04.2, the same practitioner must not have two SCHEDULED appointments at the exact same date and time. Different practitioners may be booked at the same time.

Steps to reproduce:
1. Register patients P1 and P2.
2. Register practitioners D1 and D2.
3. Book A1 for P1 and D1 at 09:00.
4. Attempt A2 for P2 and D1 at 09:00.
5. Attempt A3 for P2 and D2 at 09:00.

Failing test:
project/test_regressions.py::test_f8_01_practitioner_conflict_rule
Failure: DID NOT RAISE ValueError for the conflicting D1 appointment.

My hypothesis:
The practitioner-ID comparison inside has_practitioner_conflict() may be reversed.

Relevant code:
if (
    appointment.appointment_id != exclude_appointment_id
    and appointment.practitioner.practitioner_id != practitioner_id
    and appointment.date_time == date_time
    and appointment.status.value == "scheduled"
):
    return True

Task:
Rank the three most likely causes. For each, identify the evidence I should inspect to distinguish it from the other possible causes.
Do not rewrite the entire application.
Do not invent requirements.
Treat all suggested explanations as hypotheses."

1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
Copilot ranked the reserved practitioner comparison as the most likely cause. As the source inspection confirmed that 'has_practitioner_conflict()' used 'appointment.practitioner.practitioner_id != practitioner_id' and was causing D1 to be compared with D1 to return false, and D1 compared with D2 to return true, this suggestion was deemed to be correct as it matched both the oberserved behaviour and the failing regression test. Therefore it is accepted and the != was changed to ==.


2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
Another one of copilots suggestion was that the 'book_appointment()' might pass the wrong practitioner ID into 'has_practitioner_conflict()'. Further inspection lead to the understanding that the service passed 'practitioner.practitioner_id', which belonged to the practitioner resolved for the new booking request so therefore the caller supplied the expected value and was not able to explain the failure. So finally it was deemed that this suggestion is false and therefore needed to be rejected.

3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
Copilot suggested that whitespace, different value types or duplicated practitioner records could've potentially cause the IDs to be compared incorrectly. The synthetic test used ordinary strings D1 and D1 and the already existing registration and validation tests passed. The failure also modified exactly according to the visible != operator, so without any evidence of a type or whitespace mismatch it can be deemed that this suggestion is also incorrect and is to be rejected. 

Final human conclusion and comparison with initial hypothesis: [complete]
The supported root cause was the reserved practitioner comparison within the 'has_practitioner_conflict()' this was agreed with the original human hypothesis, but copilots output remained a hypothesis until the code, caller and tests were properly inspected. Changing the != to == was the smallest supported repair and the focused regression test then passed in 0.01s, and the repair was recorded in commit 9059737469c089044d3843bbcf23fe3de67e31a7.


### F8-02 Copilot review
Actual prompt / output reference and member: [complete]
Andy Hoang submitted the F8-02 diagnostic prompt containing the observed behaviour, retained-history requirements, reproduction steps, failing test, human hypothesis and relevant lookup code. Copilot was asked to rank three possible causes and identify evidence that would distinguish them. It ranked status-based exclusion, different appointment sources and cancellation changing the appointment’s identity or ID. Output reference can be seen within the 'AI review output' folder

1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
Copilot was instructed to rank the cancelled-status filter as the most likely cause, and further inspection confirmed that A1 remained within the 'list_appointment' with a 'CANCELLED' status, however the 'find_appointment()' required the 'appointment.status.value != "cancelled"' so therefore the ID would match whilst the status condition prevented the object from being returned. Therefore this suggestion can be considered correct and is to be accepted.

2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
The second suggestion that Copilot outputted was that the listing and lookup might have used different collections or filtered views. Further insepections showcased that the 'find_appointment()' directly looks over 'self.list_appointments()' whilst 'list_appointments()' returned the values from the same '_appointments' collection. Therefore A1 was present within that list and was reached by the lookup loop. So this proves that the suggestion is wrong so it was rejected because no seperate or filtered collection existed.

3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
The final suggestion that copilot made was that the cancellation might have altered the ID, and it introduces whitespace or replace the appointment object. The regression test confirmed that cancellation returned the same object and that the object remained in the stored appointment list. As its ID remained A1, whilst only its status was chnaged to 'AppointmentStatus.CANCELLED'. This suggestion was then deemed as wrong as was rejected.

Final human conclusion and comparison with initial hypothesis: [complete]
The suppported root cause was the cancellation-status condition within the 'find_appointment()', this was supported by the inital huaman hypothesis, but the suggestion was verified by inspecting list members, object identity, statues and lookup behaviour. The smallest repair was done to remove only the cancelled-status filter while preserving validation and ID matching. The focused test passed in 0.01s, the full suite passed all 55 tests, and the repair was committed and pushed as bac6afe36e5dfeb881a9561f968142c16906d154. 


## G. Failing to passing regression evidence

| Checkpoint | Code SHA or precise diff | Command and working directory | Actual result and artefact reference |
|---|---|---|---|
| F8-01 before repair | [complete] | [complete] | [complete] |
Code SHA:
bc965111f508ed490c749bb583aaaf6588f1b321

Command and working directory:
from project/: python3 -m pytest tests '/Users/andyhoang/st1-assignment-3/project/test_regressions.py' -v

Active results and artefact reference:
1 failed in 0.01s; expected ValueError was not raised. See project/test_regressions.py.

| F8-01 after repair | [complete] | [complete] | [complete] |
Code SHA: 
9059737469c089044d3843bbcf23fe3de67e31a7

Command and working directory:
from project/: python3 -m pytest '/Users/andyhoang/st1-assignment-3/project/test_regressions.py'::test_f8_01_practitioner_conflict_rule -v

Active results and artefact reference:
1 passed in 0.01s and != was changed to ==.

| F8-02 before repair | [complete] | [complete] | [complete] |
Code SHA:
9059737469c089044d3843bbcf23fe3de67e31a7

Command working directory:
python3 -m pytest tests '/Users/andyhoang/st1-assignment-3/project/test_regressions.py' -v

Active results and artefact reference:
F8-02 failed because lookup returned None and combined result was 2 failed in 0.01s.

| F8-02 after repair | [complete] | [complete] | [complete] |
Code SHA: 
bac6afe36e5dfeb881a9561f968142c16906d154

Command working directory:
python3 -m pytest '/Users/andyhoang/st1-assignment-3/project/test_regressions.py'::test_f8_02_cancelled_appointment_remains_retrievable -v

Active result and artefact6 reference:
1 passed in 0.01s and local and remote SHAs matched after the push.

| Full suite after both repairs, before refactor | [complete] | [complete] | [complete] |
Code SHA:
bac6afe36e5dfeb881a9561f968142c16906d154

Command and working directory:
From project/: python3 -m pytest tests '/Users/andyhoang/st1-assignment-3/project/test_regressions.py' -v


Explain how the assertions detect each relevant incorrect result and protect previous behaviour: [complete]
Unrelated failures investigated / resolution: [complete or not applicable with reason]
The F8-01 test required a 'ValueError' when the same practitioner is booked at the exact same time. It also confirms that the rejected booking does not change stored appointments and that a different practitioner remains permitted. The F8-02 test, checks whether that cancellation retains the same object with 'CANCELLED' status and that list and lookup operations still return it. It also verifies that repeated cancellation remains rejected.


Unrelated failures investigated:
No unrelated failures remained after both repairs and temporary 'AttributeError' and 'IndentationError' and missing colon 'SyntaxError' that occured were all caused by editing problems that were corrected before verification. 'ModuleNotFoundError' occured when the full suite was run from the repository root and was then resolved by running it from project/. An intermediate 4 failed, 51 passed result occurred when F8-01 was accidentally changed back to !=; restoring == produced the final 55 passed result.


## H. Refactoring decision and before/after verification
 
Smell and exact location: [complete]
'SmartCareDataStore.has_practitioner_conflict' in 'project/smartcare/data_store.py' used the magic string "scheduled". This method accessed 'appointment.status.value' and compared its internal value directly with that string, this would therefore cause unnecessary dependance on how th enum value was represented internally. This also made the intended appointment status to be less explicit to the reader. The main issue was a code smell rather than a product defect as the tests already passed beforehand.


Small proposed structural change / why justified: [complete before editing]
The proposed change was to modify the 'appointment.status.value == "scheduled" with appointment.status is AppointmentStatus.SCHEDULED. As the already existing enum was already imported into the 'data_store.py' so therefore no new dependency was needed. By using the enum member it communicates the intended status more explicitly. It also helped to reduce the risk of any spelling mistakes or inconsistent magic strings. This was a very small structural change that did not appear to alter the conflict rule.


External behaviour to preserve / relevant tests: [complete]
The same practitioner must still be rejected if another scheduled appointment exists at the same exact date and time. A different practitioner must then remain permitted at that time and a cancelled appointment must continue to release the practitioner's slot. Appointment identity, stored state and exception behaviour also needs to remain unmodified. The regression tests, focused service test and complete suite were all used to protect these very behaviours. 


Before result: see G, full passing suite.
The before-refactor code SHA was bac6afe36e5dfeb881a9561f968142c16906d154. The complete suite was run from /Users/andyhoang/st1-assignment-3/project. The command used was python3 -m pytest '/Users/andyhoang/st1-assignment-3/project/test_regressions.py'. Pytest collected 55 tests from the existing and regression-test files. The result was 55 passed in 0.04s.


Actual change / diff / separate refactor SHA: [complete]
The refactor removed the 'appointment.status.value == "scheduled"' from the conflict condiiton, this expression was then changed to 'appointment.status is AppointmentStatus.SCHEDULED'. The Git commit showcased onw insertion and one deletion within the datastore.py file and no other production-code lines were included in the refactor commit. 
Code SHA: 27d4856e925992960bdb5fc3fc387f3b6cab8d55


Focused and full after-refactor commands / working directory / results / evidence: [complete]
The syntax check python3 -m py_compile smartcare/data_store.py completed without an error. Running python3 -m pytest test_regressions.py -v produced 2 passed in 0.00s. The four focused practitioner-conflict and cancelled-slot tests produced 4 passed in 0.01s. The complete suite was then run from the project/ directory using the existing tests and the regression-test file. The final after-refactor result was 55 passed in 0.03s.


Result — accepted, revised or rejected / reason / behaviour-preservation conclusion: [complete]
The refactor was then accepted as it greatly improved readability whilst still keeping the intended conflict rule unchanged. The enum comaprison more clearly identified that only the scheduled appointments would create conflicts. Whilst the focused tests confirmed that the same-practitioner conflicts would be rejected and different practitioner bookings remained permitted. It also confirmed that cancelled appointments would continue to release their time slots, and finally all 55 tests passed after the change, providing evidence that external behaviour was preserved.


## I. Git, human review and integration

Issues for both defects / refactor scope and owners: [complete]
Focused Github issues are still needed to be created or linked for F8-01, F8-02 and the refactoring decision. The F8-01 covers restoring the same practitioner conflict rule whilst F8-02 covered the retained cancelled appointment lookup. The main refactor issue covered replacing the magic 'scheduled' string with the 'AppointmentStatus.SCHEDULED'. Andy Hoang completed these repairs and refactor work.


Branch / prepared, repair and refactor checkpoints: [link B/C/D/H]
The work was completed on debug/stage08. The prepared faulty-state SHA was b05c90b760b350ddc01b288c81b8bd1a2e3f89c7, and the regression-test SHA was bc965111f508ed490c749bb583aaaf6588f1b321. The F8-01 repair SHA was 9059737469c089044d3843bbcf23fe3de67e31a7, while the F8-02 repair SHA was bac6afe36e5dfeb881a9561f968142c16906d154. The refactor SHA was 27d4856e925992960bdb5fc3fc387f3b6cab8d55, and it was pushed successfully.



PR link and another member's reviewer identity: [complete]



Key human feedback, difference from Copilot findings and response/outcome: [complete]
Actual review approval / merge evidence: [complete]
Integrated code SHA and team pull/retest command / working directory / result: [complete]
Evidence-only later SHA / explanation if different: [complete or not applicable]
Each member's substantive contribution and artefact: [complete]

## J. Required reflections

1. Which Copilot diagnosis appeared convincing but lacked evidence? [complete; report honestly if none and discuss the least-supported real suggestion]
Copilots suggestion that 'book_appointment()' might possibly pass the wrong practitioner ID to 'has_practitioner_conflict' would initially appear plausible. As passing the wrong argument could potentially produce behaviours similar to that of a reversed comparison, however source inspection would show that the service passed the practitioner ID belonging to the requested booking and no execution or code evidence supported an incorrect caller argument. The suggestion was therefore rejected after the visible != comparison provided a better-supported explanation.


2. What evidence changed your group's view? [complete]
The failing tests first established only that the conflict and cancelled history behaviours were incorrect, but by inspecting 'has_practitioner_conflict()' it would reveal that practitioner IDs were being compared using != which would directly explain the reversed conflict results. And further inspection to the 'find_appoint()' would reveal that an explicit condition excluding appointments with a cancelled status. The list and identity checks confirmed that the cancelled appointment remained stored rather than being deleted or replaced. This evidence would change both diagnoses from plausible hypothesis into supported root causes.


3. How did regression tests protect the refactoring? [complete]
Before refactoring, the complete suite passed all 55 test, which would establish a working baseline. The refactoring replaced the 'scheduled' magic string with 'AppointmentStatus.SCHEDULED' without changing the conflict logic, now after the change, both Stage 8 regression tests passed, and the four focused conflict tests passed in 0.01s. The complete suite then passed all 55 tests in 0.03s. These results showed that the readability improvement preserved the required external behaviour.


## K. Ten formative questions

1. What should an engineer do before changing code in response to a failure?

Response: [complete]
First, reproduce the failure consistently and then record the expected and observed behaviour. Once this is done, confirm the expected behaviour against the requirements, then form a testanle hypotheses and inspect relevant evidence before ever changing any lines of code.

2. Where should expected behaviour come from during debugging?

Response: [complete]
Expected behaviour should come from approved requirements, acceptance criteria and documented system contracts. Already existing tests can help provide supporting evidence when they agree with those requirements. A failing test should not automatically be assumed correct.

3. What is a debugging hypothesis?

Response: [complete]
A debugging hypothesis is a testable explaination for why a failure occured within the program. This should identify the suspected cause and the evidence that may exist if it is correct. This hypothesis is accepted or rejected after inspecting that specific evidence.

4. What is a regression test and why is it retained?

Response: [complete]
A regression test reproduces required behaviour associated with a discovered defect. It should fail whilst the defect exists and should pass after the repair. This is retained to detect if a later change reintroduces the same problem.

5. What is meant by root cause?

Response: [complete]
The root cause refers to the underlying code condition or decision that produced a specific failure. It isnt necessarily the line where the test or exception first appeared. Evidence from requirements, execution results and source code should support the identified cause.

6. What is refactoring?

Response: [complete]
Refactoring changes the internal structure of working code without ever changing its required external behaviour. Its main purpose is to help improve readability, maintainability and or design. Test should then be passed before and after the refactoring.

7. What is a swallowed exception?

Response: [complete]
A swallowed exception occurs when an exception is caught but ignored or hidden without the appropriate handling. This could possibly make the program appear successful despite the operationm failing. This also makes debugging signifcantly harder as useful failure information is lost.

8. What is a code smell?

Response: [complete]
A code smell is a warning that code could be difficult to understand, maintain or change in a safe manner. Examples of this would include duplicated code, magic values, deep nesting and mixed responsibilities. Code smell is not automatically detected as a defect but it may justify careful refactoring.

9. How should GitHub Copilot-generated debugging diagnoses be treated?

Response: [complete]
Copilot diagnoses should be treated as a unverified hypotheses rather than cold facts. As each suggestion must be compared with the requirements, source code and test evidence. It should only be accepted once the availble evidence supports it. 
10. What is the Stage 8 engineering rule?

Response: [complete]
The Stage 8 rule is to diagnose before fixing. Engineers should observe, reproduce, hypothesise and inspect evidence before editing the code. They should then apply the smallest repair supported by that evidence.

## L. Completion and handover

- [x] Existing project, earlier tests and stage records preserved.
- [x] Passing Stage 7 SHA and safe preparation details recorded.
- [x] Both defects reproduced with meaningful failing tests.
- [ ] Both human hypotheses recorded before Copilot; actual suggestions evaluated with evidence.
- [x] Supported causes and minimal repairs explained; focused and full regression results recorded.
- [x] One genuine refactor verified under passing before/after tests.
- [ ] Human PR review, feedback resolution and integrated retest recorded.
- [x] Tutorial, three reflections and ten formative responses complete.
- [ ] Local recovery metadata excluded from submitted source.
- [ ] Same project and full suite ready for Stage 9 after Stage 8 integration, verification and recording.

Verified integrated code SHA / result: see I.
Submitted SHA and evidence-only difference if any: [complete]
Unresolved issues or incomplete checks / owner / next action: [complete]
Both prepared defects have been repaired, and the enum refactor has been completed and pushed on debug/stage08. The latest branch test result is 55 passed in 0.03s.

Handover note: [complete]
