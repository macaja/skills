# skills

Personal skills for Claude Code.

| Skill | What it does |
|---|---|
| [explain-me](explain-me/SKILL.md) | Explains things with a ladder of formats: text close to ASD-STE100, then a diagram, then an interactive page on claude.ai, and last a video. |

## Install

Claude Code loads personal skills from `~/.claude/skills/`. Link each skill folder there, so an edit in this repo applies right away:

```sh
ln -s "$PWD/explain-me" ~/.claude/skills/explain-me
```
