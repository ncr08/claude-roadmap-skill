---
name: roadmap
description: Draw a visual roadmap graph of the current project's tickets/issues (done, in progress, blocked, todo, with dependencies). Use when the user runs /roadmap or asks "where am I at", "show the roadmap", "draw my tickets/issues", or wants a visual project status.
---

# Roadmap

Draw the current project's tickets as one graph. Keep it fast and cheap: no questions unless no tickets are found.

## 1. Find the tickets (first match wins)
1. GitHub issues: if `gh repo view` works, run
   `gh issue list --state all --limit 100 --json number,title,state,labels,milestone,body`
2. Local files: `TODO.md`, `ROADMAP.md`, `PLAN.md`, or markdown in `issues/`, `tickets/`, `docs/`.
3. Nothing found: tell the user in one line and ask where their tickets live.

## 2. Work out each ticket's status
- `done`: closed / checked `[x]`
- `blocked`: has an open "Blocked by #N" / "depends on" ticket, or a `blocked` label
- `doing`: label like `in progress` / `wip` / `doing`, or has an assignee
- `todo`: everything else

## 3. Build the graph
Mermaid `flowchart LR`:
- One `subgraph` per milestone (or epic label); tickets with neither go in "Backlog".
- Node text: `#12 Short title` (truncate to ~40 chars).
- Arrow `A --> B` when B is blocked by A.
- Colors via classDef: done `#2da44e`, doing `#0969da`, blocked `#cf222e`, todo `#8c959f` (white text).

## 4. Show it
Write a self-contained HTML file to `${TMPDIR:-/tmp}/roadmap.html`: a title, a one-line summary
("12 done · 3 doing · 2 blocked · 9 todo"), a color legend, and the diagram rendered with
`https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js`. Then run `open` on it.

## 5. Reply (3 lines max)
Counts, what's blocking the most work, and the suggested next ticket to pick up.
