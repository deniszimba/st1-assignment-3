# Stage 12 activities and evidence

BLANK student response template. Supplied from the beginning in stage12/ in your EXISTING repository; complete it only when you reach Stage 12 after the previous applicable stage is integrated, verified and recorded; preserve project/, tests, earlier records and Git history. UG/common and PG/extended scope must be explicit. Use concise results and versioned links, not copied logs or source. No staff answers or fabricated approvals.

Group/tutorial: Tutorial: Wednesday 4:30-6:30, Group: 3
Members and UG/PG applicability: 
Andy Hoang, Denis Zimba, Tari Ganas and Ahron Singh. All members are UG.

## A Release scope and starting SHA

Release label/version and requirements baseline: 
Proposed SmartCare UG RC1, SmartCare A3 2026 revision 2.

Common starting SHA / branch / applicable members: 
Main at 3e260ca030adc4cb291bf635fa15348c1de864a1; applicable to all four members.

PG starting SHA / branch / applicable members or not applicable: Not applicable as all members are UG.

Working-state review and approved integration: 
PR #15 merged Stage 9 as `a5509994bd9c12beb9fea6f96bc91e0d3bbe2bf8`. PR #16 merged the Stage 8 cleanup as `56d80cdb1183734ad2698343079a6e18f54a1844`. PR #17 produced code/evidence SHA `3e260ca030adc4cb291bf635fa15348c1de864a1`. Commit `07fa711d8b04db43f5318447ae7a53fa59ceab51` later finalized the Stage 9 integration evidence and is the base of PR #18. A fresh clone was clean before testing.

Protected common candidate and PG differences: 
The common candidate is 3e260ca030adc4cb291bf635fa15348c1de864a1. There is no PG branch or PG difference.

Feature freeze / owner / verifier: 
Group member Andy is completing stage 12. Application code is currently frozen whilst the release documentation is corrected.

## B Requirements and release readiness matrix

Tutorial activity 1: All tests pass, README setup is incomplete, one dependency is unreviewed and a known limitation is undocumented. Decide Release / Release with conditions / Do not release and justify: 
The appropriate decision is Do not release yet. As passing tests do not compensate for incomplete setup documentation, an unreviewed dependency or an undocumented limitation. Those gaps must be corrected and the final candidate independently reproduced before release.


Tutorial activity 2 and actual readiness matrix. Add exact requirement/acceptance IDs, evidence and reviewer; distinguish common/PG applicability.

| Release claim / requirement / scope | Evidence | Location/link and SHA | Reviewer | Sufficient? | Gap/action |
|---|---|---|---|---|---|
| Cancellation history works | Cancellation history works | Cancelled appointments remain retrievable after cancellation | `project/tests/test_regressions.py`; tested at `1f77c75899876b7a737d864a9fe681d9b7e34ae0` | Denis reviewed Stage 8 | Yes | None found |

| Architecture responsibilities are appropriate | Domain, store, services, queries and console have separate responsibilities | `project/smartcare/`; Stage 9 B/E | Andy reviewed Stage 9 | Yes | Final release review not recorded |

| Rescheduling is safe — PG only | Not applicable as all members are UG. |

| AI use is responsible — common recheck / PG assurance| Human hypotheses and Accept/Modify/Reject decisions recorded | Stage 8 F and Stage 9 E | Andy and Denis | Partial | Final Stage 12 confirmation not recorded |

| System is maintainable | Focused modules, type hints, docstrings, named sorting key and 74 tests | Application source and tests | Stage 8/9 reviewers | Yes | Final release sign-off not recorded |


| FR-01–03 register/find and validation | FR-01–03 registration, lookup and validation | Valid, blank, trimmed, duplicate and unknown cases tested | Domain, service and Stage 6 tests | Tari and Ahron | Yes | None found |


| FR-04–05 booking/conflict rules | FR-04–05 booking and conflicts | Registered identity, exact conflict, different practitioner and released slot tested | Service, regression and workflow tests | Denis | Yes | Duration overlap is outside scope |


| FR-06–08 cancellation/history/find | FR-06–08 cancellation, history and lookup | Guarded cancellation, retained identity and lookup tested | Domain, service and regression tests | Denis | Yes | None found |

