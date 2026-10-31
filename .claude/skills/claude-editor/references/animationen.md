# Aufgabe 5: Animationen
Jede Animation ist eine kleine Webseite. Für jeden Zeitpunkt weiß die Seite genau, wo jedes Element steht. Der Renderer
öffnet die Seite im Hintergrund, macht für jeden Zeitpunkt ein Bild und setzt die Bilder zu einem Video zusammen
(30 Bilder pro Sekunde → eine Minute Video = 1.800 Bilder). Weil alles Code ist, lässt sich jede Kleinigkeit ändern.
## Aufbau
- Eine Szene = ein Ordner `animationen/<nr>_<name>/index.html`, Vorlage: `$SK/vorlagen/animation.html`.
- Vertrag: `window.FILM = { dauer, breite, hoehe, bereit, zeige(t) }`. `zeige(t)` stellt das Bild zur Zeit t her.
  Alles hängt nur von t ab – dann sieht jedes gerenderte Bild immer gleich aus.
- **Wortzeiten:** Jede Szene bekommt die Zeiten ihrer Ankerwörter aus `schnitt/schnitt_woerter.json` (relativ zum Start der
  Szene). Ein Element erscheint genau auf seinem Wort. Ändert sich der Schnitt, die Zeiten neu einsetzen und neu rendern.
- Stil aus `references/stil.md`, Verbotsliste vor jeder Szene lesen. Schriften lokal ablegen (`material/schriften/`) und per
  `@font-face` einbinden, damit das Rendern ohne Internet gleich aussieht.
## Arten von Szenen
- **Vollbild-Grafik:** deckt das ganze Bild ab (Grund nicht durchsichtig).
- **Über dir:** durchsichtiger Hintergrund (`background: transparent`), Text oder Grafik neben dir. Mit `--alpha` rendern.
  Darauf achten, dass nichts über dem Gesicht liegt (Gesichtsposition am Kontaktbogen der Aufnahme ablesen).
- **Webseiten und Belege:** Die Seite als ganzes Bild aufnehmen und in einem Browserfenster zeigen, das langsam scrollt:
  ```bash
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --hide-scrollbars \
    --window-size=1440,3000 --screenshot=material/seite.png "<adresse>"
  ```
  Dann eine Szene bauen, die dieses Bild in einem Fensterrahmen zeigt und die wichtige Stelle markiert. Seiten nie
  beschneiden, immer das ganze Fenster in voller Auflösung zeigen, damit man sieht, woher der Beleg kommt.
- **Text hinter dir:** braucht eine Freistellung (die Person wird in jedem Bild ausgeschnitten, dann liegen drei Ebenen
  übereinander: Raum – Grafik – Person). Das ist nicht Teil der Grundversion. Wenn der User es will: ein lokales
  Freistellungsmodell einrichten, an drei Bildern testen und das Ergebnis zeigen, bevor es für ein ganzes Video genutzt wird.
## Rendern
```bash
node $SK/scripts/render.mjs animationen/03_titel/index.html --bilder=0.5,1.2,3 --aus=pruefung/03   # erst Standbilder ansehen
node $SK/scripts/render.mjs animationen/03_titel/index.html --aus=animationen/03_titel/03_titel.mp4  # Vollbild-Szene
node $SK/scripts/render.mjs animationen/04_liste/index.html --alpha --aus=animationen/04_liste/04_liste.mov  # über dir
```
Nach jeder Änderung nur die betroffene Szene neu rendern. Lange Renderings dürfen über Nacht laufen.
## Ganzes Video
Jedes Kapitel bekommt einen eigenen Unteragenten mit einem Bauauftrag: Stil (stil.md), Regeln (regeln.md), die Sätze des
Kapitels aus dem Storyboard, die Wortzeiten, Vorlage und Renderbefehl. Die Unteragenten bauen gleichzeitig. Danach prüft
Claude jedes Ergebnis selbst (Kontaktbogen, Ankerwörter, Verbotsliste) und gibt Mängel zurück, bevor der User etwas sieht.
## Zusammensetzen
`schnitt/schnitt.mp4` bleibt unten, die Szenen liegen darüber – siehe `references/pruefen.md` (Export).
