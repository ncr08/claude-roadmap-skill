---
name: roadmap
description: Open a one-screen visual roadmap of the current project's GitHub issues (done, in progress, blocked, to do, grouped in stages). Use when the user runs /roadmap or asks "where am I at", "show the roadmap", or wants a visual project status.
---

# Roadmap

A script does all the work, so do NOT read tickets or write HTML yourself.

1. Run: `python3 -I ~/.claude/skills/roadmap/roadmap.py <repo dir>` (default: current directory).
   It fetches the issues, builds the page, opens it in the browser and prints a short summary.
2. If the output starts with `NO_TICKETS`, say so in one line and ask where the tickets live (a sibling repo?).
3. If the output has a `HINT` line: run the script with `--titles` (one line per ticket), then write
   `<repo>/.roadmap.json` once, grouping tickets into 4–6 stages by theme:
   `{"stages":[{"name":"Crawler MVP","desc":"one short line","ids":"1-19"}, ...]}`
   then run the script again. Never do this if there is no HINT.
4. Reply with at most 3 lines: totals, what's blocking the most work, what to pick up next.
   Use the script's summary; don't re-read the issues.
