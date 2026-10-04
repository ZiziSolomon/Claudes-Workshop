"""Gujarati possessive particle agrees with the gender of the thing possessed:
   ni (feminine), no (masculine), nu (neuter).  'Luv Ni Love Storys' works
   because story = vaarta/kahani (feminine).  Titles: <owner> <particle> <thing>.
   Gender below is for the Gujarati word each English noun is usually swapped for."""
import random
THINGS = {  # english word as used in code-mixed speech: (gender, gujarati)
    "Story": ("f", "varta"), "Love": ("m", "prem"), "Chai": ("f", "chaa"),
    "Wedding": ("n", "lagna"), "Mobile": ("m", "mobile"), "Exam": ("f", "pariksha"),
    "Heart": ("n", "dil"), "Scooter": ("n", "scooter"), "Time": ("m", "samay"),
    "Plan": ("m", "plan"), "Mistake": ("f", "bhool"), "Dream": ("n", "sapnu"),
}
OWNERS = ["Surat", "Papa", "Mummy", "Whatsapp", "Monsoon", "Neighbour", "Wifi", "Ahmedabad"]
P = {"f": "ni", "m": "no", "n": "nu"}
def title(rng=random):
    t = rng.choice(list(THINGS)); g, _ = THINGS[t]
    return f"{rng.choice(OWNERS)} {P[g].capitalize()} {t}"
if __name__ == "__main__":
    random.seed(2020)
    for _ in range(12): print(title())