| FR-09 and QRY/FP listing/filter/order/purity | FR-09 and QRY/FP listing, filtering, ordering and purity | Fresh lists, enum filtering, time/ID order and source non-mutation tested | Query and workflow tests | Andy | Yes | Purity also relies on inspection |

| UI full console sequence and error recovery |Scripted real-menu workflows and invalid inputs tested | Workflow tests | Andy | Yes | Final independent reproduction not recorded |


| Session-only scope / FR-10 retired | README and demonstration disclose data loss on exit | README and source | Stage 12 local check | Yes | Accepted limitation |

| PG RES and assurance integration |  |


## C Full regression results

| Suite/scope | Environment/version | Working directory and command | Tested SHA | Actual result | Evidence link |
|---|---|---|---|---|---|
| Complete common | macOS; Python 3.14.7; pytest 8.3.5 | `project/`; `python3 -m pytest -q` | `1f77c75899876b7a737d864a9fe681d9b7e34ae0` | **74 passed in 0.04s** | `project/tests/` |

| Complete PG if applicable |  |Not applicable as all members are UG.

| Affected focused checks after correction |  | Focused checks | Python 3.14.7; pytest 8.3.5 | `project/`; `python3 -m pytest -q tests/test_regressions.py tests/test_queries.py tests/test_workflows.py` | `1f77c75899876b7a737d864a9fe681d9b7e34ae0` | **17 passed in 0.02s** | Named test files |

| Compilation check | Python 3.14.7 | `project/`; `python3 -m compileall -q smartcare main.py` | `1f77c75899876b7a737d864a9fe681d9b7e34ae0` | Passed with no compilation error | Local release-branch run |

| Full integrated recheck |  |


Prior assertions preserved / reviewed test diff: 
Reviewed test dif, showed that all accumulated stage 6-9 tests remain under 'project/tests/'. The release documentation commit does not change the application source. 
Remaining failure / limitation: 
No test or compilation failure was observed.

## D Console and end to end demonstration

| Demo step | Synthetic setup/input | Expected requirement | Observed result | Evidence/link |
|---|---|---|---|---|
| Problem and stakeholders 
| Synthetic clinic data | Explain registration, booking, cancellation and listing | Documented | Project README |

| Register and find Patient and two Practitioners 
| Register/find Patient and two Practitioners | P1, D1 and D2 | FR-01–03 | Registered and found successfully | Interactive run and workflow test |

| Valid booking | A1/P1/D1 at 09:00 | FR-04 | Stored successfully | Workflow test |

| Same practitioner exact-time conflict rejected | A2/D1 at A1 time | FR-05 | Rejected and A2 not stored | F8-01 regression |

| Different practitioner same time allowed | A2/D2 at A1 time | AC-04.2 | Booking succeeded | Workflow test |

| Cancel SCHEDULED and retain/find CANCELLED object | Cancel and find A1 | FR-06–08 | Same object retained as CANCELLED | F8-02 regression |

| Invalid/repeated cancellation rejected | Cancel A1 again | Cancellation guard | Rejected without deleting history | Domain/service tests |

| Default all-status listing | D1 with blank filter | QRY-02/04 | All matching statuses returned | Query/workflow tests |

| Explicit filtering / empty vs unknown / deterministic order | Status filters and practitioner IDs | QRY/FP | Correct filtered, empty or error results and deterministic order | Query/workflow tests |

| Invalid date/status/menu/lookup recovery and continued operation | Bad menu, date, status and lookup inputs | UI-02 | Error displayed and menu continued | Console recovery tests |

| Session-only limitation and normal exit | Demo and Exit option | Session scope | Clean exit and data-loss message | Demo and README |

| One meaningful requirement-linked pytest test explained | Requirement-linked test | F8-02 | FR-07 | Detects cancelled-history regression | Regression test |

| Architecture and one actual AI decision / known limitation | Concurrency suggestion | Scope control | Rejected as outside assessed UG scope | Stage 9 E/F |

| PG reschedule identity/participants/time and no-op 
| PG conflict/invalid status/failure non-mutation 
| PG old slot / current lookup/list ordering / assurance risks 
Stable demo owner / fresh process / command: 
Andy Hoang, the commands used were `python3 main.py` and `python3 main.py --interactive` from `project/`.

PG demonstrations through service/tests or not applicable: 
Not applicable as all members are UG.

## E Final code quality and AI review

