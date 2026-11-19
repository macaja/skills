# skills

Personal skills for Claude Code.

| Skill | What it does |
|---|---|
| [explain-me](explain-me/SKILL.md) | Explains things with a ladder of formats: text close to ASD-STE100, then a diagram, then an interactive page on claude.ai, and last a video. |
| [spec-docs](spec-docs/SKILL.md) | Starts, writes and reviews a project specification in `docs/projects/<name>/`, approved before any code. Rules have ids, and a script checks the ones a machine can check. |
| [plain-writing](plain-writing/SKILL.md) | Writes or rewrites any text in plain language with the same rules. It keeps every fact, adds none, and draws a small diagram only when words are not enough. |

## Install

Claude Code loads personal skills from `~/.claude/skills/`. Link each skill folder there, so an edit in this repo applies right away:

```sh
ln -s "$PWD/explain-me" ~/.claude/skills/explain-me
```
