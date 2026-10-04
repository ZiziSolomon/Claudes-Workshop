"""Same experiment for the standard genetic code: every single-base substitution
in every sense codon, classified as synonymous / missense / nonsense (stop)."""
from collections import Counter
B = "TCAG"
AA = "FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG"
CODE = {a + b + c: AA[16*i + 4*j + k] for i, a in enumerate(B) for j, b in enumerate(B) for k, c in enumerate(B)}
tab = Counter()
for cod, aa in CODE.items():
    if aa == "*": continue
    for pos in range(3):
        for nb in B:
            if nb == cod[pos]: continue
            new = CODE[cod[:pos] + nb + cod[pos+1:]]
            tab[(pos + 1, "synonymous" if new == aa else "stop" if new == "*" else "missense")] += 1
kinds = ["synonymous", "missense", "stop"]
for pos in (1, 2, 3):
    n = sum(tab[(pos, k)] for k in kinds)
    print(f"position {pos}: " + "  ".join(f"{k} {tab[(pos, k)]/n:.0%}" for k in kinds))
n = sum(tab.values())
print("all:        " + "  ".join(f"{k} {sum(tab[(p, k)] for p in (1,2,3))/n:.0%}" for k in kinds))
