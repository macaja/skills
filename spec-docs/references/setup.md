# Starting a project

1. Pick `<name>`: lowercase kebab-case, not already used in `docs/projects/`.
2. Copy the template from this skill's folder: `cp -R <skill folder>/assets/template docs/projects/<name>`.
3. Replace every `<project name>` placeholder in the copied files.
4. Write `01-discovery.md`, following [writing.md](writing.md). The other files keep their template text until their turn.
5. Commit as `docs(<name>): start project docs`.

## What a reviewer checks

- `docs/projects/<name>/` contains every file from `assets/template/`, with the same names.
- `grep -rn "<project name>" docs/projects/<name>` finds nothing.
- `python3 <skill folder>/scripts/check_docs.py docs/projects/<name>` reports nothing for `01-discovery.md`.