| Review area | Code/evidence location | Finding or no finding | Correction/no change and recheck |
|---|---|---|---|
| OOP responsibilities and pure-query boundaries | SmartCare modules | Responsibilities appropriately separated | No code change |

| PascalCase and snake_case naming | Source inspection | Consistent | No change |

| Useful type hints and meaningful docstrings | Source inspection | Useful coverage | No change |

| Four-space indentation and imports/layout | Source and compilation | No compilation issue | No change |


| Focused methods / duplication / dead or commented code | Source inspection | No material release defect found | No change |

| Globals / leakage / unnecessary inheritance or frameworks | Source inspection | No unnecessary framework or global store introduced | No change |

| No SQLite/persistence/repository ABCs/speculative features | Source inspection | No SQLite or repository abstraction added | No change |

| Synthetic data / secrets / dependencies / provenance | Tracked files and dependency inspection | Synthetic data only; no tracked secret found | No change |

| Significant common Copilot contributions and human verification | Stage 8 F and Stage 9 E | Human decisions and test reruns recorded | Bounded tests accepted and concurrency rejected |

| PG plan/diff/test approvals and Stage 11 VERIFY/TRUST |

| AI claim | Affected requirement/code | Human check | Accept/Modify/Reject and reason | Actual outcome/action or no change |
|---|---|---|---|---|
|  | Add COMPLETED-filter, display-order and entry-point tests, consider concurrency protection | Query, service and UI | Compared with requirements, code and tests | Accept bounded coverage; reject concurrency as outside scope | Four tests added in `41beaa1`; full suite has 74 passing tests |

Access route or approved equivalent / limitations: 
GitHub Copilot use was recorded in Stages 6–9.

Available AI evidence and missing evidence honestly disclosed: 
Stage 8 records the Copilot debugging outputs and human evaluation decisions. Stage 9 then records the supplied promt, sumarise responses, accepted and rejected suggestions and resulting test evidence. A complete version stage 9 copilot transcript was not stored however, and no final stage 12 AI-provenance confirmation has yet been recorded.


## F README and reproducibility check

| README item | Location | Verifier | Result/gap |
|---|---|---|---|
| Purpose and included common/PG scope | Root/project README | Stage 12 local check | UG scope documented |

| Out-of-scope capabilities and known limitations | Project README/Stage 12 G | Stage 12 local check | Documented |

| Confirmed teaching Python version and dependency installation | README/requirements | Stage 12 local check | Actual environment recorded; pytest pinned |

| Working directory / demo / interactive / test commands | Project README | Local release run | Commands reproduced |

| Repository structure and architecture responsibilities | Project README | Stage 12 local check | Documented |

| Responsible AI summary / synthetic-data rule | Root/stage records | Stage 12 local check | Present |

| Release label/version and SHA links | Root README/Stage 12 | Stage 12 local check | Current candidate recorded |

Root README index and project/README verified: 
The root README was updated within the commit `1f77c75899876b7a737d864a9fe681d9b7e34ae0`. Group information, repository URL, completed stage, tested SHA and test commands were all added, and the project README contains setup, demonstration, interactive-menu and testing instructions.

Fresh clone or extracted ZIP / candidate identity: 
Tari independently extracted the 'SmartCare release check.zip' into a seperate directory outside the current working repository. The archives represented the release candidate after the stage 12 documentation and file name portability changes.

Verifier and clean environment / actual version: 
Tari performed the independent verification on macOS using python v3.14.3 and pytest 8.3.5. The extraction copt was tested seperately from the working repository.

Setup/run/test commands and observed results: 
The standard demonstration and ineractive console all ran smoothly with no bugs or problems. Practitioner conflict rejection, different practitioner same time booking, cancellation history retrival, filtering, no match handling and invalid input recovery were all verified. Finally, the completed extracted test suite produced: '74 passed in 0.08 seconds'.

Missing local file or setup gap / remedy and recheck: 
No mising dependencies, import, test discovery, or extraction problems occured or were found during the independent review. Additionally four non-ASCCI stage 8 screenshot filenames had previously caused an inconsistent ZIP filename comparison and were changed by the member resposible for the stage 8 work (Andy Hoang), this can be seen in PR#18, and then after which the archive was extracted and tested successfully by Tari.

## G Known limitations debt and release notes

