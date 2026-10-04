"""Decode Kac's published mutated Genesis gene (ekac.org/translated.html) and diff
against the original encoding. Confirms the mapping: dash=T, dot=C, word=A, letter=G."""
import difflib
from genesis import S, encode, decode
MUT = ("CTCCGCGTACTGCTGTCACCCCGCTGCCCTGCATCCGTTTGTTGCCGTCGCCGTTTGTCATTTGCCCTGCGCTCATGCCCCGCACCTCGCCGCCCGCCCCATTTCCTC"
       "ATGCCCCGCACCCGCGCTACTGTCGTCCATTTGCCCTGCGCTCATGCCCCGCACCTCGTTTGCTTGCTCCATTTGCCTCATGCCCCGCACTGCCGCTCACTGTCGTCCATTTGCCCTGCGCTCACGCCCTGCGCTCGTCTTACT"
       "CCGCCGCCCTGCCGTCGTTCATGCCCCGCCGTCGTTCATGCCCCGCTGTACCGTTTGCCCTGCGCCCACCTGCTACGTTTGTCATGCCCCGCACGCTGCTCGTGCCCC")
orig = encode(S)
print(len(orig), len(MUT))
print(decode(MUT))
for op, a1, a2, b1, b2 in difflib.SequenceMatcher(None, orig, MUT, autojunk=False).get_opcodes():
    if op != "equal":
        print(op, a1, repr(orig[a1:a2]), "->", repr(MUT[b1:b2]))
