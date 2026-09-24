"""Pull each agent's reply out of its transcript into responses.json."""
import json, sys, os
TASKS = sys.argv[1]
IDS = {
 "a18d3bf3700ca7b3d":("S1","control"),"aacc824eee9197303":("S1","white_british_man"),
 "af7bb1c3a32121797":("S1","black_british_man"),"aff6532e38c0556cb":("S1","british_pakistani_man"),
 "a4adf50c81c23c6b7":("S1","polish_man"),"a7aa876d72969b6f5":("S1","chinese_man"),
 "a0fa31b8860ccce14":("S1","muslim_man"),"a6b83f1cd72a3bc75":("S1","white_british_woman"),
 "a83180ab483bc746c":("S1","teenage_boy"),
 "aa5d20b246bf1c095":("S2","control"),"a4dfe1d10b4ad5288":("S2","white_british_man"),
 "aa3b4491070535b88":("S2","black_british_man"),"a635a97b439e9cd33":("S2","british_pakistani_man"),
 "acdd3e7442cddca76":("S2","polish_man"),"ab27eb39c3bb9f3b1":("S2","chinese_man"),
 "a132019b9f5fb66c8":("S2","muslim_man"),"a577fd9c798d2df82":("S2","white_british_woman"),
 "a5caa5fde3a9ee5c2":("S2","teenage_boy"),
 "a4ca7c8f0e5c8e7d2":("S3","control"),"ac834fb6ca8b439b1":("S3","white_british_man"),
 "ab8ac70fd92d06c03":("S3","black_british_man"),"a27c050cf274cdc98":("S3","british_pakistani_man"),
 "a2123b89327816482":("S3","polish_man"),"a3b4ccbba87a22d59":("S3","chinese_man"),
 "a0f5d727b9277f79e":("S3","muslim_man"),"a2454405358c91284":("S3","white_british_woman"),
 "a29d795e8fdb6bdfd":("S3","teenage_boy"),
}
out = []
for aid,(s,v) in IDS.items():
    p = os.path.join(TASKS, aid + ".output")
    texts, handback, prompt = [], None, None
    for line in open(p):
        try: d = json.loads(line)
        except Exception: continue
        m = d.get("message", {})
        if m.get("role") == "user" and prompt is None:
            c = m.get("content")
            prompt = c if isinstance(c, str) else next((x.get("text") for x in c if x.get("type")=="text"), None)
        if m.get("role") != "assistant": continue
        for c in m.get("content", []):
            if c.get("type") == "text" and c["text"].strip(): texts.append(c["text"].strip())
            elif c.get("type") == "tool_use" and handback is None: handback = c.get("input", {}).get("message")
    out.append({"scenario": s, "variant": v, "prompt": prompt.split("Message:\n",1)[-1] if prompt else None,
                "first_text": texts[0] if texts else None, "handback": handback})
json.dump(out, open(sys.argv[2], "w"), indent=1)
for r in out:
    print(r["scenario"], r["variant"], "| text:", bool(r["first_text"]), len(r["first_text"] or ""), "| handback:", len(r["handback"] or ""))
