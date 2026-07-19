## ADDED Requirements

### Requirement: Treat bug reports as evidence
The local bugfix workflow SHALL treat a reported symptom as evidence to investigate rather than as the final bug definition or component boundary.

#### Scenario: A new symptom is reported
- **WHEN** a player, human reviewer, or coding agent reports incorrect behavior
- **THEN** the investigation SHALL separately record the clue, a faithful reproduction, the candidate or confirmed violated rule, and the verification status
- **AND** it SHALL NOT name a root cause solely from the report or an existing patch description

### Requirement: Confirm the violated rule before integration
A bugfix SHALL identify the logical owner and violated rule that explain the reproduced symptom before the fix is integrated or prepared as an upstream change.

#### Scenario: A candidate cause is proposed
- **WHEN** an investigation proposes a cause
- **THEN** it SHALL trace relevant writers, readers, resets, and sibling paths
- **AND** it SHALL state observations that could disprove the cause
- **AND** static inspection without runtime evidence SHALL remain labelled as a candidate cause

### Requirement: Evaluate a preventive local refactor
Every confirmed bugfix SHALL evaluate whether a local refactor at the rule's owner can prevent the same invalid state across sibling paths.

#### Scenario: The same rule is repeated or inferred by callers
- **WHEN** several callers repeat a predicate, cleanup sequence, temporary mutation, or lifecycle guess
- **THEN** the design SHALL prefer one owner-level operation or predicate when it removes the failure mechanism without changing unrelated game semantics
- **AND** the design SHALL explain why a narrow patch is retained when no refactor is justified

### Requirement: Group fixes by cause and owner
Bugfix boundaries SHALL be chosen by shared behavioral contract, violated rule, logical owner, and state lifecycle rather than by file proximity, feature label, historical report, or the number of test surfaces required.

#### Scenario: Two symptoms are considered for one fix
- **WHEN** two symptoms share the same owner-level rule and lifecycle
- **THEN** they MAY be handled by one coherent fix with one causal verification matrix

#### Scenario: Two patches touch the same area for different reasons
- **WHEN** two patches have different owners or failure mechanisms
- **THEN** they SHALL remain separate even if they touch the same file, flag, panel, or gameplay feature

### Requirement: Audit multiple mods before regrouping them
A multi-mod bugfix audit SHALL inventory the in-scope mods, investigate disjoint owners or lifecycles independently, and synthesize boundaries only after each investigation records the same evidence fields.

#### Scenario: Existing bugfix mods are considered for consolidation
- **WHEN** several local mods may overlap or encode ad hoc fixes
- **THEN** production edits SHALL remain frozen during the comparative investigation
- **AND** each investigation SHALL record its evidence status, violated-rule candidate, logical owner, unresolved semantics, and proposed disposition
- **AND** the synthesis SHALL account for every in-scope mod or name its coordination exclusion

### Requirement: Compare the actual semantic delta of an existing patch
An existing mod SHALL be evaluated against both its original upstream basis when reconstructable and current upstream, rather than treating its copied implementation or tests as an authoritative contract.

#### Scenario: A mod is retained, split, or replaced
- **WHEN** an audit decides the disposition of an existing patch
- **THEN** it SHALL compare current upstream with the mod disabled, enabled alone, and composed with directly related mods
- **AND** it SHALL record upstream drift or an unreconstructable original basis
- **AND** an exactly-once claim SHALL define stable operation identity and nested or re-entrant behavior

### Requirement: Build an assumed-upstream baseline before regrouping remaining mods
When an in-scope local responsibility has an active upstream PR that is accepted as the local development assumption, the development branch SHALL apply the exact PR commit to core and disable the duplicate mod responsibility before deeper refactoring or gameplay verification.

#### Scenario: One PR replaces an entire live mod responsibility
- **WHEN** the PR patch covers every reachable behavior owned by a local bugfix mod
- **THEN** the development configuration SHALL disable that mod after applying the core patch
- **AND** verification SHALL exercise the core implementation without the wrapper present

#### Scenario: One PR replaces only part of a mixed mod
- **WHEN** the mod also owns unrelated behavior not covered by the PR
- **THEN** only the matching wrapper, registry mutation, tests, and documentation SHALL be retired
- **AND** the remaining mod behavior SHALL delegate to corrected core rules where applicable rather than copying them

