# Stil
Der Stil gilt für jedes Video. Solange die Abschnitte unten leer sind, zuerst den Stil einrichten (Ablauf direkt hier).
Ohne Vorgaben baut Claude immer ähnliche, austauschbare Grafiken – der Stil ist deshalb der wichtigste Schritt.
## So richtest du den Stil ein
1. **Beispiele sammeln.** Den User um Screenshots oder Videos bitten, die ihm gefallen (in `material/stil/` ablegen).
   Videos mit `kontaktbogen.py --alle 0.5` Bild für Bild auswerten, bei Effekten `--alle 0.0333` (jedes Bild).
2. **Beschreiben.** In eigenen Worten zusammenfassen, was die Beispiele ausmacht: Schriften, Farben, Hintergründe,
   Bewegungen (Tempo, Kurven), Übergänge, Aufbau der Szenen, wie Text und Person zusammenspielen. Dem User zeigen.
3. **Drei Testszenen bauen** (je 4–6 s, unterschiedliche Bildarten: z. B. Titel, Vollbild-Grafik, Übergang),
   rendern und zeigen. Der User sagt, was passt und was nicht. Wiederholen, bis die Testszenen sitzen.
4. **Eintragen.** Alles Ergebnis unten festhalten. Erst danach Animationen für ein ganzes Video bauen.
## Farben
Abgenommen am 31.10.2026. Mix aus Dominik Lebersorger und Robin Fübbeker (aus vidIQ-Analysen, Farbwerte geschätzt).
- Grund: fast Schwarz #0B0B0C mit weichem Lichtfleck in der Mitte (#1A1B1F). Nie reines #000, nie Weiß als Vollbild.
- Schrift: Weiß #FFFFFF, zweite Ebene Grau #8E9096, inaktiv #55575C.
- Linien und Kreise: Weiß mit 22 % Deckkraft (rgba(255,255,255,.22)).
- Eine Akzentfarbe, nur für aktive Zustände, Zähler und Nummern: warmes Orange #E2723F.
- Bedeutungsfarben nur bei gut gegen schlecht: Grün #4EBA6F, Rot #E5484D.
- Fertige Werte als CSS-Variablen: `videos/_stil/animationen/stil.css`. Jede neue Szene bindet diese Datei ein.
## Schriften
- Zitate, Regeln, Kapiteltitel: Playfair Display (Serif), Regular, betontes Satzende kursiv.
- Alles andere: Inter. Überschriften Medium, große Zahlen Light, Labels in Großbuchstaben mit weiter Laufweite (0,28em).
- Dateien: `videos/_stil/material/schriften/` (Playfair als woff2, Inter als otf). Pfade in CSS relativ zur CSS-Datei.
## Bewegung und Übergänge
- Auftritt: 0,4 s einblenden und 14 px von unten, Kurve expo-out (schnell rein, lange sanft aus). Kein Federn, kein Hüpfen.
- Abgang: 0,3 s ausblenden.
- Listen und Übersichten: inaktive Punkte unscharf (6 px) und gedimmt (35 %), der aktive wird scharf, 8 % größer,
  weißer Rand und Schein in der Akzentfarbe, Unterstrich in Akzentfarbe.
- Zähler „Freigeschaltet 03/07“ oben rechts, springt auf dem Ankerwort weiter.
- Ganz langsamer Drift (3 px pro Sekunde) bei ruhigen Vollbildern, damit das Bild nie steht.
- Text bleibt 2 bis 3,5 s stehen.
- Zwischen Szenen nur harte Schnitte, keine Übergangseffekte.
- Fertige Funktionen (auftritt, fokus, aus, ein, fort): `videos/_stil/animationen/bewegung.js`.
## Aufbau der Szenen
- Kamera: Brustbild mittig, geringe Schärfentiefe, dunkler Raum mit warmem Licht im Hintergrund, gedeckte Farben.
- Alle 2 bis 4 s ein Wechsel (Schnitt, Zoom 10 bis 15 % auf die Aufnahme oder Grafik). Nie länger als 5 s dasselbe Bild.
- Vollbild-Grafik für Kapitelübersicht, Zitate und Zahlen. Bei längeren Erklärgrafiken die Person als abgerundetes
  Fenster unten rechts.
- Wiederkehrendes Muster: Übersicht aller Punkte am Anfang, vor jedem Punkt dieselbe Übersicht mit dem nächsten Punkt aktiv.
- Ton: ruhige Ambient- oder Lo-Fi-Musik deutlich unter der Stimme. Leiser Klick bei jedem Zustandswechsel, tiefes leises
  Whoosh bei neuem Kapitel, sonst keine Effekte.
- Vorbild-Szenen (abgenommen): `videos/_stil/animationen/01_zitat`, `02_kapitel`, `03_zahlen`.
## Verbotsliste
- Wort-für-Wort-Untertitel im Karaoke-Stil, bunte Untertitel mit Kontur
- Meme-Sounds, Vine-Boom, laute Whooshes auf jedem Schnitt
- Grelle oder bunte Hintergründe, Farbverläufe über die ganze Fläche
- Papier-, Grunge-, Film- oder Rauschtexturen
- 3D-Kamerafahrten, Glitch- und Wackel-Übergänge
- Emojis, Sticker, Meme-GIFs, Stockfoto-Optik
- Kleine Kärtchen auf leerem Grund, die wie eine Präsentation wirken
- Mehr als eine Akzentfarbe gleichzeitig
