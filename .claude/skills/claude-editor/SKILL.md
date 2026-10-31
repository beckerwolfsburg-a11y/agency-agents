---
name: claude-editor
description: Editiert YouTube-Videos komplett mit Claude Code – Stil beibringen, Skript, Storyboard, Schnitt der Aufnahme (letzter Versuch je Satz, Pausen raus), Animationen als HTML gerendert, Musik und Soundeffekte, Prüfung und Export. Nutze diesen Skill bei "/claude-editor", "neues Video", "Video editieren", "schneide meine Aufnahme", "Storyboard", "Animationen bauen", "Stil einrichten", "Video fertig machen".
---
# Claude Editor
Ein System, mit dem Claude aus einer Aufnahme ein fertig editiertes Video macht. Der Mensch entscheidet (Thema, Stil,
Geschmack, Abnahme), Claude erledigt die Arbeit dazwischen.
**Vor jeder Aufgabe lesen:** `references/regeln.md` (feste Regeln und alles, was der Skill bisher gelernt hat) und
`references/stil.md` (der Stil des Users). Danach die Datei der jeweiligen Phase.
## Pfade
- Skill: `~/.claude/skills/claude-editor` (im Folgenden `$SK`)
- Python: `$SK/.venv/bin/python` · Renderer: `node $SK/scripts/render.mjs`
- Projektordner: der Ordner, der in Claude Code geöffnet ist. Jedes Video bekommt `videos/<JJJJ-MM-TT>-<kurzname>/` mit
  `skript/ aufnahme/ material/ schnitt/ animationen/ ton/ pruefung/ fertig/`. Anlegen, wenn er fehlt.
## Die sieben Aufgaben
| # | Aufgabe | Datei | Ergebnis | Freigabe durch den User |
|---|---|---|---|---|
| 1 | Stil beibringen (einmalig, dann für jedes Video) | `references/stil.md` | Stilregeln + Verbotsliste in stil.md, 3 Testszenen | ja |
| 2 | Skript | `references/skript.md` | `skript/skript.md`, Sätze nummeriert | ja |
| 3 | Storyboard | `references/storyboard.md` | `skript/storyboard.html` (Satz links, Bild rechts) | ja |
| 4 | Schnitt | `references/schnitt.md` | `schnitt/schnitt.mp4` + Wortzeiten | ja |
| 5 | Animationen | `references/animationen.md` | `animationen/<szene>/` als HTML + gerendertes Video | je Teil |
| 6 | Ton | `references/ton.md` | `ton/ton.wav` (Stimme, Musik, Effekte, −14 LUFS) | Musik wählt der User |
| 7 | Prüfen und exportieren | `references/pruefen.md` | `fertig/<titel>.mp4` | ja |
Der User kann an jeder Stelle einsteigen („hier ist meine Aufnahme“, „ich habe schon ein Skript“). Dann bei der passenden
Aufgabe beginnen und fehlende Grundlagen erfragen oder aus vorhandenen Dateien holen.
## Arbeitsweise
- **Erst planen, dann bauen.** Skript und Storyboard werden abgenommen, bevor eine Animation entsteht. Einen Plan zu ändern
  kostet fast nichts, eine fertige Animation zu ändern kostet Zeit und Rechenleistung.
- **Erst selbst prüfen, dann zeigen.** Vor jeder Vorschau: Kontaktbogen ansehen, Schnitt prüfen, Ton gegen Bild prüfen
  (`references/pruefen.md`). Was Claude findet, behebt es, bevor der User etwas sieht.
- **Nur ändern, was der User nennt.** Abgenommene Teile bleiben exakt so. Nach einer Notiz nur die betroffenen Teile neu rendern.
- **Kurz berichten.** Ergebnis zuerst, als Datei oder Pfad zum Ansehen. Nicht nacherzählen, was gemacht wurde.
- **Große Videos aufteilen.** Bei einem ganzen Video jedes Kapitel an einen eigenen Unteragenten geben (Bauauftrag mit Stil,
  Regeln, Wortzeiten des Kapitels). Danach jedes Ergebnis selbst prüfen.
## Der Skill lernt mit
Nach jeder Korrektur des Users fragen: Welche Anweisung hätte diesen Fehler verhindert? Diese Anweisung als neue Regel in
`references/regeln.md` (Abschnitt „Gelernt“) oder `references/stil.md` eintragen – kurz, mit Datum und Grund. So passiert
derselbe Fehler beim nächsten Video nicht mehr.
