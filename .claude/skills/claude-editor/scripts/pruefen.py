"""Prüft einen Schnitt gegen das Skript: fehlende Sätze, doppelte Stellen, zu lange Pausen.
Aufruf:  python pruefen.py <kontrolle.json> <skript.md> [--pause 0.25]
kontrolle.json = transkribieren.py auf das GESCHNITTENE Video angewendet.
Ausgabe: Liste der Funde mit Zeit im geschnittenen Video. Ziel: 0 fehlende Sätze, 0 doppelte Stellen, 0 lange Pausen."""
import argparse, difflib, json, re
ap = argparse.ArgumentParser()
ap.add_argument('kontrolle'); ap.add_argument('skript'); ap.add_argument('--pause', type=float, default=0.25)
a = ap.parse_args()
norm = lambda t: re.sub(r'[^\wäöüß]', '', t.lower())
W = [w for ab in json.load(open(a.kontrolle))['abschnitte'] for w in ab['woerter']]
gesagt = [norm(w['wort']) for w in W]
text = '\n'.join(z for z in open(a.skript, encoding='utf-8').read().splitlines() if z.strip() and not z.lstrip().startswith('#'))
saetze = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]
funde = 0
print('— Sätze aus dem Skript, die im Schnitt fehlen oder unvollständig sind —')
for nr, s in enumerate(saetze, 1):
    sw = [norm(x) for x in s.split() if norm(x)]
    m = difflib.SequenceMatcher(None, sw, gesagt, autojunk=False)
    treffer = sum(b.size for b in m.get_matching_blocks())
    if treffer / max(1, len(sw)) < 0.8:
        funde += 1; print(f'  Satz {nr} ({treffer}/{len(sw)} Wörter gefunden): {s[:90]}')
print('— Doppelte Stellen (dieselben 3 Wörter zweimal kurz hintereinander) —')
gesehen = {}
for i in range(len(gesagt) - 2):
    g = tuple(gesagt[i:i + 3])
    if g in gesehen and i - gesehen[g] <= 25 and i - gesehen[g] >= 3:
        funde += 1; print(f'  {W[i]["start"]:7.2f} s: „{" ".join(w["wort"] for w in W[i:i + 3])}“ (schon bei {W[gesehen[g]]["start"]:.2f} s)')
    gesehen[g] = i
# direkte Wortwiederholung („ich ich“), auch über Satzgrenzen
for i in range(1, len(gesagt)):
    if gesagt[i] and gesagt[i] == gesagt[i - 1] and len(gesagt[i]) > 2:
        funde += 1; print(f'  {W[i]["start"]:7.2f} s: Wort doppelt „{W[i]["wort"]}“')
print(f'— Pausen länger als {a.pause} s —')
for v, n in zip(W, W[1:]):
    if n['start'] - v['ende'] > a.pause:
        funde += 1; print(f'  {v["ende"]:7.2f} s: {n["start"] - v["ende"]:.2f} s zwischen „{v["wort"]}“ und „{n["wort"]}“')
print(f'\n{funde} Funde.' if funde else '\nKeine Funde – der Schnitt ist sauber.')
