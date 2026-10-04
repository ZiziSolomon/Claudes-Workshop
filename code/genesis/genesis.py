"""Toy re-run of Eduardo Kac's *Genesis* (1999): a Bible sentence -> Morse -> DNA,
then "UV" point mutations, then decode back. Mapping is from memory, unverified:
dash=T, dot=C, letter gap=G, word gap=A. Kac's page only says "a conversion
principle specially developed for this work"."""
import random, sys
M = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", ".- -... -.-. -.. . ..-. --. .... .. .--- -.- .-.. -- -. --- .--. --.- .-. ... - ..- ...- .-- -..- -.-- --..".split()))
R = {v: k for k, v in M.items()}
S = "LET MAN HAVE DOMINION OVER THE FISH OF THE SEA AND OVER THE FOWL OF THE AIR AND OVER EVERY LIVING THING THAT MOVES UPON THE EARTH"

def encode(s):
    return "A".join("G".join(M[c].replace("-", "T").replace(".", "C") for c in w) for w in s.split())

def decode(dna):
    out = []
    for w in dna.split("A"):
        out.append("".join(R.get(l.replace("T", "-").replace("C", "."), "?") for l in w.split("G") if l))
    return " ".join(out)

def uv(dna, n, rng):
    d = list(dna)
    for i in rng.sample(range(len(d)), n):
        d[i] = rng.choice([b for b in "ACGT" if b != d[i]])
    return "".join(d)

if __name__ == "__main__":
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 2001)
    dna = encode(S)
    print(len(dna), "bases")
    assert decode(dna) == S
    for n in (1, 3, 10, 30):
        print(f"{n:>3} hits: {decode(uv(dna, n, rng))}")
