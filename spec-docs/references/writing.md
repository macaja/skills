# Writing and reviewing project documents

Each rule has an id, so a review can point at it. A document is `approved` only when it breaks no rule.

## Rules for every document

- **G1** The first line after the title is `Status: draft | in review | approved`. ADRs use `Status: proposed | accepted | superseded by NNNN` instead.
- **G2** Every section from the template is present. A section that does not apply says `Not applicable: <reason>`.
- **G3** An `approved` document or `accepted` ADR has no `TODO` or `TBD`. Unknowns go in the `Open questions` section, each with an owner.
  - An `approved` document keeps only questions marked `(not blocking)`. The answer to such a question changes no `In scope` item, acceptance criterion or design decision.
  - ADRs have no `Open questions`, so an ADR with unknowns stays `proposed`.
- **G4** Every statement about existing code names the file path.
- **G5** Information lives in one document only. Other documents link to it and do not repeat it.
- **G6** Acronyms are spelled out the first time they appear.
- **G7** Under 200 lines. A longer document is split.
- **G8** A document moves to `in review` when the pull request that proposes it is opened. Only a person sets `approved` (or `accepted` for an ADR). They do it in a commit of its own, with the footer `Approved-by: <name>`. The agent that wrote or reviewed the document never does.
- **G9** The text follows the plain-writing skill: every fact kept, no fact added, short sentences, common words. `plain-writing/scripts/check.py` reports nothing, or each finding is kept on purpose.

## Discovery (`01-discovery.md`)

- **D1** The problem is stated in 1 to 3 sentences, and says who has it.
- **D2** Every item under `Evidence` has a source: a link, a data query or a named person.

## Scope (`02-scope.md`)

- **S1** `In scope` and `Out of scope` are lists of one-line items.
  - Every `In scope` item starts with an id: `I1`, `I2`, and so on, in order.
  - Every `In scope` item has its own subsection under `Acceptance criteria`, titled `I<n>: <item>`, with at least one criterion. Each criterion starts with its own id `I<n>.<m>` (`I1.1`, `I1.2`, and so on).
  - Ids are never renumbered or used again. A removed item or criterion takes its id with it.
  - Other documents, pull requests and tests refer to items and criteria by id, never by their text.
- **S2** Each item in `Definition of done` can be answered yes or no by someone who did not write it.
- **S3** Every acceptance criterion is delivered by at least one milestone in `04-delivery.md`, through its own id or the id of its item.
- **S4** Each acceptance criterion describes one behaviour.
  - The behaviour can be seen from outside the code, and someone who did not write it can answer yes or no.
  - `Acceptance criteria` checks each `In scope` item on its own. `Definition of done` checks the project as a whole. So the same check never appears in both.

## Design (`03-design/design.md`)

- **E1** Every `In scope` item id from `02-scope.md` appears in a section of the design.
- **E2** Every choice with more than one reasonable option has an ADR with `Status: accepted`, and the design links to it.
- **E3** Every external call and every input lists what happens when it fails or is not valid.

## ADRs (`03-design/adrs/`)

- **A1** One decision per file, named `NNNN-<slug>.md`, numbered in order from `0001`. New ones are copied from `0000-template.md`.
- **A2** `Options` lists at least two options, each with its downside.
- **A3** An `accepted` ADR is never edited. To change it, write a new ADR with `Supersedes: NNNN`, and set the old one to `Status: superseded by NNNN`.
- **A4** Some ADRs make a design or architecture decision: how the pieces of the system are built, or how they talk to each other. Such an ADR has a box diagram in its `Diagram` section.
  - The diagram shows what the chosen option does, main steps only, with 6 boxes or fewer.
  - It uses box-drawing characters in a `text` code block, as the plain-writing skill describes.
  - Any other ADR writes `Not applicable: <reason>` there.

## Delivery (`04-delivery.md`)

- **L1** Every milestone has a goal, a definition of done that can be answered yes or no, and a status: `not started | in progress | done`.
- **L2** Every milestone lists in `Delivers` the ids from `02-scope.md` that it delivers. An item id (`I1`) means all its criteria. A criterion id (`I2.1`) means only that one.
- **L3** A milestone moves to `in progress` in a pull request that changes only documentation. This happens once L4 holds, and before any of its code. It moves to `done` in the pull request that finishes its work. A change to the `Status:` line of a milestone is not an edit to the content of an approved `04-delivery.md`.
- **L4** A milestone moves to `in progress` only when `02-scope.md`, `03-design/design.md` and `04-delivery.md` have `Status: approved`. No code is written for a milestone before that (see "Spec first" in `SKILL.md`).
- **L5** A milestone moves to `done` only when every acceptance criterion it delivers has at least one passing test marked with its id.
  - The mark is a comment in the test with the project folder name and the id: `// <name> I<n>.<m>`.
  - When no automated test can check a criterion, it needs a manual check. Write the manual check in the `Testing instructions` of that pull request.
- **L6** Every milestone has a `Deliverables` table. Each row is one pull request, with these columns:
  - `Id`: `M<k>.<n>` inside milestone `M<k>` (`M1.1`, `M1.2`, and so on). Ids are never renumbered or used again.
  - `Type`: the Conventional Commits type and optional scope of the pull request title, for example `feat(scoring)`, `docs(runbook)`, `build(scripts)` or `ci`. The types are `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore` and `revert`. A pull request that needs two types is two deliverables.
  - `What it changes`: one line.
  - `Delivers`: the ids from `02-scope.md` that it delivers. Write `—` when it delivers none, for example a build script or a continuous integration (CI) job.
- **L7** Every id in the `Delivers` line of a milestone appears in the `Delivers` column of at least one of its deliverables.
- **L8** A `docs` deliverable is documentation that the project produces, like a runbook or a user guide. It is never a file under `docs/projects/<name>/`. Those files change in pull requests of their own (see "Spec first" in `SKILL.md`).
  - The documentation-only pull request that moves a milestone to `in progress` (L3) is not a deliverable.
  - The move to `done` goes in the pull request of the last deliverable of the milestone.
- **L9** The `Dependencies` section has one Mermaid `flowchart`, and it is the only place where dependencies are written. This is the one diagram in Mermaid: it can have more than 6 boxes, and GitHub draws it.
  - It has a `subgraph` per milestone, and one node per deliverable with its id and type as the label: `M1_1["M1.1 build(scripts)"]`. Mermaid node names cannot contain dots.
  - An arrow `M1_1 --> M1_2` means that `M1.2` cannot start until `M1.1` is merged.
  - It has no cycles, and no arrow from a later milestone to an earlier one.
  - Implementation starts at the deliverables with no arrow coming in. Deliverables with no path between them can be built in parallel.

## How to review

1. Run `scripts/check_docs.py docs/projects/<name>`. It checks G1, G2, G3, G7, S1, S3, E1, A1, L1, L4, L6 (the ids and types), L7 and L9.
2. Run `plain-writing/scripts/check.py` on each document for G9.
3. Read the document for the other rules: G4, G5, G6, G8, D1, D2, S2, S4, E2, E3, A2, A3, A4, L2, L3, L5 and L8.
4. Report each broken rule as `<file>: <rule id>: <what is wrong>`. For example: `02-scope.md: S3: I3.2 has no milestone in 04-delivery.md`.
5. When no rule is broken, say so. Leave `Status: approved` to a person (G8).