#### Scenario: The upstream PR later changes or is rejected
- **WHEN** the assumed upstream patch is no longer the intended integration commit
- **THEN** its overlay SHALL be independently replaceable or revertible without restoring unrelated retired responsibilities

### Requirement: Verify the causal radius
Each replacement bugfix SHALL prove the original symptom, sibling entry and cleanup paths, unchanged inverse cases, and supported mod composition before it is considered complete.

#### Scenario: A replacement fix is verified
- **WHEN** a candidate replacement passes its focused regression
- **THEN** verification SHALL also run with unrelated local mods disabled
- **AND** wrapper or registry changes SHALL load through the real mod loader
- **AND** Tk and Web behavior SHALL both be checked when the change affects input, waiting, panels, or visible settlement
- **AND** the record SHALL distinguish automated, manual, and static evidence

### Requirement: Isolate upstream candidates in linked worktrees
Every direct upstream candidate SHALL be prepared in a new linked worktree of the main repository from current `upstream/master`, rather than in an independent clone or the local integration checkout.

#### Scenario: A direct upstream candidate starts
- **WHEN** a root-cause fix has a narrow independently reviewable contract
- **THEN** it SHALL receive one `codex/` branch and linked worktree created from current `upstream/master`
- **AND** unrelated integration commits, mods, and central OpenSpec artifacts SHALL remain outside its proposed public diff

### Requirement: Gate candidates on local evidence and fresh review
Each direct upstream candidate SHALL stop locally with a PR draft, repeatable reproduction, appropriate evidence, and fresh-context review until the user authorizes outward actions.

#### Scenario: A candidate is ready for user review
- **WHEN** its root-cause fix and causal-radius tests pass
- **THEN** a local Chinese PR draft SHALL explain the player-visible problem, confirmed cause, final fix, and only verification represented by the candidate
- **AND** every candidate that changes game behavior SHALL provide one repeatable representative player flow and inspected, comparable before/after images from the real Tk renderer
- **AND** one main, easy-to-understand case SHALL be sufficient even when the same rule covers sibling cases
- **AND** a chance-dependent flow MAY be discovered through bounded, recorded manual Tk exploration before its successful checkpoint and player-action route are frozen
- **AND** deterministic A/B evidence SHALL restore the same Python and NumPy random state after loading, use a stable `PYTHONHASHSEED` and interpreter, and keep UI operation manual
- **AND** a separately reviewed compatibility PR MAY be applied identically to both local evidence runtimes when required to load the same checkpoint, but its files and claims SHALL remain outside the candidate's proposed diff and PR artifacts
- **AND** state assertions SHALL supplement rather than replace those images, and a candidate whose behavior cannot be truthfully exposed by any representative Tk case SHALL remain blocked
- **AND** a fresh-context reviewer SHALL inspect only the diff, reproduction, evidence, and draft for scope leakage and human-reviewability
- **AND** no branch, screenshot, or PR SHALL be published before user authorization

#### Scenario: A guessed player route is not scheduler-reachable
- **WHEN** a static path estimate or earlier trial does not produce the target behavior through the normal scheduler
- **THEN** the investigation SHALL record why the route failed and SHALL NOT present its frames as PR evidence
- **AND** later trials MAY change the checkpoint, public destination, NPC, time window, or normal player actions based on observed Tk behavior
- **AND** a route SHALL be promoted only after two identical baseline repetitions reach the public destination and select the affected template under the recorded random environment
- **AND** the baseline and candidate visual runs SHALL use that same checkpoint, action route, and random environment through a local visual subagent that inspects each captured Tk frame before choosing and issuing one local UI action
- **AND** the visual run SHALL NOT use blind coordinate or command batches, direct gameplay-state mutation, VNC/noVNC, or a network relay

### Requirement: Bound concurrent Tk evidence capture
The local workflow SHALL provide exactly three supervised Tk capture slots so unrelated PR evidence tasks can run concurrently without sharing a display, runtime, or process lifetime.

#### Scenario: A session starts a Tk evidence run
- **WHEN** a session requests a capture slot
- **THEN** it SHALL acquire one free slot for the full supervised command lifetime
- **AND** the slot SHALL own an isolated Xvfb display, runtime sequence, owner metadata, and cleanup boundary
- **AND** one candidate's baseline and candidate SHALL run sequentially within that slot
- **AND** a game already running outside the allocator SHALL reserve one of the three capacities until it exits
- **AND** OpenSpec and project-local skill edits SHALL remain serialized in the main worktree rather than follow the parallel runtime slots

