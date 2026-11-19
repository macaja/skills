---
name: spec-docs
description: Starts, writes and reviews the specification of a project in docs/projects/<name>/ - discovery, scope, design, architecture decision records (ADRs) and delivery plan - with rule ids a review can point at, a rule checker script, and plain-writing style. The specification is approved before any code. Use it when the user asks to start the docs of a new project, to write or review a discovery, scope, design, ADR or delivery document, or to check a spec. Also use it before writing code for a milestone of a project that has docs in docs/projects/.
---

# Spec docs

A project's specification lives in `docs/projects/<name>/`. It is written and approved before the code, and it stays in the repo after the project is finished, as a reference.

## Which file to read

| Task | Read |
|---|---|
| Start the documentation of a new project | `references/setup.md` |
| Write or review any project document | `references/writing.md` |
| Write code for a milestone | "Spec first", below |

When a task covers more than one row, read each file in the order of the table. The rules live only in `references/writing.md`. This file does not repeat them.

## What each document answers

| File (copied from `assets/template/`) | Answers |
|---|---|
| `01-discovery.md` | What problem we solve, for whom, what we know and what we do not know |
| `02-scope.md` | What we will do and what we will not do, and when it counts as done |
| `03-design/design.md` | How we will build it |
| `03-design/adrs/NNNN-<slug>.md` | One decision each, with the options we considered. ADR means architecture decision record. |
| `04-delivery.md` | The milestones, their order and status, the pull requests of each milestone, and which pull request to build first |

## How the text is written

Every document follows the plain-writing skill: about 80% of ASD-STE100, every fact kept, no fact added. A diagram is a small box drawing, with 6 boxes or fewer. The one exception is the dependency graph in `04-delivery.md` (rule L9), which stays in Mermaid. That graph can have more than 6 boxes, and GitHub draws Mermaid.

When the plain-writing skill is not installed, read it at `../plain-writing/SKILL.md`, in the same repo as this skill.

## Two scripts

Run both on every document you write or review:

```sh
python3 scripts/check_docs.py docs/projects/<name>            # the rules a machine can check
python3 ../plain-writing/scripts/check.py docs/projects/<name>/02-scope.md   # long sentences and formal words
```

Both paths are relative to this skill's folder. `check_docs.py` prints each broken rule as `<file>: <rule id>: <what is wrong>`. It does not check every rule: `references/writing.md` says which rules still need a person or a model to read the document.

## Spec first

A change in the behaviour of the code delivers a milestone with `Status: in progress` in `docs/projects/<name>/04-delivery.md`.

1. Before you write code, find that milestone.
2. Read what it delivers: the items and acceptance criteria in `02-scope.md`, and the matching parts of `03-design/design.md`.
3. When no such milestone exists, stop and tell the user.

Never write a project's documents and its code in the same pull request. The one exception is the pull request that finishes a milestone: it also moves that milestone's `Status:` line to `done`.

Two kinds of change need no milestone:

- A refactor that does not change behaviour.
- A bug fix that makes the code match acceptance criteria already in an approved `02-scope.md`.
