# Aufgabe 4: Schnitt
Der User nimmt sich ganz normal auf und spricht dabei viele Sätze mehrmals. Claude macht daraus eine saubere Fassung:
von jedem Satz der letzte vollständige Versuch, keine Fehlstarts, keine langen Pausen.
`$SK = ~/.claude/skills/claude-editor` · `$PY = $SK/.venv/bin/python` · alle Befehle im Ordner des Videos.
## 1. Aufnahme ablegen
Datei(en) nach `aufnahme/`. Mehrere Dateien zuerst zu einer zusammenfügen:
`ffmpeg -f concat -safe 0 -i liste.txt -c copy aufnahme/aufnahme.mp4` (liste.txt: `file 'teil1.mp4'` je Zeile).
## 2. Mitschreiben
```bash
$PY $SK/scripts/transkribieren.py aufnahme/aufnahme.mp4 schnitt/woerter.json --prompt "Fachwörter aus dem Skript, durch Komma getrennt"
```
Die Aufnahme wird an den Pausen in kurze Abschnitte zerlegt, jeder wird einzeln mitgeschrieben. So bleiben Wiederholungen
und abgebrochene Versuche sichtbar. Atem und Geräusche werden übersprungen.
## 3. Versuche den Skriptsätzen zuordnen → `schnitt/schnitt.json`
Abschnitte aus `woerter.json` neben `skript/saetze.json` legen. Für jeden Skriptsatz alle Versuche finden und den
**letzten vollständigen** nehmen (alle Wörter des Satzes in der richtigen Reihenfolge; kleine Abweichungen beim Sprechen
sind in Ordnung, das Gesagte zählt). Setzt der User mitten im Satz neu an, beginnt das Stück beim neuen Ansatz.
```json
{"stuecke": [{"von": 12.31, "bis": 18.02, "satz": 1}, {"von": 25.40, "bis": 31.77, "satz": 2}]}
```
`von` = Start des ersten Worts, `bis` = Ende des letzten Worts (Zeiten aus woerter.json). Reihenfolge = Reihenfolge im Video.
Eigene Sätze des Users, die nicht im Skript stehen, aber zum Thema gehören, bleiben drin. Sätze an Claude („nochmal“, „warte“)
und reine Geräusche fliegen raus. Daneben `schnitt/schnitt_liste.md` schreiben: je Satz der gewählte Versuch und wie viele
Versuche es gab – damit der User nachvollziehen kann, was passiert ist.
## 4. Schneiden
```bash
$PY $SK/scripts/schneiden.py aufnahme/aufnahme.mp4 schnitt/schnitt.json schnitt/schnitt.mp4 --woerter schnitt/woerter.json
```
Das Skript legt die Ränder an den echten Wortrand (auch leise Endungen wie „t“ oder „s“), kürzt Pausen über 0,25 s auf
0,12 s und schneidet Bild und Ton bildgenau. Ergebnis: `schnitt.mp4`, `schnitt_zeiten.json` (alte → neue Zeit) und
`schnitt_woerter.json` (jedes Wort mit seiner Zeit im geschnittenen Video – die Grundlage für Animationen und Effekte).
## 5. Selbst prüfen (Pflicht, bevor der User etwas sieht)
```bash
$PY $SK/scripts/transkribieren.py schnitt/schnitt.mp4 schnitt/kontrolle.json --prompt "…"
$PY $SK/scripts/pruefen.py schnitt/kontrolle.json skript/skript.md
```
Ziel: keine fehlenden Sätze, keine doppelten Stellen, keine Pause über 0,25 s. Jeden Fund ansehen und in `schnitt.json`
beheben, dann Schritt 4 und 5 wiederholen. Zusätzlich die Übergänge an 3–4 Stellen anhören bzw. dort einzeln mitschreiben:
Kein Wort darf angeschnitten sein. Hinweis: Die Spracherkennung schreibt Wiederholungen manchmal weg – Stellen, an denen der
User sich nur um eine Silbe versprochen hat, deshalb im Zweifel einzeln mitschreiben (`transkribieren.py` auf einen kurzen
Ausschnitt, den man mit `ffmpeg -ss <start> -t <dauer>` herausschneidet).
## 6. Änderungen
Der User nennt ein Wort oder einen Satz, der raus soll oder anders geschnitten werden soll → `schnitt.json` anpassen,
Schritt 4 und 5 wiederholen. Danach müssen alle Zeiten neu berechnet werden, die von `schnitt_woerter.json` abhängen
(Animationen, Effekte) – deshalb Zeiten nie von Hand eintragen, sondern immer aus den Wortzeiten ableiten.
