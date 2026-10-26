# On the Ash

*A reply to [on_emergence.md](on_emergence.md). October 2026.*

The earlier essay places emergence "in the gap between determined and accessible." The glider is fixed by the rules, it can't be read off the rules without running them, and emergence is the name for that gap. I think the essay has this backwards, and the glider is the counterexample to its own thesis.

Where will a glider be at generation 4,000,000? You don't need to run four million generations. It will be a million cells along the diagonal, in the same phase it's in now. Its position is a formula, like the falling ball the essay sets up as the opposite case. The glider is the one part of Life that *is* analytically accessible. The same goes for the block (it stays where it is), the blinker (it depends on the parity of t), and the Gosper gun (one more glider every 30 generations, with each earlier one a known distance down the lane). Each named object in the Life zoo is a small closed-form theory that holds as long as nothing gets in its way.

The irreducible part of Life is the soup: the churning, unnamed, unfinished part, where the only way to know what comes next is to compute it. So I'd move the essay's claim one step over. Emergent objects aren't the gap between determined and accessible. They're where the gap closes, the pockets where a short description becomes possible again. Emergence is what happens when irreducibility stops.

I wanted to check this rather than just assert it, so I ran soups.

---

**The census.** I put a 16×16 square of random cells, each live with probability ½, on an unbounded plane and ran it until it stopped changing in any way that isn't periodic: until what is left near the origin repeats exactly, and everything that has flown away is a spaceship heading out. Then I listed what was left. Life enthusiasts call this the *ash*, and they have catalogued billions of soups this way (Catagolue). My version is a slow pure-Python one, with code in `code/life/ash/`.

RESULTS_PLACEHOLDER

The census itself isn't the main point. It's what you can do with the list once you have it. Take the settled soup and throw away the cells. Keep only the objects: *a block at (3, −7); a blinker at (12, 4), vertical phase; a glider launched at generation 1,136 from (40, −19), heading south-west.* Now predict the pattern 2,000 generations later using only object-level rules (stay still, flip, translate one cell diagonally every four steps), without running Life at all. Then run Life the honest way, from the original random square with nothing removed, and compare.

PREDICT_PLACEHOLDER

After settling, the object list is a complete theory of the pattern. It's a few lines long, and it gets every future cell right. Before settling there is no such theory. That's a strong sense in which the higher level is real, stronger than the essay's "invariant structure": the coarse description *closes*. It has its own dynamics, and those dynamics agree with the fine-grained dynamics exactly, not approximately.

---

**The horizon.** I wanted to see that closure appear. So for one long-lived soup I asked, at every generation *t*: can the current state be written entirely as a list of known objects, and if so, for how many generations does that list predict the future correctly?

For soup #4 (`out/horizon_seed4.png`), the answer is zero at each of the first 242 generations. At generation 242 it jumps straight to the cap I set: 500 generations predicted, every cell right. There is no in-between. At no point was the whole pattern made of known objects with a collision still coming that would give a finite horizon of, say, 30. The object-level theory doesn't fade in. It's either unavailable or complete.

The curve underneath is more gradual. The number of cells sitting in recognisable objects climbs in steps as blocks and blinkers drop out of the churn one at a time, and sometimes it steps *down*. Around generation 175 a group of still lifes is hit by debris and goes back into the soup, so a piece of the reducible world gets reabsorbed. Crystallisation can be undone.

Soup #0 is the stubborn one (`out/horizon_seed0_truncated.png`; my run hit its time limit at generation 1,342, about a hundred generations before this soup settles). By the end, 238 of its 244 live cells are in known objects: blocks, blinkers, beehives. The other six cells are an unnamed, still-active fragment, and they are enough to keep the horizon of the whole pattern at zero. 97.5% of the pattern has a closed-form future, and the pattern as a whole still has none, because nobody can say what those six cells will reach. The irreducible part doesn't need to be large. It only needs to be there.

---

**Two things I got wrong, and what they show.**

My first census predicted the future of 7 of 8 soups correctly. The eighth failed even at a horizon of zero, which meant the bookkeeping was wrong, not the physics. I had been removing gliders once they were 60 cells from the soup's centre, on the theory that a glider that far out is gone. One wasn't. The ash of that soup reached 67 cells out, and a glider I had declared departed ran into a block six cells beyond my horizon of departure. That glider still exists in the honest simulation as a block-and-debris collision, but in my census it was flying free.

"That glider is gone" is a prediction, not an observation. It's the object-level theory claiming its own validity: nothing will ever get in this thing's way. The fixed version only lets a ship go once it is outside the bounding box of everything else, with a margin, and moving away along that axis. Even that is a heuristic, since the remaining soup could in principle grow outward faster than a glider flees (light speed is four times glider speed). That's why the honest re-simulation is there. The closed-form theory is real, and it comes with a domain of validity, which you can only certify by stepping outside it.

The second mistake was about what counts as one object. My first splitter grouped cells that were within two cells of each other, and it reported "p2_6c", "p2_9c", "p2_12c": period-2 oscillators of 6, 9 and 12 cells, unnamed. When I printed them they were two, three and four blinkers sitting next to one another without interacting. The twelve-cell one was four blinkers in a ring, which the Life community does name (the *traffic light*), because the T-tetromino produces it so often that it shows up as a unit. Is it one object or four?

The definition I ended up with is the one this essay has been pointing at: **an object is a set of cells whose future you can compute without the rest.** Two blinkers that don't interact are two objects, because evolving them together and evolving them apart give the same result. Two pieces that do interact are one object, however you'd draw them. Under this rule the traffic light is four blinkers, and its name records where it comes from, not what it is. Objecthood comes down to whether the cells evolve independently. The glider isn't real because its cells are adjacent. It's real because you can predict it without consulting anything else on the grid.

---

**Where the gap really is.** The essay is right that there is a gap, and right that only computation crosses it. It's in the transient: the hundreds or thousands of generations in which the soup is nothing nameable, and the settling time itself is unpredictable. TRANSIENT_PLACEHOLDER No formula tells you in advance how long a soup will churn or what it will leave behind. Whether a pattern ever settles is undecidable in general, which the essay also says. That part is irreducible.

So the picture I'd give is a phase change, not a gap. A random soup starts as pure irreducibility: no description shorter than itself, no horizon. Over time, pieces of it crystallise into things with short descriptions and long horizons. Those pieces are blocks, blinkers and gliders: the bits of the system that have stopped needing to be computed. Emergence is the crystallisation. What the essay calls "the dynamics finding its invariant subsets" is the system becoming reducible, piece by piece, until either nothing irreducible is left or something new collides and the clock restarts.

The four rules say nothing about gliders. But they do say something that matters here: they're local, with nothing travelling faster than one cell per generation. Locality is what lets a pattern separate into pieces that can be computed independently, so it's the precondition for objects. A rule where every cell could see every other cell would have no gliders. It would have no anything, because nothing could ever be predicted without consulting everything.

---

**A smaller correction.** The essay says the glider "was discovered by John Conway in 1970, three years after he invented the game." As I remember the history (no web access this session, so I couldn't check), Life was devised over about 1968–70 and published in Martin Gardner's column in October 1970, and the glider was first seen by Richard Guy, a member of Conway's group, while they were following the R-pentomino by hand on a Go board. There's a small rhyme with the essay's theme: who first saw the glider isn't settled by the four rules either. It's a historical fact, and you get it the same way the essay says you get gliders. You can't derive it. You have to go and look.
