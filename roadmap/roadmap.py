#!/usr/bin/env python3
"""Build a one-screen roadmap page from a repo's GitHub issues. Usage: roadmap.py [repo_dir] [--titles]

Reads issues with gh, groups them into stages, writes $TMPDIR/roadmap.html, opens it and prints a short summary.
Stages come from <repo>/.roadmap.json if present: {"stages":[{"name":"..","desc":"..","ids":"1-19,21,22"}]}
Otherwise: "Part of #N" parents, then milestones, then phase-* labels, then "Other".
"""
import json, os, re, subprocess, sys, html, tempfile

args = [a for a in sys.argv[1:] if not a.startswith("--")]
repo = os.path.abspath(args[0]) if args else os.getcwd()
run = lambda *c: subprocess.run(c, cwd=repo, capture_output=True, text=True)

r = run("gh", "issue", "list", "--state", "all", "--limit", "300", "--json",
        "number,title,state,labels,milestone,assignees,body")
if r.returncode or not json.loads(r.stdout or "[]"):
    print("NO_TICKETS: no GitHub issues found in " + repo); sys.exit(0)
issues = sorted(json.loads(r.stdout), key=lambda i: i["number"])
by = {i["number"]: i for i in issues}

if "--titles" in sys.argv:
    for i in issues: print(i["number"], i["state"][0], i["title"][:70])
    sys.exit(0)

DOING = {"in progress", "wip", "doing", "agent-in-batch"}
YOU = {"ready-for-human"}
parent, blockers = {}, {}
for i in issues:
    b = i["body"] or ""
    m = re.search(r"(?:Part of|Parent:?) #(\d+)", b)
    if m: parent[i["number"]] = int(m[1])
    m = re.search(r"(?:Blocked by|Depends on)\s*:?\s*(.*?)(?:\n\s*\n|\Z)", b, re.S | re.I)
    blockers[i["number"]] = [int(x) for x in re.findall(r"#(\d+)", m[1])] if m else []

def status(i):
    n, labels = i["number"], {l["name"].lower() for l in i["labels"]}
    if i["state"] == "CLOSED": return "done"
    if any(by.get(b, {}).get("state") == "OPEN" for b in blockers[n]): return "blocked"
    if labels & YOU: return "you"
    if labels & DOING or i["assignees"]: return "doing"
    return "todo"
st = {i["number"]: status(i) for i in issues}

def parse_ids(s):
    out = []
    for part in str(s).split(","):
        a, _, b = part.strip().partition("-")
        out += range(int(a), int(b or a) + 1)
    return [n for n in out if n in by]

stages, cfg = [], os.path.join(repo, ".roadmap.json")
if os.path.exists(cfg):
    for s in json.load(open(cfg))["stages"]:
        stages.append((s["name"], s.get("desc", ""), parse_ids(s["ids"])))
else:
    groups = {}
    for i in issues:
        n = i["number"]
        key = parent.get(n) or (n if n in parent.values() else None)
        if key: name = "#%d %s" % (key, by[key]["title"][:40]) if key in by else "Group #%d" % key
        elif i["milestone"]: name = i["milestone"]["title"]
        else:
            ph = [l["name"] for l in i["labels"] if l["name"].lower().startswith("phase")]
            name = ph[0] if ph else "Other"
        groups.setdefault(name, []).append(n)
    stages = [(k, "", v) for k, v in groups.items()]
    stages.sort(key=lambda s: (s[0] == "Other", min(s[2])))
    if len(groups.get("Other", [])) > 0.6 * len(issues):
        print("HINT: most tickets are ungrouped. Run with --titles, then write .roadmap.json (stages with ids ranges) once.")

E = html.escape
total, done = len(issues), sum(v == "done" for v in st.values())
cards = []
for k, (name, desc, ids) in enumerate(stages, 1):
    d = sum(st[n] == "done" for n in ids)
    chips = "".join('<span class="chip %s" title="#%d %s">%d</span>' % (st[n], n, E(by[n]["title"][:80]), n) for n in ids)
    deps = [" ".join("#%d" % b for b in blockers[n]) + " → #%d" % n for n in ids if blockers[n] and st[n] != "done"]
    cards.append('<section class="stage"><div class="step">Stage %d</div><h2>%s</h2><p class="desc">%s</p>'
                 '<div class="frac">%d of %d done</div><div class="mini"><i style="width:%d%%"></i></div>'
                 '<div class="chips">%s</div>%s</section>'
                 % (k, E(name), E(desc), d, len(ids), 100 * d // max(len(ids), 1), chips,
                    '<p class="dep">%s</p>' % E("; ".join(deps)) if deps else ""))

page = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "template.html")).read()
page = (page.replace("{{TITLE}}", E(os.path.basename(repo))).replace("{{DONE}}", str(done))
            .replace("{{TOTAL}}", str(total)).replace("{{STAGES}}", "".join(cards)))
out = os.path.join(os.environ.get("TMPDIR", tempfile.gettempdir()), "roadmap.html")
open(out, "w").write(page)
subprocess.run(["open", out])

left = [n for n in by if st[n] != "done"]
print("%s: %d of %d done. Opened %s" % (os.path.basename(repo), done, total, out))
for n in left: print("  %s #%d %s%s" % (st[n].upper(), n, by[n]["title"][:60],
      (" (waiting on " + ", ".join("#%d" % b for b in blockers[n]) + ")") if st[n] == "blocked" else ""))