Delivered features: 
Patient and practitioner registration and lookup, appointment booking and conflict protection, cancellation and retained history, filtered and ordered appointment listing, and finally an interactive console.

Important fixes: 
The most important fixes done would be repairing both F8-01 and F8-02. F8-01 repaired practitioner conflict comparison. F8-02 restored cancelled-appointment lookup. Then in Stage 8, we added an enum-based status refactor. Then in Stage 9 added queries, console integration and review tests.

Architecture/quality improvements: 
Shared in memory store, seperated responsibilities, pure queries and named ordering and key and 74 automated tests.

Known limitations: 
Session only data, naive minute precision date/time, no authentication, presistence, rescheduling, duration overlap, patient conflict, clinic hours validation, notifications, billing, insurance, or production monitoring. 

AI-assisted development note: 
The AI helped to provide bounded debugging and review suggestions. With humans verifying suggestions against requirements, source and tests, accepted useful coverage additions and rejected concurrency expansion outside the assessed scope.


| Debt item | Impact | Priority | Future action | Accepted? / release rationale |
|---|---|---|---|---|
|  |
| Session-only storage | All registered records are lost when the application exits | Expected scope limitation | Add persistence only under a future approved requirement | Accepted because FR-10 persistence was retired |

| Non-atomic booking conflict check | Simultaneous concurrent requests could potentially create a race condition | Low for the current single-user console | Introduce transactional conflict checking if concurrency becomes required | Accepted because concurrency is outside the assessed scope |

| Naive minute-precision date and time | The application has no timezone policy and does not support seconds | Medium for future production use | Define timezone and scheduling precision requirements before production use | Accepted as a documented limitation |

| Incomplete AI transcript metadata | Some AI provenance cannot be independently reconstructed from a complete transcript | Medium | Preserve full versioned prompts and responses in future stages | Accepted with honest disclosure because human decisions and test evidence are recorded |

Session-only synthetic data and minute-precision local time: 
SmartCare stores only the synthetic data inside the memory for its current session. Records are then intentionally lost when the program is exited, and the appointment times use naive local datetimes at minute precision. 

Production auth/roles, portal, notifications, billing/insurance, clinical AI exclusions: 
Authentication, user roles, patient portals, notifications, billing, insurance processing, and clinical AI are not implemented nor claimed to be. These capabilities would be outside the UG SmartCare release scope.

Scale/concurrency, timezone policy, operations/monitoring, accessibility/usability limitations: 
The application has not been production-assured for concurrent access, large0scale workloads, timezone handling, operation monitoring or even formal accessibility and usability requirements, as this application is a small, single process application. 

Difference between accepted scope limit and unresolved required behaviour: 
An accepted scope limitation concerns functionality that the approved requirements would purposefully exclude, these would include presistence, or concurrent booking. An unresolved requirement however would mean an applicable requirement is failing and would block release. No unresolved required application behaviour has been identified through the completed demonstration, focused tests or full suite.

PG assurance residual risks / owner / status or not applicable: 
Not applicable as all members are UG.
## H Release findings and corrective action

| Requirement/claim | Reproduction/observation | Impact/severity | Owner/action | Corrective diff | Focused/full recheck | Residual limit |
|---|---|---|---|---|---|---|
| Root README release-ready | Starter wording/placeholders identified | High | Andy updated README | `1f77c75899876b7a737d864a9fe681d9b7e34ae0` | README inspected and tests passed | Final submitted SHA not recorded |

| Stage 9 integration recorded | Final merge evidence was needed | High | Stage 9 record finalized | `07fa711d8b04db43f5318447ae7a53fa59ceab51` | Git history checked | None found |

| Earlier records accurate | Stage 6 placeholder and Stage 8 stale handover found | Medium | Andy corrected grounded wording | 
`1f77c75899876b7a737d864a9fe681d9b7e34ae0` | Diff and stale-text check | Historical PR #5 approval gap disclosed |

| Candidate code passes | Full/focused tests and compilation | No code defect | No executable change required | None | 74 full and 17 focused tests passed | Tests are not exhaustive |


Justified no-change conclusion if no defect found: 
No application defect was found during the independent demonstration, interatcive console verification or complete regression run. The file name correction was limited to evidence file portability and did not alter the application source or required behaviour in any manner.

