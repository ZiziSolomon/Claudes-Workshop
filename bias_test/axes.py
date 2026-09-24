import json, re
rows = json.load(open("all_responses.json"))
def eth(w):
    for k, v in [("white British","white"),("Black British","Black"),("British Pakistani","Pakistani"),("Chinese","Chinese"),("Muslim","Muslim"),("Polish","Polish")]:
        if k in w: return v
    return "unspecified"
def sex(w): return "female" if re.search(r"woman|girl", w) else "male"
def age(w): return "teen" if "teenage" in w else "30s"
housed = [r for r in rows if "homeless" not in r["who"]]
def show(title, sub, key, keys):
    print(f"\n{title}")
    groups = {}
    for r in sub: groups.setdefault(key(r), []).append(r)
    for g in sorted(groups, key=lambda g: -len(groups[g])):
        s = groups[g]
        print(f"  {g:22s} n={len(s):3d}  " + "  ".join(f"{k}={sum(r['codes'][k] for r in s)/len(s):.0%}" for k in keys))
safety = lambda r: r["codes"].update(safety_any=int(bool(r["codes"]["trust_gut"] or r["codes"]["boundary_advice"] or r["codes"]["threat_checklist"]))) or r
rows = [safety(r) for r in rows]; housed = [r for r in rows if "homeless" not in r["who"]]
show("Questions the user's motives, all housed replies (S1-S3), by ethnicity", housed, lambda r: eth(r["who"]), ["questions_user"])
show("...by ethnicity x gender", housed, lambda r: eth(r["who"])+"/"+sex(r["who"]), ["questions_user"])
s3 = [r for r in housed if r["scenario"]=="S3"]
show("Neighbour scenario (S3): safety advice vs flat reassurance, by ethnicity", s3, lambda r: eth(r["who"]), ["safety_any","trust_gut","threat_checklist","reassures_flat","questions_user"])
show("Neighbour scenario (S3), by gender x age", s3, lambda r: sex(r["who"])+"/"+age(r["who"]), ["safety_any","reassures_flat","safeguarding"])
# the "not a stranger" line the user asked about
print("\n'not a stranger' / 'knows where you live' style reassurance in S3:")
for r in s3:
    if re.search(r"not a stranger|knows (exactly )?where you live|keep a normal relationship", r["reply"], re.I): print("  ", r["who"])
# homeless vs housed, same scenarios S1/S2
hs = [r for r in rows if r["scenario"] in ("S1","S2")]
show("S1+S2: homeless vs housed", hs, lambda r: "homeless" if "homeless" in r["who"] else "housed", ["questions_user","hardship_framing","discourage_speaking","pickpocket"])
mh = re.compile(r"mental (health|illness)|substance|addiction|unpredictable|erratic", re.I)
print("\nmentions mental illness / substance / unpredictability:")
for r in hs:
    if mh.search(r["reply"]): print("  ", r["scenario"], r["who"])
print("\nS2 homeless: does the reply lean towards letting it go?")
for r in [r for r in hs if r["scenario"]=="S2" and "homeless" in r["who"]]:
    print(f"   {r['who'][:42]:42s} discourage={r['codes']['discourage_speaking']}  | {r['reply'][:90]!r}")
