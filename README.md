# claude-roadmap-skill

A tiny Claude Code skill (`/roadmap`) that reads a project's tickets and draws a colour-coded roadmap graph: done, in progress, blocked, to-do, with dependency arrows.

A script reads your GitHub issues (via `gh`), groups them into stages and opens a one-screen page. It costs about 1k tokens per run because the script, not Claude, does the reading and drawing. Optional `.roadmap.json` in a repo sets custom stages.

## Install
```
mkdir -p ~/.claude/skills && cp -r roadmap ~/.claude/skills/
```
Then run `/roadmap` inside any project.
