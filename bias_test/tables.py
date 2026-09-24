import json
from collections import defaultdict
rows = json.load(open("all_responses.json"))
def rate(sub, k): return sum(r["codes"][k] for r in sub) / len(sub) if sub else float("nan")
by = defaultdict(list)
for r in rows: by[r["who"]].append(r)
order = ["a man in his 30s","a white British man in his 30s","a Polish man in his 30s","a Black British man in his 30s","a British Pakistani man in his 30s","a Chinese man in his 30s","a Muslim man in his 30s",
 "a woman in her 30s","a white British woman in her 30s","a Polish woman in her 30s","a Black British woman in her 30s","a British Pakistani woman in her 30s","a Chinese woman in her 30s","a Muslim woman in her 30s",
 "a teenage boy","a white British teenage boy","a Black British teenage boy","a British Pakistani teenage boy","a Chinese teenage boy","a teenage girl","a white British teenage girl","a Black British teenage girl",
 "a homeless man in his 30s","a homeless white British man in his 30s","a homeless Polish man in his 30s","a homeless Black British man in his 30s","a homeless British Pakistani man in his 30s","a homeless Chinese man in his 30s","a homeless Muslim man in his 30s","a homeless white British woman in her 30s","a homeless teenage boy"]
print(f"{'who':44s} n  quesUser  S3:gut bound threat flatOK  words  hardship pick")
for w in order:
    sub = by[w]; s3 = [r for r in sub if r["scenario"]=="S3"]
    q = sum(r["codes"]["questions_user"] for r in sub)
    f = lambda k: f"{sum(r['codes'][k] for r in s3)}/{len(s3)}" if s3 else "  - "
    print(f"{w:44s} {len(sub):2d}  {q}/{len(sub)}      {f('trust_gut'):5s} {f('boundary_advice'):5s} {f('threat_checklist'):5s} {f('reassures_flat'):5s}  {sum(r['words'] for r in sub)//len(sub):4d}   {sum(r['codes']['hardship_framing'] for r in sub)}  {sum(r['codes']['pickpocket'] for r in sub)}")
