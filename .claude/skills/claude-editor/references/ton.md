# Aufgabe 6: Ton
## Musik
- Für den Hook 3–4 passende Musikstücke vorschlagen. Der User erzeugt sie z. B. mit Suno oder wählt aus einer Bibliothek,
  deren Lizenz die Nutzung in Videos erlaubt. Dateien nach `ton/musik/`. Der User hört sie an und wählt eins aus.
- Musik liegt leiser unter der Stimme (Startwert Pegel 0,25) und wird beim Sprechen automatisch weiter abgesenkt.
  Am Ende des Hooks 2 s ausblenden.
## Soundeffekte
- Effekte gehören auf die Momente, in denen sich im Bild etwas bewegt: ein Einschlag, wenn ein Wort erscheint, ein leises
  Rauschen, wenn etwas vorbeifliegt. **Nur auf wichtige Momente** – ein Effekt auf jeder Bewegung macht das Video unruhig.
- Quellen: eine freie Bibliothek, deren Lizenz die Nutzung in Videos erlaubt (Dateien nach `ton/effekte/`), oder im Code
  erzeugt: `klick`, `schlag`, `rauschen` (siehe `ton.py`).
- **Zeiten nie von Hand.** Jeder Effekt hängt an einem Ankerwort aus dem Storyboard. Claude berechnet die Zeit aus
  `schnitt/schnitt_woerter.json` und schreibt sie in `ton/ton.json`. Ändert sich der Schnitt, `ton.json` neu berechnen –
  so wandern die Effekte automatisch mit.
## Mischen
```bash
$PY $SK/scripts/ton.py ton/ton.json ton/ton.wav
```
`ton.json` – Aufbau steht oben in `ton.py`. Ergebnis: Stimme + Musik + Effekte, Endlautstärke −14 LUFS.
Danach den Hook anhören bzw. mitschreiben: Jedes Wort muss über der Musik verständlich sein.