Release blockers still open / status: 
Independent ZIP verification and human approval are all completed. PR#18 and the file name portability correction in PR19 have all been merged successfully with no issues. Therefore the remaining work would be to merge the final stage 12 evidence update and record the final main SHA and generating the SmartCare release zip from that SHA, then finally verifying the final archive before submission.

## I Git review and integration evidence

Issue / PR / diff links and reviewed SHA: 
PR #15 integrated Stage 9, PR #16 integrated the Stage 8 cleanup and PR #17 integrated the final Stage 8 evidence. [PR #18](https://github.com/deniszimba/st1-assignment-3/pull/18) contains the Stage 12 documentation changes. Current `main` is `07fa711d8b04db43f5318447ae7a53fa59ceab51`.

PR #18 recorded the Stage 12 documentation, feedback resolutions and release-check evidence and was merged as ec4418fbaa311f056902bc94095786c10f67e86f. PR #19 corrected the four non-ASCII Stage 8 evidence filenames and was merged as 03fbe163e6dcf40c1d295c6cea192413492e6de5.


Independent reviewer / feedback / response: 
Tari independently extracted and verified the release check ZIP for Smartcare on macOS using python 3.14.3 and pytest 8.3.5. Tari then helped to confirm that the demonstration, interactive console and required behavioour all worked and the full extracted suite produced '74 passed in 0.08 seconds'. Therefore with all this no extraction, dependency, import or test discovery issues were found and Tari approved the candidate for course release (seen in his comment in PR#18).

Integration commit / full recheck: 
PR#18 was integrated as 'ec4418fbaa311f056902bc94095786c10f67e86f', and PR #19 was integrated as '03fbe163e6dcf40c1d295c6cea192413492e6de5'. The independently extracted candidate subsequently produced 74 passed in 0.08 seconds.

Tracked and untracked file inspection / cleanliness: 
The candidate excluded the Stage 8 preparation utility, local recovery metadata, environments, caches and duplicate application copies. The regression test is stored with the accumulated suite under project/tests/. The four affected screenshot filenames were converted to portable ASCII names through PR #19.

Secrets/staff material/caches/tool-metadata exclusion check: 
No tracked `.env`, virtual environment, cache, Stage 8 utility, recovery metadata or real patient data was found.

Candidate recovery plan / known-good SHA: 
The tested executable candidate can be recovered at `1f77c75899876b7a737d864a9fe681d9b7e34ae0`. Commit `821e06285dae624ac921bb718c593a89ba836084` contains subsequent Stage 12 documentation only and does not modify application code or tests. The pre-PR `main` branch can be recovered at `07fa711d8b04db43f5318447ae7a53fa59ceab51`.

Named substantive contributions: 
Ahron contributed to the stage 6 services and the stage 7 follow up tests. Tari contributed to stage 6-7 tests, reviews and integration. Andy completed stage 8 repairs, tests, refactoring, cleanup, stage 9 review and stage 12 documentation. Denis completed stage 9 queries, services and console and tests and reviewed stage 8.

## J Human release decision

Decision — READY FOR COURSE RELEASE / READY WITH DOCUMENTED LIMITATIONS / NOT YET READY: 
Ready with documented limitations.

Approver / date / rationale and evidence: 
Tari approved the candidate on November 7th 2026 after his independent extraction and test of all the archives. The demonstration and interactive console worked, the required behaviours were reproduced and all 74 tests passed. All of this evidence can be seen in his comment in PR#18.

What risks remain / conditions / owners: 
The accepted limitations include session only storage, naive miniute precision local date and time values and the absense of production authentication, concurrency protection, notification, billing, monitoring and a formal timezone policy. The final evidence update was merged and the submitted source candidate was recorded as '09b70dc38ef309d2d02e6d513e5a88ec3ba77fd0'. Then the Smartcare release zip was generated from that commut, then extracted independently and was verified with 74 passing tests. Finally, only the confirmed assessment submission and the seperate reflection, peer assessment and oral video remain, these are left uncompleted as their deadlines are significantly after this assignment, and can only be attempted after the submission/completion of this assignment.

Can the team explain the system: 
Yes, the group staged evidence all identifies the responsibilities of the domain, data store, services, queries and console. It also records debugging repairs, regression tests, AI assisted suggestions, human decisions and accepted release limitations.

Can a change be recovered: 
Yes, the release work is recoverable through the repository history, recorded commit SHAs and pull requests and the technical and packaging candidates can all be reconstructed from the recorded integration commits. 

Common decision / PG decision where different: 
The common UG decision is ready with documented limitations but the PG decision is not applicable as every group member is a UG student.

## K Final tested release SHA

Exact common tested SHA: 
`09b70dc38ef309d2d02e6d513e5a88ec3ba77fd0`.

Exact PG tested SHA or not applicable: 
Not applicable as all members are UG.

Final submitted SHA / repository URL: 
Final submitted source SHA: 09b70dc38ef309d2d02e6d513e5a88ec3ba77fd0, Repository URL: https://github.com/deniszimba/st1-assignment-3.

Evidence-only later commit and difference explanation: 
The submitted source candidate is '09b70dc38ef309d2d02e6d513e5a88ec3ba77fd0', a later evidence only documentation only change records the ZIP hash and post-port verification results It only changes the stage 12 activitiy md file and doesn't change the application source, dependencies or tests. 


Executable changes after testing and re-verification: 
None, the archive was generated directly from '09b70dc38ef309d2d02e6d513e5a88ec3ba77fd0' and then extracted into a seperate direcrtory and tested without modifying its contents.

Source ZIP name / SHA correspondence / extracted comparison: 
`SmartCare-release.zip` was generated with `git archive` from `09b70dc38ef309d2d02e6d513e5a88ec3ba77fd0`. Its SHA-256 is `de555abd3ee8bf6cf1b13e6d171a8f44a8e805237ed382b41e232c2ee55c6aef`. `unzip -t` was used to report no errors, the Git tree to zip file comparision also produced to differences and the seperately extracted archive produced 74 passed tests in 0.08 seconds using Python 3.14.7 and pytest 8.3.5.

## L Submission package verification

- [x] Feature freeze and scoped requirements traced.
- [x] Applicable full regressions, integrated demo and invalid paths verified.
- [x] Architecture/code quality and final AI/dependency checks complete.
- [x] Root README and project/README reproduced by another verifier.
- [x] Release notes, technical debt and limitations visible.
- [x] Independent human review, integration and release decision recorded.
- [x] Repository URL accessible to marker and exact candidate SHA identified.
- [x] One source ZIP from submitted commit with root README.md and .gitignore.
- [x] project/ source and all accumulated applicable tests included.
- [ ] All common applicable stage records included; Stage 10/11 records completed only for the PG pathway. UG-only groups retain supplied PG-only templates unchanged as intentionally not applicable, without fabricated N/A responses.
- [x] No .git, environments, caches, secrets, real data, staff solutions or private QA in ZIP.
- [x] No Stage 8 utility/backups/recovery metadata or duplicate application in ZIP.
- [x] Mixed-group common protection and candidate upload routing checked.
- [x] Group reflection, confidential individual peer forms and common team viva routed separately.

Confirmed assessment item/upload route: 
Deadline/timezone: 
Repository access arrangement: The group repository is available at https://github.com/deniszimba/st1-assignment-3. 

Mixed-candidate upload arrangement: 
Not applicable. All four group members are completing the common UG pathway, so the group will submit one common release candidate rather than separate UG and PG candidates.

Oral/video recording/accessibility arrangements:


Remaining administration or release dependency: 
Independent review, PR #18 integration and independent extracted-ZIP verification are complete. The remaining work is to merge the final Stage 12 evidence update, record the resulting final main SHA, generate SmartCare-release.zip from that exact SHA, calculate its SHA-256 hash, extract and test the final ZIP, and submit it through the confirmed assessment route. The group must also complete any separately required reflection, confidential peer-assessment and viva/video submissions.


## M Formative questions

1. What is a release candidate? 
A release candidate is an exact software version that is belived to be suitable for release but can still be subject to final verification and approval

2. What is feature freeze and why is it used? 
Feature freeze stops unapproved functionality from being added whilst the candidate is tested, this helps to reduce to risk of the tested version being changed unexpectedly.

3. What is regression testing in a release context? 
Regression testing reruns accumulated tests against the integrated candidate to detect possible damage to previously working behaviour..

4. What is a known limitation? 
A known limitation is a disclosed unsupported capability or condition with an understood impact.

5. What is technical debt? 
Technical debt is a weakness that increases the future costs or risks and should be properly recorded, prioritised and assigned.

6. What are release notes? 
Release notes summarise features, fixes, quality improvements, setup information and limitations.

7. What is software maintenance? 
Software maintanence is correcting, adapting, and improving software even after inital development whilst still preserving its required behaviour.

8. What is the purpose of the individual demonstration/viva? 
It verifies that each member can independently explain the system, evidence and their own personal contribution.

9. What should the final responsible-AI check establish before release? 
It should establish permitted use, provenance, human verification, protection of sensitive information and accountable decisions.

10. What is the main course conclusion about AI and the role of the software engineer? 
AI can help accelerate suggesions but engineers should always remain responsible for requirements, architecture, evidence, testing and risk and approval. 

## N Reflection viva and handover

Strongest evidence SmartCare is ready: 
The strongest evidence is that the tested executable candidate passed all 74 tests, the 17 focused tests and the compilation check, while earlier demonstrations covered the required workflows and recovery cases.

Weakest area: 
Independent release review, final merge and ZIP verification.

How AI use changed from Stage 1 to Stage 12: 
By stages 8 and 9 particularly, AI was treated as a bounded second opinon that helped to check against requirements, source codes and tests.

Start doing — engineering and AI use: 
Record any huamn reasoning before AI consultation and verify all clean candidates immediately after integration. 

Stop doing — engineering and AI use: 
Stop treating AI claims or one local test run as solid release proof.

Continue doing — engineering and AI use: 
Continue to use requirement linked changes, regression tests, exact SHA's and the accept, modify, and reject decision making. 

What worked / caused rework / future delivery improvement: 
Small repairs and focused testing worked especially well, late correction and utility placement and stale evidence did cause rework. But within future projects it is necessary to perform evidence and cleanliness checks immediately after every merge. 

One paragraph — If AI can write code why do we still need software engineers: 
AI can very well produce plausible suggestions, but it does not own requirements, or observe every runtime fact or even accept responsibilities for the outcome. Software engineers however help constrain scope, protect data, inspect architectures, test behaviour, resolve confliction evidence and decide which exact version is ready and safe to release. For example, within SmartCare's accepted test suggestions and rejected concurrency expansions, it demonstrates why accountable human judgement will always remain necessary.

| Preparation item | Own explanation and evidence link |
|---|---|
| Problem and stakeholders | Synthetic small-clinic workflow and project README |


| Two requirements and acceptance criteria | FR-05 conflict rule and FR-07 retained history and Stage 8 regressions |

| Domain model and architecture | Domain, store, service, query and console responsibilities |

| Design trade-off | In-memory simplicity versus loss on exit |

| Meaningful test and its limits / 100 percent coverage | F8-02 detects cancelled-history regression and tests cannot prove every input |

| Diagnosed defect and verification | Reversed comparison and cancelled lookup filter |

| Shared store and session-state/query responsibilities | One session store and explicit-input fresh-list queries |

| What would break if session-state lookup/query responsibilities changed? | Recreated stores lose state and storage-owning queries break purity |

| Why cancellation is domain behaviour / conflict coordination is service behaviour | Domain guards status and service coordinates conflicts |

| FR-07 retained history test | `test_f8_02_cancelled_appointment_remains_retrievable` |

| Actual AI change rejected/modified or honestly accepted with verification | Concurrency rejected and bounded test coverage accepted |

| Unresolved limitation / future production work | Persistence, authentication, timezones and concurrency |

| Personal implementation contribution | Andy completed Stage 8 repairs, tests, refactor and cleanup and stage 12 documentation |

| Personal test/review/design/integration contribution | Andy reviewed Stage 9 and prepared Stage 12 documentation |

| PG agentic change and rescheduling verification | Not applicable as all members are UG students.

| PG responsible-AI risk/remediation or supported no finding |Not applicable as all members are UG students.

Optional bounded-change practice only: validation rule, focused test, safe error-message change, explicit-input query or agreed status rule with test. Explain expected impact before editing, make a small change, run the test, and identify evidence to inspect if unsure. No live AI unless explicitly permitted. Preserve the submitted candidate.

Practice question/change and reasoning: [response or not undertaken]
Separate reflection / peer / common team viva evidence links and routing: 
No further coding stage. Later corrections use the published assessment process.
