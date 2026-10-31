# Aufgabe 3: Storyboard
Bevor eine einzige Animation entsteht, plant Claude das ganze Video Satz für Satz.
## Ergebnis
`skript/storyboard.html` – eine Seite zum Durchscrollen: links der gesprochene Satz, rechts das Bild dazu (Beschreibung
und, wo hilfreich, eine kleine Skizze oder ein Standbild aus einer Testszene). Pro Zeile außerdem:
- **Bildart:** du im Bild · du mit Grafik daneben/dahinter · Vollbild-Grafik · Bildschirmaufnahme · Text
- **Ankerwort:** auf welchem Wort das Bild oder Element erscheint
- **Dauer** (aus der Sprechzeit geschätzt, nach der Aufnahme aus den echten Wortzeiten)
Daneben `skript/storyboard.json` mit denselben Angaben für den Bau.
## Zwei Regeln
1. Das Bild zeigt immer die **Kernaussage** des Satzes, nicht irgendein Nebenwort.
2. **Keine Bildart zweimal hintereinander**, damit das Video nicht eintönig wird.
## Ablauf
Der User geht die Seite in Ruhe durch und ändert, was nicht passt. Erst nach seinem Okay wird gebaut.
