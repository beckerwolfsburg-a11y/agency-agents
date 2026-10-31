# Aufgabe 2: Skript
Das Skript ist die Grundlage für alles danach: Claude ordnet später jeden Satz der Aufnahme einem Skriptsatz zu, und
Storyboard und Animationen hängen an diesen Sätzen.
## Format
`skript/skript.md`: `# Titel`, `## Kapitel`, darunter nur gesprochener Text in ganzen Sätzen. Keine Regieanweisungen im
Text (die gehören ins Storyboard). Danach `skript/saetze.json` erzeugen: `[{"nr": 1, "kapitel": "...", "text": "..."}]`.
## Drei Wege zum Skript (den User fragen, welcher)
1. **Vorbild-Video.** Der User gibt einen Link. Herunterladen (z. B. mit yt-dlp, falls installiert), mit
   `transkribieren.py` mitschreiben und in Teile zerlegen: Einstieg, einzelne Schritte, Schluss. Daraus einen Aufbau für das
   eigene Thema bauen – mit eigenen Inhalten, nichts abschreiben.
2. **Eigene Videos.** Der User gibt Transkripte von 2–3 eigenen Videos, die gut gelaufen sind. Daraus Ton, Satzlänge und
   Erklärweise ableiten und das neue Skript genauso schreiben.
3. **Feste Vorlage.** Eine Vorlage im Skill speichern (unten) und für jedes neue Thema füllen.
## Vorlage: Tutorial
1. Ergebnis zeigen (Hook: was am Ende möglich ist)
2. Was man braucht
3. Die Schritte der Reihe nach
4. Kurze Zusammenfassung und nächster Schritt
## Regeln
- Ganze Sätze, die man gut sprechen kann. Keine Satzfragmente.
- Eine Aussage pro Satz. Zahlen und Fakten nur, wenn sie belegt sind.
- Der User geht das Skript danach selbst durch und ändert alles, was nicht nach ihm klingt. Erst dann Storyboard.
