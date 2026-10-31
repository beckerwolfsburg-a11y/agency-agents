# Regeln
Claude liest diese Datei vor jeder Aufgabe. Jede Regel gilt, bis der User sie ändert.
## Schnitt
- Von jedem Satz bleibt nur der **letzte vollständige Versuch**. Abgebrochene Wörter, Fehlstarts und Füllwörter fliegen raus –
  außer der User sagt sie absichtlich (z. B. ein „äh“ als Beispiel im Skript). Solche Stellen gehören in die Schnittliste.
- **Nie eine Endung oder einen Wortanfang abschneiden.** Leise Zischlaute (t, s, z, f) am Wortende gehören zum Wort.
  `schneiden.py` schützt sie; nach jedem Schnitt mit `pruefen.py` kontrollieren.
- Pausen zwischen Wörtern höchstens 0,25 s. Atem zwischen Sätzen fliegt raus.
- Bild und Ton werden nur bildgenau geschnitten (macht `schneiden.py`), damit die Lippen synchron bleiben.
- Eigene Ergänzungen des Users, die nicht im Skript stehen, bleiben drin, wenn sie zum Thema gehören. Im Zweifel fragen.
## Animationen
- Jedes Element erscheint genau auf dem Wort, zu dem es gehört (Wortzeiten aus `schnitt/schnitt_woerter.json`).
- Das Bild zeigt die **Kernaussage** des Satzes, nicht ein Nebenwort.
- Keine Bildart zweimal hintereinander (Wechsel zwischen dir im Bild, Vollbild-Grafik, Bildschirmaufnahme, Text).
- Text bleibt lange genug stehen, damit man ihn lesen kann (Faustregel: 0,3 s pro Wort, mindestens 1,5 s).
- Was gesprochen wird, nicht noch zusätzlich ausschreiben. Lieber zeigen als beschriften.
- Keine leere Sekunde: Jede Sekunde im Vollbild hat Inhalt.
- Text und Grafiken nie über das Gesicht legen.
- Logos immer in ihren echten Markenfarben. Echte Webseiten als ganzes Browserfenster zeigen, nicht abgeschnitten.
- Jedes Bild hängt nur von der Zeit ab (siehe Vorlage). Kein Zufall ohne festen Startwert, keine selbst laufenden CSS-Animationen.
- Nie zwei riesige Flächen (Hintergründe, Raster, Böden) gleichzeitig halbdurchsichtig überblenden – das überlastet den
  Grafikspeicher beim Rendern, und Teile fehlen dann zufällig im Bild. Eine Fläche nehmen und ihre Farbe ändern.
## Ton
- Musik liegt deutlich leiser unter der Stimme. Jedes Wort muss verständlich bleiben.
- Effekte nur auf wichtige Momente. Ein Effekt auf jeder Bewegung macht das Video unruhig.
- Endlautstärke −14 LUFS.
## Prüfen
- Vor jeder Vorschau: Kontaktbogen alle 0,5 s (Effekte im Intro: jedes Bild), `pruefen.py` ohne Funde, Bild- und Tonlänge gleich.
- Vor dem Zeigen das Ende jeder Datei anhören bzw. mitschreiben: Das letzte Wort muss vollständig sein.
- Export = genau das, was in der Vorschau abgenommen wurde. Nach der Abnahme nichts mehr ändern.
## Gelernt
<!-- Hier trägt Claude nach jeder Korrektur neue Regeln ein: Datum – Regel – Grund. -->
- 31.10.2026 – Nach den ersten Standbildern prüfen, ob die eigenen Schriften geladen sind (document.fonts, Status „loaded“). – Grund: Ein falscher Pfad in stil.css fiel beim Rendern nicht auf, Chrome nahm stillschweigend eine Ersatzschrift.
- 31.10.2026 – Renderer hier mit `--prozesse=1` starten. – Grund: Mit mehreren Tabs hängt die Bildaufnahme (puppeteer-core 23 mit neuerem Chrome).
