# Stage 6 activities and evidence

Complete this one group record. Link actual issues, diffs, tests and reviews; avoid copying entire histories. Blank fields are intentional. Duplicate rows as needed. Use synthetic data only. Every member records their own meaningful contribution. Do not invent results, reviews or Copilot use.

- Group/tutorial: Wed 4:30 - 6:30 Group 3
- Members, GitHub usernames and cohorts: Andy Hoang, Denis Zimba, Tari Ganas, Ahron Singh typicalgeezer42
- Repository URL: [[response]](https://github.com/deniszimba/st1-assignment-3)
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
- Follow-up review question 1: [response]
- Follow-up review question 2: [response]
- Follow-up review question 3: [response]
- Follow-up review question 4: [response]
- Follow-up review question 5: [response]
- Additional questions if useful: [response]

## E Team workflow agreement

| Practice | Team agreement |
|---|---|
| Branch naming | [response] |
| Commit message convention | [response] |
| PR size | [response] |
| Another-member review requirement | [response] |
| Merge rule | [response] |
| Significant Copilot disclosure rule | [response] |

## F Issue and backlog index

Create at least two focused issues. Add a linked practitioner-lookup issue or an explicit supporting criterion with the tutor if needed to cover all three service targets.

| Issue link | Requirement | Owner | Acceptance criteria or precise link | Status |
|---|---|---|---|---|
| [issue 1] | [response] | [response] | [response] | [response] |
| [issue 2] | [response] | [response] | [response] | [response] |

## G Pull request evidence

Repeat this block per PR. Record actual events, not planned approvals.

- PR link and title: [response]
- Linked issue and requirement: [response]
- Feature branch: [response]
- Changed behaviour: [response]
- Meaningful commits: [links]
- Test command, directory and observed result: [response]
- Another-member reviewer: [response]
- Human observations recorded before Copilot: [link and time]
- Requirement, responsibilities, test assertions and unrelated-scope checks: [response]
- Key feedback: [response]
- Author response/change and verification: [response]
- Reviewer recheck and approval: [link]
- Merge outcome and SHA: [response]
- Significant Copilot assistance: [summary or none]
- Linked issue closure: [response]
- Each member updated main: [member and confirmation]
- Integrated verification after merge: [command, directory, result and code SHA]

## H Copilot collaboration record

Record meaningful required use, not every trivial completion. Repeat per significant interaction.

- Member and task: [response]
- Prompt/purpose and relevant issue/diff: [response]
- Summary of output: [response]
- Human check against actual code, requirements and tests: [response]
- Decision — Accept / Modify / Reject: [select]
- Reason: [response]
- Verification/evidence: [link and result]

## I Human versus Copilot review comparison

- Human reviewer noticed before consulting Copilot: [response]
- Copilot noticed: [response]
- Overlap: [response]
- What did the human reviewer notice that Copilot did not: [response]
- What did Copilot identify that the human reviewer initially missed: [response]
- Unsupported or incorrect Copilot suggestion: [response or none identified with explanation]
- Human judgement accepted, modified or rejected, and why: [response]
- Which evidence justified merge approval: [response]

## J Contributions

Repeat per member. Include only categories that describe actual work; write not applicable where appropriate. Pairing or mentoring can be supported by a short corroborated note.

- Member: [response]
- Implementation: [work and evidence]
- Testing: [work and evidence]
- Review: [work and evidence]
- Issue refinement: [work and evidence]
- Design and responsibility discussion: [work and evidence]
- Debugging or integration: [work and evidence]
- Documentation or team support: [work and evidence]

## K Exit question

Why is a high commit count not necessarily evidence of strong contribution?

[response]

## L Stage 6 formative questions

1. What is version control?

[response]

2. Why is a feature branch useful?

[response]

3. What makes a commit a good engineering commit?

[response]

4. What is a pull request?

[response]

5. What is the purpose of code review?

[response]

6. What does a Git diff show?

[response]

7. What is a Definition of Done?

[response]

8. What is the appropriate role of GitHub Copilot in pull-request review?

[response]

9. Why should individual contribution not be judged only by commit count?

[response]

10. What is the Stage 6 engineering rule?

[response]

## M Completion and handover

- Starting SHA: [response]
- Final Stage 6 code SHA: [response]
- Test command: [response]
- Working directory: [response]
- Observed result: [response]
- PR and another-member reviewer: [links]
- Unresolved issue or none: [response]
- Stage 7 handover status: [ready for tutor checkpoint / unresolved work]
- Final submitted SHA if later than tested SHA: [response and evidence-only difference]

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
