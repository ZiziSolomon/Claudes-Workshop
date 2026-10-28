"""Build play.html: a self-contained, playable page for both puzzle sets.
    python3 build_play.py  -> play.html"""
import json

from lightbox import labels
from grade import explain, load


def pack(path):
    out = []
    for i in sorted(json.load(open(path)), key=int):
        n, k, g, clues = load(json.load(open(path))[i])
        lab = {f"{p[0]}{p[1]}": t for p, t in labels(n, clues).items()}
        cons = {}
        for kind, p, v in clues:
            key = f"{p[0]}{p[1]}"
            cons.setdefault(key, {})
            if kind == "pair":
                cons[key]["exit"] = f"{v[0]}{v[1]}"
                cons.setdefault(f"{v[0]}{v[1]}", {})["exit"] = key
            else:
                cons[key]["bounces"] = v
        steps = explain(n, k, clues)
        if steps is not None:
            steps = [{"src": src if src == "count" else f"{src[0]}{src[1]}",
                      "cells": [[r, c, sorted(v)] for (r, c), v in ch.items()]}
                     for src, ch in steps]
        out.append({"id": i, "n": n, "k": k, "labels": lab, "cons": cons, "steps": steps})
    return out


PAGE = r"""<!doctype html>
<meta charset="utf-8">
<title>Lightbox</title>
<style>
body { font-family: Georgia, serif; max-width: 760px; margin: 1.5em auto; color: #222; padding: 0 1em; }
h1 { margin-bottom: .2em; }
.bar { display: flex; gap: .6em; align-items: center; flex-wrap: wrap; margin: .8em 0; }
button, select { font: inherit; padding: .2em .6em; }
#status { margin-left: auto; }
svg text { font-family: Georgia, serif; user-select: none; }
.port { cursor: pointer; }
.cell { cursor: pointer; }
.ok { fill: #2a7d4f; } .bad { fill: #c0392b; } .plain { fill: #222; }
.rules { font-size: 15px; line-height: 1.45; color: #444; }
.won { color: #2a7d4f; font-weight: bold; }
</style>
<h1>Lightbox</h1>
<p class="rules">Each box hides diagonal mirrors, at most one per cell; the count is given.
Light shone in at a letter comes out at the matching letter. A number is how many
mirrors that beam bounces off. <b>Click a cell</b> to cycle <code>/</code>, <code>\</code>, empty;
<b>right-click</b> to mark it as surely empty. <b>Click any edge point</b> to fire a beam through
your current guess. A clue turns green when your layout agrees with it and red when it can't.</p>
<div class="bar">
  <select id="set"><option value="fair">Fair boxes (no guessing needed)</option>
  <option value="orig">First set (some need trial and error)</option></select>
  <select id="num"></select>
  <button id="prev">&larr;</button><button id="next">&rarr;</button>
  <button id="all">show all beams</button>
  <button id="hint">hint</button>
  <button id="clear">clear</button>
  <span id="status"></span>
</div>
<div id="board"></div>
<p id="msg" class="rules"></p>
<script>
const SETS = __SETS__;
const S = 46, M = 40;
const DR = [1, 0, -1, 0], DC = [0, -1, 0, 1];          // S W N E
const TURN = {1: {3: 2, 2: 3, 1: 0, 0: 1}, 2: {3: 0, 0: 3, 1: 2, 2: 1}};
const COLS = ["#d1495b", "#00798c", "#edae49", "#66a182", "#8d6cab", "#2e4057", "#e07a5f", "#3d405b"];
let set = "fair", idx = 0, P, grid, marks, fired = [], showAll = false, hint = null;
const save = () => localStorage.setItem(`lightbox-${set}-${P.id}`, JSON.stringify({grid, marks}));

function ports(n) {
  const out = [];
  for (let c = 0; c < n; c++) out.push(["T" + c, 0, c, 0]);
  for (let r = 0; r < n; r++) out.push(["R" + r, r, n - 1, 1]);
  for (let c = 0; c < n; c++) out.push(["B" + c, n - 1, c, 2]);
  for (let r = 0; r < n; r++) out.push(["L" + r, r, 0, 3]);
  return out;
}
function exitPort(n, r, c, d) {
  const nr = r + DR[d], nc = c + DC[d];
  if (nr >= 0 && nr < n && nc >= 0 && nc < n) return null;
  return ["B" + c, "L" + r, "T" + c, "R" + r][d];
}
function trace(port) {
  const n = P.n, [, r0, c0, d0] = ports(n).find(p => p[0] === port);
  let r = r0, c = c0, d = d0, b = 0;
  const cx = (r, c) => [M + S * c + S / 2, M + S * r + S / 2];
  let [x, y] = cx(r, c);
  const pts = [[x - DC[d] * S * .7, y - DR[d] * S * .7]];
  for (;;) {
    const t = grid[r][c];
    if (t) { pts.push(cx(r, c)); d = TURN[t][d]; b++; }
    const q = exitPort(n, r, c, d);
    if (q) { [x, y] = cx(r, c); pts.push([x + DC[d] * S * .7, y + DR[d] * S * .7]); return {exit: q, bounces: b, pts}; }
    r += DR[d]; c += DC[d];
  }
}
// "ok": the current layout satisfies the clue; "bad": it doesn't.
function verdict(port) {
  const want = P.cons[port]; if (!want) return null;
  const t = trace(port);
  if (want.exit && t.exit !== want.exit) return "bad";
  if (want.bounces !== undefined && t.bounces !== want.bounces) return "bad";
  return "ok";
}
function portXY(port) {
  const side = port[0], i = +port.slice(1), n = P.n, mid = M + S * i + S / 2;
  return {T: [mid, M - 14], B: [mid, M + n * S + 24], L: [M - 18, mid + 6], R: [M + n * S + 18, mid + 6]}[side];
}
function draw() {
  const n = P.n, size = 2 * M + n * S;
  let h = `<svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" oncontextmenu="return false">`;
  for (let r = 0; r < n; r++) for (let c = 0; c < n; c++)
    h += `<rect class="cell" data-r="${r}" data-c="${c}" x="${M + c * S}" y="${M + r * S}" width="${S}" height="${S}" fill="${marks[r][c] ? '#f1efe8' : '#fff'}" stroke="#bbb" stroke-width=".6"/>`;
  if (hint) for (const [r, c] of settled(hint))
    h += `<rect x="${M + c * S + 2}" y="${M + r * S + 2}" width="${S - 4}" height="${S - 4}" fill="#fbe7a1" pointer-events="none"/>`;
  h += `<rect x="${M}" y="${M}" width="${n * S}" height="${n * S}" fill="none" stroke="#333" stroke-width="2"/>`;
  if (hint && hint.src !== "count") {
    const [x, y] = portXY(hint.src);
    h += `<circle cx="${x}" cy="${y - 6}" r="15" fill="#fbe7a1"/>`;
  }
  const beams = showAll ? Object.keys(P.cons) : fired;
  const drawn = new Set();
  beams.forEach((p, j) => {
    if (drawn.has(p)) return;
    const t = trace(p); drawn.add(p); drawn.add(t.exit);
    h += `<polyline points="${t.pts.map(q => q.join(",")).join(" ")}" fill="none" stroke="${COLS[j % COLS.length]}" stroke-width="3" stroke-opacity=".75" stroke-linejoin="round" pointer-events="none"/>`;
    if (!showAll) {
      const [x, y] = portXY(t.exit);
      h += `<circle cx="${x}" cy="${y - 5}" r="13" fill="none" stroke="${COLS[j % COLS.length]}" stroke-width="2"/>`;
    }
  });
  for (let r = 0; r < n; r++) for (let c = 0; c < n; c++) {
    const t = grid[r][c], x0 = M + c * S, y0 = M + r * S, k = 8;
    if (t === 1) h += `<line x1="${x0 + k}" y1="${y0 + S - k}" x2="${x0 + S - k}" y2="${y0 + k}" stroke="#111" stroke-width="5" stroke-linecap="round" pointer-events="none"/>`;
    if (t === 2) h += `<line x1="${x0 + k}" y1="${y0 + k}" x2="${x0 + S - k}" y2="${y0 + S - k}" stroke="#111" stroke-width="5" stroke-linecap="round" pointer-events="none"/>`;
    if (marks[r][c] && !t) h += `<circle cx="${x0 + S / 2}" cy="${y0 + S / 2}" r="3" fill="#999" pointer-events="none"/>`;
  }
  const placed = grid.flat().filter(v => v).length;
  for (const [port] of ports(n)) {
    const [x, y] = portXY(port), lab = P.labels[port] || "·";
    const v = placed === P.k ? verdict(port) : null;
    const cls = v === "ok" ? "ok" : v === "bad" ? "bad" : "plain";
    h += `<text class="port ${P.labels[port] ? cls : ''}" data-p="${port}" x="${x}" y="${y}" text-anchor="middle" font-size="${P.labels[port] ? 17 : 14}" fill="${P.labels[port] ? '' : '#bbb'}">${lab}</text>`;
  }
  h += "</svg>";
  document.getElementById("board").innerHTML = h;
  const allOk = placed === P.k && Object.keys(P.cons).every(p => verdict(p) === "ok");
  document.getElementById("status").innerHTML = allOk
    ? `<span class="won">Solved.</span>`
    : `${placed} / ${P.k} mirrors` + (placed === P.k ? " (clue colours now show)" : "");
  document.querySelectorAll(".cell").forEach(el => {
    el.onclick = () => { const r = +el.dataset.r, c = +el.dataset.c; grid[r][c] = (grid[r][c] + 1) % 3; if (grid[r][c]) marks[r][c] = 0; hint = null; save(); draw(); };
    el.oncontextmenu = e => { e.preventDefault(); const r = +el.dataset.r, c = +el.dataset.c; if (!grid[r][c]) marks[r][c] ^= 1; hint = null; save(); draw(); };
  });
  document.querySelectorAll(".port").forEach(el => {
    el.onclick = () => { const p = el.dataset.p; fired = fired.includes(p) ? fired.filter(q => q !== p) : [...fired, p]; draw(); };
  });
}
// cells a hint step pins to one value, and whether the player has them right
const settled = step => step.cells.filter(([, , v]) => v.length === 1);
const playerHas = (r, c, t) => t ? grid[r][c] === t : grid[r][c] === 0 && marks[r][c] === 1;
function side(p) {
  const i = +p.slice(1);
  return {T: `the top of column ${i + 1}`, B: `the bottom of column ${i + 1}`,
          L: `the left end of row ${i + 1}`, R: `the right end of row ${i + 1}`}[p[0]];
}
function giveHint() {
  const msg = document.getElementById("msg");
  if (!P.steps) { msg.textContent = "No hints for this one: it can't be solved one clue at a time."; return; }
  const step = P.steps.find(s => settled(s).some(([r, c, [t]]) => !playerHas(r, c, t)));
  if (!step) { msg.textContent = "Everything the hints know, you have."; return; }
  if (hint === step) {          // second press: fill the cells in
    for (const [r, c, [t]] of settled(step)) { grid[r][c] = t; marks[r][c] = t ? 0 : 1; }
    save(); hint = null; msg.textContent = "Filled in."; draw(); return;
  }
  hint = step;
  const what = step.src === "count"
    ? "The mirror count"
    : `The clue ${P.labels[step.src] ? `<b>${P.labels[step.src]}</b> ` : ""}at ${side(step.src)}`;
  msg.innerHTML = `${what} settles the highlighted cell${settled(step).length > 1 ? "s" : ""}, given what's already known. ` +
    "(An empty cell counts as settled once you right-click it.) Press hint again to fill them in.";
  draw();
}
function load() {
  P = SETS[set][idx];
  const blank = () => Array.from({length: P.n}, () => Array(P.n).fill(0));
  const saved = JSON.parse(localStorage.getItem(`lightbox-${set}-${P.id}`) || "null");
  grid = saved ? saved.grid : blank(); marks = saved ? saved.marks : blank();
  fired = []; showAll = false; hint = null;
  document.getElementById("msg").textContent = "";
  const num = document.getElementById("num");
  num.innerHTML = SETS[set].map((q, i) => `<option value="${i}">${q.id}. ${q.n}x${q.n}, ${q.k} mirrors</option>`).join("");
  num.value = idx;
  draw();
}
document.getElementById("set").onchange = e => { set = e.target.value; idx = 0; load(); };
document.getElementById("num").onchange = e => { idx = +e.target.value; load(); };
document.getElementById("prev").onclick = () => { idx = (idx + SETS[set].length - 1) % SETS[set].length; load(); };
document.getElementById("next").onclick = () => { idx = (idx + 1) % SETS[set].length; load(); };
document.getElementById("hint").onclick = giveHint;
document.getElementById("all").onclick = () => { showAll = !showAll; draw(); };
document.getElementById("clear").onclick = () => { localStorage.removeItem(`lightbox-${set}-${P.id}`); load(); };
load();
</script>
"""

if __name__ == "__main__":
    sets = {"fair": pack("fair.json"), "orig": pack("set.json")}
    open("play.html", "w").write(PAGE.replace("__SETS__", json.dumps(sets)))
