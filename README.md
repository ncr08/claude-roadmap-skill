# claude-roadmap-skill

A tiny Claude Code skill (`/roadmap`) that reads a project's tickets and draws a colour-coded roadmap graph: done, in progress, blocked, to-do, with dependency arrows.

Tickets come from GitHub issues (via `gh`) or local markdown files (`TODO.md`, `ROADMAP.md`, `tickets/`).

## Install
```
mkdir -p ~/.claude/skills && cp -r roadmap ~/.claude/skills/
```
Then run `/roadmap` inside any project.
