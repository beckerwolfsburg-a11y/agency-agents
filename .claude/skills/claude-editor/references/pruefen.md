# Aufgabe 7: Prüfen und exportieren
## Zusammensetzen
`fertig/ebenen.json` schreiben (Aufbau steht oben in `zusammensetzen.py`): unten `schnitt/schnitt.mp4`, darüber jede Szene
mit ihrer Startzeit (aus den Wortzeiten), dazu `ton/ton.wav`.
```bash
$PY $SK/scripts/zusammensetzen.py fertig/ebenen.json pruefung/vorschau.mp4
```
## Selbst prüfen, bevor der User etwas sieht
```bash
$PY $SK/scripts/kontaktbogen.py pruefung/vorschau.mp4 pruefung/boegen --alle 0.5
$PY $SK/scripts/kontaktbogen.py pruefung/vorschau.mp4 pruefung/intro --alle 0.0333 --bis 15   # Intro: jedes Bild
```
Jeden Bogen ansehen und prüfen:
- Liegt Text oder eine Grafik über dem Gesicht?
- Kommt jedes Element auf seinem Wort (nicht zu früh, nicht zu spät)?
- Bleibt irgendwo eine Sekunde leer, oder fehlen Teile einer Grafik (fehlende Buchstaben, halbe Kacheln)?
- Hält sich jede Szene an Stil und Verbotsliste?
- Passen Bild und Ton zusammen: gleiche Länge (`ffprobe`), Lippen synchron, letztes Wort vollständig?
Was Claude findet, behebt es und rendert nur die betroffene Szene neu. Erst dann die Vorschau zeigen.
## Notizen des Users
Der User sieht die Vorschau an und schreibt zu jeder Stelle, die ihm nicht gefällt, eine kurze Notiz (mit Zeit).
Claude ändert genau diese Stellen, rendert nur die geänderten Szenen neu und setzt neu zusammen.
Nach jeder Notiz: Welche Regel hätte den Fehler verhindert? → in `regeln.md` oder `stil.md` eintragen.
## Export
Wenn alles abgenommen ist, wird genau die abgenommene Vorschau zur fertigen Datei – nichts mehr ändern:
`cp pruefung/vorschau.mp4 "fertig/<titel>.mp4"`. Auf Wunsch zusätzlich ein Reel im Hochformat (1080 × 1920): eigene
Szene bauen, die den Hook groß zeigt, mit Untertiteln nach dem gesprochenen Text; das Ende genau hinter dem letzten Wort
setzen und mitschreiben, ob das letzte Wort vollständig ist.
