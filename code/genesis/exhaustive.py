"""Every single-base substitution of the Genesis gene (361 x 3), classified by
what the decoded sentence becomes, broken down by which symbol was hit."""
from collections import Counter
from genesis import S, encode, decode
dna = encode(S)
NAME = {"T": "dash", "C": "dot", "G": "letter gap", "A": "word gap"}
tab = Counter()
for i, b in enumerate(dna):
    for nb in "ACGT":
        if nb == b: continue
        t = decode(dna[:i] + nb + dna[i+1:])
        kind = "same" if t == S else ("garbled(?)" if "?" in t else "valid letters")
        tab[(NAME[b], NAME[nb], kind)] += 1
kinds = ["same", "valid letters", "garbled(?)"]
print(f"{'hit':<11}{'became':<12}" + "".join(f"{k:>15}" for k in kinds))
for src in NAME.values():
    for dst in NAME.values():
        if src == dst: continue
        row = [tab[(src, dst, k)] for k in kinds]
        if sum(row): print(f"{src:<11}{dst:<12}" + "".join(f"{x:>15}" for x in row))
tot = Counter(); [tot.update({k: v}) for (_, _, k), v in tab.items()]
print({k: f"{tot[k]/sum(tot.values()):.0%}" for k in kinds})
