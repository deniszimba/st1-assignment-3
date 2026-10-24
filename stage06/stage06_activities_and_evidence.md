# Stage 6 activities and evidence

Complete this one group record. Link actual issues, diffs, tests and reviews; avoid copying entire histories. Blank fields are intentional. Duplicate rows as needed. Use synthetic data only. Every member records their own meaningful contribution. Do not invent results, reviews or Copilot use.

- Group/tutorial: Wed 4:30 - 6:30 Group 3
- Members, GitHub usernames and cohorts: Andy Hoang, Denis Zimba, Tari Ganas, Ahron Singh typicalgeezer42
- Repository URL: (https://github.com/deniszimba/st1-assignment-3)
- Starting SHA: 90d0d7f5c52379ab957e37cdd988c6a36017b675 (“Add shared SmartCare Assignment 3 starter”, Denis Zimba, 14 Oct 2026)

## A Requirement to issue activities

### FR-02 Patient Search

- Title:
  Patient search by ID (FR-02)
  
- Context: PatientService.find_patient 
- Requirement: Find a patient by patient ID

- Acceptance criteria:

With P1 registered, find_patient('P1') returns the same stored Patient object (checked with is), not a copy
find_patient('P1    ') returns that same patient
find_patient('p1') raises LookupError since its case sensitive
An unregistered valid ID such as P2 raises LookupError
A blank or non-text ID raises ValueError
Lookup never adds, replaces or changes a patient record

- Scope:
  'find_patient' works and the tests pass no changes to any other .py files
  
- Definition of Done: the find_patient works and every acceptance criteria is met. 
- Owner: Ahron 
- Actual issue link: https://github.com/deniszimba/st1-assignment-3/issues/1

### Supporting FR-03 Practitioner Search

- Title:
  Practitioner lookup by ID
  
- Context: PractitionerService.find_practitioner raises NotImplementedError. It is a supporting lookup over practitioners registered under FR-03
- Requirement: Find a Practitioner by Practitioner ID

- Acceptance criteria:

Returns the same stored object, not a copy
Trimmed IDs work
Wrong case raises LookupError
Unknown ID raises LookupError
Blank or non-text ID raises ValueError
Lookup never adds or changes a record

- Scope:
PractitionerService.find_practitioner in services.py and tests in test_services.py only
  
- Definition of Done: the PractitionerService.find_practitioner works and every acceptance criteria is met.
- Owner: Ahron
- Actual issue link: https://github.com/deniszimba/st1-assignment-3/issues/2
  
### FR-06 Appointment Cancellation with FR-07 retained history

- Title: Cancel a scheduled appointment and keep it in history (FR-06, FR-07)
- Context: AppointmentService.cancel_appointment raises NotImplementedError. Appointment.cancel() already only allows SCHEDULED to CANCELLED and raises ValueError otherwise.
- Requirement: FR-06 Cancel only a SCHEDULED appointment. FR-07 Keep the same appointment, CANCELLED, in session history.
- Acceptance criteria:

Cancelling SCHEDULED A1 returns the same Appointment object with status CANCELLED
After cancelling, find_appointment('A1') returns that same object, the store still lists it, and the other details dont change
A second cancellation raises ValueError and the status stays CANCELLED
Cancelling a COMPLETED appointment raises ValueError and it stays COMPLETED
An unknown valid ID raises LookupError; a blank or non-text ID raises ValueError
Cancelling one appointment does not change any other appointment
Uses Appointment.cancel(); no direct status assignment, deletion or replacement object
- Scope: cancel_appointment in services.py and tests in test_services.py only
- Definition of Done: Every acceptance criterion has a passing test in tests/test_services.py and everything works and is completed.
- Owner: Ahron
- Actual issue link: https://github.com/deniszimba/st1-assignment-3/issues/3

## B Commit quality

| Original example | Strong or Weak | Reason |
|---|---|---|
| changes | weak | It does not say what changed or why. A reviewer cannot link it to a requirement without opening the whole diff. |
| final version | Weak | 	It describes timing, not behaviour |
| Add patient search by ID | Strong | Short, imperative and names one behaviour that maps to FR-02 |
| fix stuff | Strong | Everything was fixed |
| Prevent cancellation of completed appointments | Strong | 	It names the exact rule (FR-06, only SCHEDULED can be cancelled) and the behaviour change |

## C Over scoped PR review

A cancellation PR also renames unrelated patient fields, restructures unrelated code and adds a new dependency.

- Scope concerns: The PR should deliver one thing, FR-06/FR-07 cancellation. The field renames, restructuring and new dependency are three extra changes with no linked issue or acceptance criteria.
- Responsibility and architecture concerns: By renaming the patient fields changes the domains public interface. So renaming runs the risk of breaking the lookup and booking.
- Testing and review concerns: A green run only proves the checks that exist. The supplied eight tests do not call the service cancellation at all, and they may not cover renamed fields.
- Changes to remove or separate, with reasons: Keep only cancel_appointment and its tests. Remove the field renames because no requirement asks for them if the team wants them, raise a separate issue and discuss it first.

## D Challenge a weak Copilot review

GitHub Copilot says: "Looks good; tests pass."

- Missing evidence: No test commands are provided, no SHA, and copilot cant actually see our test run, so its essentially another unverified ai claim. it names no requirement or acceptance, with no details 
- Follow-up review question 1: Which test run is "tests pass" based on? Give the command the directory, the commit SHA and the observed output or say clearly that no run was observed.

- Follow-up review question 2: Which claim shows that cancel_appointment returns the same stored object and that its status is CANCELLED?

- Follow-up review question 3: Where is FR-07 checked? That the cancelled appointment is still returned by find_appointments and still in list_appointments?
- Follow-up review question 4: What happens on a second cancellation or on a COMPLETED appointment? 
- Follow-up review question 5: Does the diff use Appointment.cancel() or does it set the status directly, delete the record or build a replacement? 
- Additional questions if useful: How does the code tell an unknown ID how does it tell an unknown ID like LookupError apart from ValueError and is there a test for each?

## E Team workflow agreement 

Agreed by: Andy Hoang, Denis Zimba, Tari Ganas, Ahron Singh 23/10/2026

| Practice | Team agreement |
|---|---|
| Branch naming | feature/<short-task> for new behaviour and fix/<short-task> for defects, one branch per issue, for example feature/patient-lookup Never commit routine work directly to main. |
| Commit message convention |Use short, clear messages that describe the action, such as Add patient search by ID`. Avoid vague messages such as changes or fix stuff|
| PR size | Keep each PR focused on one issue at a time |
| Another-member review requirement | Another member must review the changes in the file before the commits are merged |
| Merge rule | Merge only after the tests pass, feedback is answered and another member approves. |
| Significant Copilot disclosure rule | Make sure to review any important Copilot help and make sure to use it ethically and explain how the output was checked |

## F Issue and backlog index

Create at least two focused issues. Add a linked practitioner-lookup issue or an explicit supporting criterion with the tutor if needed to cover all three service targets.

| Issue link | Requirement | Owner | Acceptance criteria or precise link | Status |
|---|---|---|---|---|
|[#1](https://github.com/deniszimba/st1-assignment-3/issues/1) | FR-02 Patient search (AC-02.1, AC-02.2) | Ahron Singh | Section A, FR-02 criteria 1 to 6 | Closed by [PR #4](https://github.com/deniszimba/st1-assignment-3/pull/4) |

|[#2](https://github.com/deniszimba/st1-assignment-3/issues/2) | Supporting practitioner lookup over FR-03 registrations | Ahron Singh | Section A, supporting practitioner lookup criteria | Closed by [PR #5](https://github.com/deniszimba/st1-assignment-3/pull/5) | 

|[#3](https://github.com/deniszimba/st1-assignment-3/issues/3) | FR-06 cancellation with FR-07 retained history (AC-05.1 to AC-05.3) | Ahron Singh | Section A, FR-06/FR-07 criteria 1 to 7 | Closed by [PR #6](https://github.com/deniszimba/st1-assignment-3/pull/6) |

## G Pull request evidence

  PR #4: Patient search by ID

- PR link and title: [#4](https://github.com/deniszimba/st1-assignment-3/pull/4) patient search by ID
- Linked issue and requirement: [#1](https://github.com/deniszimba/st1-assignment-3/issues/1) FR-02 AC-02.1 AC-02.2
- Feature branch: 'feature/patient-lookup'
- Changed behaviour: patient lookup was added and seven patient search test cases. 
- Meaningful commits:
  - https://github.com/deniszimba/st1-assignment-3/commit/d72d6c6377d43d65959bb4d0ef16778baaea6577
  - https://github.com/deniszimba/st1-assignment-3/commit/30367d277b75ac26d5f30f8948d2fe9b64b5ce84 
- Test command, directory and observed result: -m pytest from project/ — 15 passed on 30367d2
- Another-member reviewer: Ahron Singh, Tari Ganas
- Human observations recorded before Copilot: Tari's review comment: (https://github.com/deniszimba/st1-assignment-3/pull/4#issuecomment-6306698027), posted 21 Oct 2026. The Copilot output was posted later on the same day (https://github.com/deniszimba/st1-assignment-3/pull/4#issuecomment-6307187070)  
- Requirement, responsibilities, test assertions and unrelated-scope checks: I confirm that only services.py changed and test_services.py was added by Tari he checked that the acceptance criteria was right judged that the code follows the requirement and ran the tests: 15 passed
- Key feedback: No changes were necessary copilot was useful however it should not be trusted blindly  
- Author response/change and verification: No code change was needed
- Reviewer recheck and approval: (https://github.com/deniszimba/st1-assignment-3/pull/4#pullrequestreview-5594757864) 21 Oct 2026
- Merge outcome and SHA: merged into main by Tari Ganas, 21 Oct 2026, merge commit [433a34524be0a4d30dae84246b43828b08ba2c5d](https://github.com/deniszimba/st1-assignment-3/commit/433a34524be0a4d30dae84246b43828b08ba2c5d) 
- Significant Copilot assistance: Tari used Copilot Chat for the required review comparison 
- Linked issue closure: in the PR description issue #1 closed when PR #4 merged
- Each member updated main: Every member updated to main, Tari Ganas, Ahron Singh 
- Integrated verification after merge: - Integrated verification after merge: `python -m pytest` in `project/` on merge commit 433a34524be0a4d30dae84246b43828b08ba2c5d: 15 passed (run by Ahron Singh, 23 Oct 2026, by checking out the merge commit; the run straight after the merge was not recorded)

PR #5: Practitioner lookup by ID

- PR link and title: [#5](https://github.com/deniszimba/st1-assignment-3/pull/5) Practitioner lookup by ID
- Linked issue and requirement: [#2](https://github.com/deniszimba/st1-assignment-3/issues/2), supporting operation over FR-03 registrations
- Feature branch: feature/practitioner-lookup
- Changed behaviour: Added practitioner lookup and seven practitioner search test cases
- Meaningful commits:
   https://github.com/deniszimba/st1-assignment-3/commit/6471d23390b54ee77c240f175a338d4c12737472
- Test command, directory and observed result: python -m pytest` from project/ — 22 passed on 6471d23.
- Another-member reviewer: Tari Ganas, Ahron Singh
- Human observations recorded before Copilot: This is Tari's Human review before Copilot (https://github.com/deniszimba/st1-assignment-3/pull/5#issuecomment-6309391741) which followed onto copilots output (https://github.com/deniszimba/st1-assignment-3/pull/5#issuecomment-6309576994) and finally Taris decision
(https://github.com/deniszimba/st1-assignment-3/pull/5#issuecomment-6309712942)
- Requirement, responsibilities, test assertions and unrelated-scope checks: The change adds the supporting practitioner lookup. PractitionerService.find_practitioner uses the data store’s existing validation and raises LookupError for an unknown practitioner. The tests check the same stored object, spaces around IDs, case sensitivity, unknown IDs, invalid IDs and unchanged records. Only services.py and test_services.py were changed.
- Key feedback: Whilst copilot is useful it shouldn't always be trusted and should always be looked over 
- Author response/change and verification: No code was changed 
- Reviewer recheck and approval: (https://github.com/deniszimba/st1-assignment-3/pull/5#issuecomment-6309721002) 21 Oct 2026
- Merge outcome and SHA: Merged into main: merge SHA f36218eb37b264b2f6b435a7933589ab07176390 (https://github.com/deniszimba/st1-assignment-3/commit/f36218eb37b264b2f6b435a7933589ab07176390) 
- Significant Copilot assistance: Tari used Copilot Chat for the required review comparison
- Linked issue closure: in the PR description issue #2 closed when PR #5 merged
- Each member updated main: Every member updated to main, Tari Ganas, Ahron Singh
- Integrated verification after merge: `python -m pytest` in `project/` on merge commit f36218eb37b264b2f6b435a7933589ab07176390: 22 passed (run by Ahron Singh, 23 Oct 2026, by checking out the merge commit; the run straight after the merge was not recorded)

  PR #6: Cancel a scheduled appointment and keep it in history

- PR link and title: [6](https://github.com/deniszimba/st1-assignment-3/pull/6) Cancel appointments and keep their history
- Linked issue and requirement: [#3](https://github.com/deniszimba/st1-assignment-3/issues/3) FR-06 and FR-07 AC-05.1 to AC-05.3
- Feature branch: feature/cancel-appointment
- Changed behaviour: Added appointment cancellation and eleven cancellation test cases
- Meaningful commits:
  https://github.com/deniszimba/st1-assignment-3/commit/4de75529e0ab807b1e1c1d8fa7985aa66c5f12ed
- Test command, directory and observed result: python -m pytest from project/ — 33 passed on 4de7552
- Another-member reviewer: Tari Ganas, Ahron Singh
- Human observations recorded before Copilot: Tari's Human review before Copilot: (https://github.com/deniszimba/st1-assignment-3/pull/6#issuecomment-6315364299)
  here is Copilots output: (https://github.com/deniszimba/st1-assignment-3/pull/6#issuecomment-6315409481)
  and here is Taris final  decisions: (https://github.com/deniszimba/st1-assignment-3/pull/6#issuecomment-6315745686) These were all committed on the 21 Oct 2026. 
- Requirement, responsibilities, test assertions and unrelated-scope checks: The change meets FR-06 and FR-07. AppointmentService.cancel_appointment finds the stored appointment, calls Appointment.cancel() and returns the same object. The tests are checked.
- Key feedback: Whilst copilot is useful it shouldn't always be trusted and should always be looked over 
- Author response/change and verification: No code was changed
- Reviewer recheck and approval: (https://github.com/deniszimba/st1-assignment-3/pull/6#pullrequestreview-5599565998) 21 Oct 2026
- Merge outcome and SHA: Merged into main: merge SHA 3ca7a3a4651d6751c8cb74133b316489cbe7407f (https://github.com/deniszimba/st1-assignment-3/commit/3ca7a3a4651d6751c8cb74133b316489cbe7407f) 
- Significant Copilot assistance: Tari used Copilot Chat for the required review comparison
- Linked issue closure: in the PR description issue #3 closed when PR #6 merged
- Each member updated main: Every member updated to main, Tari Ganas, Ahron Singh
- Integrated verification after merge: `python -m pytest` in `project/` on merge commit 3ca7a3a4651d6751c8cb74133b316489cbe7407f: 33 passed (run by Ahron Singh, 23 Oct 2026, by checking out the merge commit; the run straight after the merge was not recorded)


## H Copilot collaboration record

Record meaningful required use, not every trivial completion. Repeat per significant interaction.

- Member and task: Tari Ganas used Copilot as a second review for PR #4, which covered FR-02 patient search
- Prompt/purpose and relevant issue/diff: Copilot was asked to compare the PR #4 changes with the acceptance criteria in issue #1. The Copilot response was posted after Tari’s human review. It was also done like this with PR #5 and PR #6
- Summary of output: Copilot didn't find anything too wrong with it noted that ID trimming, case sensitivity and invalid-ID checks happen in the data store, which was outside the PR diff
- Human check against actual code, requirements and tests: Tari checked data_store.py, domain.py and test_services.py. I went through the entire thing and 15 tests passed
- Decision — Accept / Modify / Reject:
  Accept: check the data store validation
  Reject: tests only check the data store because they call the patient service
  Reject: cancellation comment because cancellation was outside PR #4
- Reason: The validation behaviour was confirmed in the existing code, so no code change was needed and the service tests check the required patient-search behaviour. Cancellation was handled separately in issue #3 and PR #6.
- Verification/evidence: Tari recorded the human decisions. Running python -m pytest from project/ on commit 30367d2 produced 15 passed. [comment](https://github.com/deniszimba/st1-assignment-3/pull/4#issuecomment-6307395508)

## I Human versus Copilot review comparison

- Human reviewer noticed before consulting Copilot: Tari checked that the PR changed only services.py and test_services.py he checked the patient search requirements against the tests and ran the full test 
- Copilot noticed: Copilot noticed that ID trimming and validation happen in the data store, which was outside the PR diff Copilot also recommended checking the code weather it was fully tested  
- Overlap: Both the reviews found nothing really wrong and agreed that the change was focused on patient lookup and its tests.
- What did the human reviewer notice that Copilot did not: Tari ran the tests and observed that 15 passed Copilot could review the supplied code but could not confirm that the tests had actually been run.
- What did Copilot identify that the human reviewer initially missed: Copilot pointed out that the service depends on validation in the data store.
  
- Unsupported or incorrect Copilot suggestion: [response or none identified with explanation]
- Human judgement accepted, modified or rejected, and why:
  Tari accepted the suggestion to check the data-store validation and confirmed that it worked correctly
  Tari rejected the claim about the tests because they call the service
  Tari rejected the cancellation comment because it was outside the PR’s scope
  - Which evidence justified merge approval:
  -  The change matched issue #1 the validation behaviour was confirmed and all 15 tests passed on commit 30367d2. Tari then submitted formal approval. 

## J Contributions

Repeat per member. Include only categories that describe actual work; write not applicable where appropriate. Pairing or mentoring can be supported by a short corroborated note.

- Member: Ahron Singh
- Implementation: PatientService.find_patient, PractitionerService.find_practitioner and AppointmentService.cancel_appointment in project/smartcare/services.py
- Testing: created project/tests/test_services.py
- Review: N/A
- Issue refinement: Drafted the stage 6 issues and their acceptance criteria
- Design and responsibility discussion: for example agreeing that cancellation must go through Appointment.cancel() rather than the service setting status with Tari, evidence is our conversation history
- Debugging or integration: added the missing test file to PR #4 as a second commit (30367d2); pulled main and ran the tests after merges
- Documentation or team support: Discord conversations and call logs with Tari.

- Member: Tari Ganas
- Implementation: N/A
- Testing: ran the full suite on the PR #4 branch: 15 passed
- Review: reviewed PR #4, ran the required Copilot comparison, recorded Accept/Reject decisions  and approved; reviewed PR #5, ran the Copilot comparison and recorded decisions; reviewed PR #6, ran the Copilot comparison, recorded decisions and approved (approval)
- Issue refinement: Tari reviewed copilots recommendations
- Design and responsibility discussion: See PR and issue history.
- Debugging or integration: merged PR #4 into main (433a345); merged PR #5 into main (f36218e); merged PR #6 into main (3ca7a3a); [TO DO: pulled main and ran the tests after the merge]
- Documentation or team support: drafted section A for FR-02 (acceptance criteria and scope wording) 


## K Exit question

A high commit count mostly just reflects habits. One person can turn a tiny change into many commits and another person could do it all in one commit for the same work, so the number provides nothing about quality or wether a requirement was met. In stage 6 All commits came from Ahron and Tari reviewed every PR, ran tests and compared copilots review with his own. Actual evidence of proving the commit works proides much more than just commit counts as a referral for quality. Better evidence is the linked issues, review comments, test results and each member's ability to explain the code.

[response]

## L Stage 6 formative questions

1. what is version control
A system that records the changes to a project as commits, allowing the team to see what was changed, when it was changed and who it was changed by. it also allows you to compare versions and return to and earlier state.

2. Why is a feature branch useful?
It keeps one fucused change serpeate from main until it has been tested and reviewed for completion. It allows memebers to work in parallel and the branches diff against main is what the reviwer checks.

3. What makes a commit a good engineering commit?
It contains one coherent change, such as one behaviour and its tests, with no unrelated files or secrets. For tests, its clear and the message shows what changed.

4. What is a pull request?
A request to merge a branch into main, it shows the ddiff and the issue and describes the behaviour of the change. For this assignment its where antoher memebr reviews and comments, requests, changes and approves before a merge.

5. What is the purpose of code review?
A different member checks the changed lines againsts the requirement and acceptance criteria. They look for defects, broken responsibilities, weak assertions and unrelated changes before the code reaches main.

6. What does Git Diff show?
The lines added and removed between the versions. 

7. a shared set of criteria that a team uses to decide when a work item or product increment is officially complete and ready for release

8. A second opinion after the human reviewer has recorded their own observations. Ai can also be a quick way to check for extra stuff that could have been missed.Each significant suggestion is checked against the code, the requirements and an observed test run, then recorded as Accept, Modify or Reject.

9. Commit count depends on how people split their work and can be inflated. It ignores quality and ignores reviewing, testing, diagnosing, documenting and explaining.


10. Review eachothers code and utilise tools to help with checks and tests.

## M Completion and handover

- Starting SHA: 90d0d7f5c52379ab957e37cdd988c6a36017b675
- Final Stage 6 code SHA: 3ca7a3a4651d6751c8cb74133b316489cbe7407f (merge of PR #6)
- Test command: python -m pytest
- Working directory: project/ (repository root, then cd project)
- Observed result: All tests passed (33)
- PR and another-member reviewer: PR #4, PR #5 and PR #6, all reviewed by Tari Ganas
- Unresolved issue or none: Tari forgot to do a formal approval on PR #5
- Stage 7 handover status: Ready
- Final submitted SHA if later than tested SHA: SHA 3ca7a3a

- [ ] Three Stage 6 service targets completed and checked.
- [ ] Original supplied tests retained and passing.
- [ ] At least two focused issues link requirements and acceptance criteria.
- [ ] Feature work reviewed by another member using the actual diff.
- [ ] Human-first review and required Copilot comparison recorded.
- [ ] Feedback resolved and approval recorded before merge.
- [ ] Everyone pulled main and integrated checks passed.
- [ ] Required activities, quiz responses and contribution notes completed.
- [ ] Only synthetic data included; confidential peer material kept out.
- [ ] Tutor can trace a requirement through issue, code, tests, PR and checkpoint.

Do not write a file's own future commit SHA into that file. Record the tested code SHA first, then commit the evidence; explain the difference when submitting.