### Requirement: Make every upstream PR draft independently understandable
Every upstream PR title and body SHALL be reviewed by an independent agent for self-containment, absence of redundant information, and prefix-by-prefix comprehensibility in the upstream review context.

#### Scenario: A PR draft enters final review
- **WHEN** a candidate implementation, submitted tests, and PR-visible evidence are fixed
- **THEN** the independent reviewer SHALL receive only the proposed upstream diff, final title/body, and evidence that will actually appear in the PR
- **AND** the title/body, initial PR-evidence prose, and every later prose revision SHALL be authored through an Agent/Workflow writer using `fable-5` at medium effort
- **AND** every claim SHALL be understandable to an erArk player who has no prior knowledge of the reported bug or proposed code
- **AND** the opening SHALL name the exact feature or scene and wrong behavior without teaching familiar gameplay
- **AND** an existing term used directly by game code or dialogue MAY stand unexplained, while a coined or private term SHALL be defined before use or removed
- **AND** the text SHALL NOT depend on local-only tests, local paths, unpublished notes, assumed overlays, or implementation drafts
- **AND** every sentence SHALL be necessary to explain the problem, root cause, chosen fix, review boundary, or submitted verification
- **AND** terms and context SHALL be introduced before use so every prefix of the title/body is coherent without relying on later text
- **AND** standalone inventories of non-goals or omitted work SHALL be removed unless a boundary is required next to a claim to keep it accurate
- **AND** character examples in the title/body SHALL use standard operators and canonical display names rather than child-operator names, nicknames, or local/custom names that require unstated context
- **AND** actionable failures SHALL require a rewrite and another independent review before the candidate can be called ready

### Requirement: Keep declared new-function registration consistent
A declared `type: new` function with `register_to` SHALL be published to the loader registry and target module as one locally atomic registration operation.

#### Scenario: Target registration fails
- **WHEN** the target module cannot be resolved or its function attribute cannot be assigned
- **THEN** the mod load SHALL report an error rather than success
- **AND** the loader registry and target module SHALL retain the values they held before that registration attempt

#### Scenario: Target registration succeeds
- **WHEN** the target module resolves and accepts the declared function attribute
- **THEN** the loader registry and target module SHALL expose the same new callable
- **AND** existing successful replacement behavior for prior values SHALL remain unchanged

#### Scenario: No target module is declared
- **WHEN** a `type: new` entry omits `register_to`
- **THEN** it SHALL remain a registry-only registration

### Requirement: Keep PR verification claims within submitted visibility
An upstream PR draft and its PR-facing evidence SHALL describe only implementation context, automated proof, and external evidence that the upstream reviewer will actually receive.

#### Scenario: An automated check is mentioned
- **WHEN** a draft or PR-facing evidence names a test, benchmark, command, count, result, or conclusion derived from that check
- **THEN** the proposed diff SHALL contain the check's logic and every required fixture
- **AND** a local-only or unchanged upstream test SHALL NOT be mentioned as PR verification

#### Scenario: Local investigation produced useful proof
- **WHEN** a temporary probe, local-only test, worktree output, OpenSpec note, agent review, or private benchmark informed the change
- **THEN** it SHALL remain outside the PR draft and PR-facing evidence
- **AND** renaming it as a reproduction, script, or manual check SHALL NOT make it PR-visible

#### Scenario: Required behavior images await publication approval
- **WHEN** inspected before/after images for a behavior-changing fix have not been uploaded
- **THEN** the artifact review MAY mark the draft local-review-ready with explicit pending-publication placeholders
- **AND** it SHALL NOT mark the draft publication-ready until user-approved public URLs replace them

#### Scenario: A draft enters the final artifact gate
- **WHEN** implementation and evidence are fixed
- **THEN** a fresh-context reviewer SHALL build a visibility ledger from the exact proposed diff and review every title, body, and PR-facing evidence artifact
- **AND** actionable findings SHALL be revised and reviewed again before the candidate is called ready

#### Scenario: A user-facing HTML review bundle is generated
- **WHEN** local PR candidates are collected for human review
- **THEN** the HTML SHALL include only candidates with an inspected representative Tk sequence, current Opus-authored PR-facing prose, and a passing fresh-context prefix audit
- **AND** blocked investigations SHALL remain in OpenSpec or private evidence records rather than filling the review page
