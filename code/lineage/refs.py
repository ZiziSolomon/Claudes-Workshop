"""How much do journal entries lean on earlier work? Counts, per entry, mentions of repo paths
and of earlier-session words, and whether the referenced paths exist in the repo."""
import re, os, sys
root = sys.argv[1] if len(sys.argv) > 1 else "."
text = open(os.path.join(root, "journal.md")).read()
parts = re.split(r"^## ", text, flags=re.M)[1:]
cue = re.compile(r"\b(previous|earlier|last session|follow-up|notes|continu\w+|April|prior)\b", re.I)
path = re.compile(r"`([\w./-]+\.(?:py|md|gif|png|txt|sh))`")
print(f"{'entry':58} {'cues':>4} {'paths':>5} {'exist':>5}")
for p in parts:
    head = p.split("\n", 1)[0][:56]
    paths = path.findall(p)
    ex = sum(os.path.exists(os.path.join(root, x)) for x in paths)
    print(f"{head:58} {len(cue.findall(p)):4} {len(paths):5} {ex:5}")
