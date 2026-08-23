---
name: kdp-buch-becker-stil
description: >
  Schreibt komplette Sachbücher / Selbsthilfebücher im Stil von Christian Becker ("Chris")
  und baut daraus ein druckfertiges 6×9-Zoll-PDF für Amazon KDP. Nutze diesen Skill immer,
  wenn der Nutzer ein neues Buch, ein weiteres Buch, ein Kapitel, ein Vorwort/Nachwort oder
  ein KDP-Manuskript "in seinem Stil", "wie Autopilot", "wie Jetzt steuerst du" oder "so ein
  Buch wie meine anderen" erstellt haben will – auch wenn er nur ein Thema nennt ("mach mir
  ein Buch über X") und den Stil nicht ausdrücklich erwähnt. Deckt Themenfindung, Gliederung
  (Teile + Kapitel), das Schreiben in der richtigen Stimme, Übungen ("Dein Moment"),
  Front-/Backmatter, Kurs-CTA und Impressum sowie den PDF-Export ab.
---

# KDP-Buch im Becker-Stil

Dieser Skill erstellt ganze Bücher in der unverwechselbaren Stimme des Autors **Christian Becker** (Signatur "Chris") und exportiert sie als **druckfertiges 6×9-Zoll-PDF für Amazon KDP** (Taschenbuch). Vorbilder sind seine Bücher *„Autopilot – Das ist nicht dein Leben"* und *„Jetzt steuerst du"*.

Der eigentliche Wert liegt in zwei Dingen: **die Stimme trifft** (ruhig, direkt, ehrlich, kein Motivations-Hype) und **die Architektur stimmt** (Teile → Kapitel → „Dein Moment"-Übung → Kapitel-Teaser). Alles andere ist Handwerk.

## Ablauf

Arbeite in dieser Reihenfolge. Bei jedem Schritt zuerst denken, dann schreiben.

1. **Auftrag klären.** Frage – falls nicht schon bekannt – nach: Thema/Versprechen des Buchs, Zielgruppe, ungefährer Umfang (Autopilot ≈ 105 Seiten / 14 Kapitel, Jetzt steuerst du ≈ 202 Seiten / 28 Kapitel), und ob es zur bestehenden Reihe gehört (dann Querverweise auf *Autopilot*). Mehr als 2–3 Fragen sind selten nötig – der Stil und die Struktur stehen ja fest.

2. **Stimme laden.** Lies `references/stimme.md`. Das ist der wichtigste Teil. Ohne die richtige Stimme ist der Rest wertlos.

3. **Struktur bauen.** Lies `references/struktur.md`. Entwirf zuerst die Gliederung: 5–6 Teile, je 2–3 Kapitel, mit einem klaren emotionalen Bogen (Erkennen → Verstehen → Handeln → Dranbleiben). Leg die Gliederung dem Nutzer kurz vor, bevor du das ganze Buch schreibst – so lässt sich früh nachsteuern.

4. **Manuskript schreiben.** Schreibe das Buch als **eine** Markdown-Datei nach dem Format in `references/struktur.md`. Nimm `assets/manuskript-vorlage.md` als Gerüst – dort sind alle Bausteine (Zum Buch, Vorwort, Teile, Kapitel, „Dein Moment", Nachwort, Kurs-CTA, Impressum) vorformatiert. Schreib die Kapitel aus, nicht als Stichpunkte. Ein Kapitel sind im Druck grob 5–6 Seiten, also etwa 1.100–1.500 Wörter Fließtext.

5. **Impressum setzen.** Übernimm die Impressum-Seite **wörtlich** aus dem Abschnitt „Impressum" weiter unten. Der Abschnitt gilt für jedes Buch und hat Vorrang vor allem, was in `assets/manuskript-vorlage.md` noch an älterem Impressum-Text steht.

6. **PDF bauen.** Erzeuge das druckfertige PDF mit dem Builder:
   ```bash
   python3 scripts/build_pdf.py <manuskript.md> <ausgabe.pdf>
   ```
   Der Builder setzt automatisch 6×9-Zoll-Seiten mit gespiegelten KDP-Rändern, Blocksatz mit deutscher Silbentrennung, laufende Kolumnentitel, Seitenzahlen, Teil- und Kapitelseiten, das Inhaltsverzeichnis und die „Dein Moment"-Kästen. Details und Optionen: `scripts/README.md`.

7. **Prüfen und übergeben.** Nenne dem Nutzer den Pfad zum PDF, die Seitenzahl und die Kapitelübersicht. Weise darauf hin, dass für KDP noch ein Cover (separat) und ein QR-Code (Platzhalter „QR-Code hier einfügen" ist im Backmatter vorgesehen) gebraucht werden. Kontrolliere vor der Übergabe die Impressum-Checkliste am Ende dieses Skills.

## Impressum

Die Impressum-Seite steht im Backmatter, auf einer eigenen Seite, ohne Kolumnentitel. Sie folgt **immer** dieser Vorlage – Wortlaut und Reihenfolge werden nicht umformuliert, gekürzt oder getauscht.

Name, Anschrift und E-Mail kommen aus `assets/autorenprofil.md`. Ist die Datei nicht vorhanden oder passt das Profil nicht zum Buch (anderes Pseudonym), frag den Nutzer einmal nach den Angaben – rate sie nie.

```markdown
# Impressum

{{BUCHTITEL}}

© {{JAHR}} {{AUTOR_NAME}}

Alle Rechte vorbehalten.

Kein Teil dieses Buches darf ohne schriftliche Genehmigung des Autors reproduziert, vervielfältigt oder übertragen werden.

**Wichtiger Hinweis:** Dieses Buch ersetzt keine Diagnose, keine Beratung und keine Psychotherapie. Es beschreibt allgemein zugängliches Wissen und Übungen zur Selbsthilfe, die du in eigener Verantwortung anwendest.{{SATZ_STANDORTBESTIMMUNG}}{{SATZ_FALLGESCHICHTEN}}

Wenn dich das Lesen stark belastet oder wenn du daran denkst, dir das Leben zu nehmen, hol dir Hilfe. Die Telefonseelsorge ist rund um die Uhr kostenlos erreichbar unter 0800 111 0 111 und 0800 111 0 222. Im Notfall wähle 112.

**Hinweis zu KI-generierten Inhalten:** Das Coverbild wurde mit einem KI-Bildgenerator erstellt und zeigt keine reale Person. Auch der Text dieses Buches ist unter Einsatz von KI entstanden und wurde redaktionell überarbeitet.

**Verantwortlich für den Inhalt (Impressum):**

{{AUTOR_NAME}}, {{STRASSE_NR}}, {{PLZ}} {{ORT}}

{{EMAIL}}

{{AUFLAGE}}. Auflage, {{JAHR}}
```

### Der KI-Hinweis

Der Absatz **„Hinweis zu KI-generierten Inhalten"** ist Pflichtbestandteil jedes Buchs. Er steht fest zwischen dem Telefonseelsorge-Absatz und dem Verantwortlichkeits-Block, wird nie abgeschwächt, nie in eine Fußnote verschoben und nie weggelassen.

Nur wenn ein Buch tatsächlich anders entstanden ist, wird der betroffene Satz gestrichen:

- Cover nicht mit KI erstellt → ersten Satz streichen.
- Text ohne KI geschrieben → zweiten Satz streichen.
- Beides trifft nicht zu → nur dann entfällt der ganze Absatz.

### Die zwei bedingten Sätze

Beide gehören in den Absatz „Wichtiger Hinweis" und beginnen mit einem Leerzeichen, damit sie sich sauber an den Satz davor anschließen.

`{{SATZ_STANDORTBESTIMMUNG}}` – nur einsetzen, wenn das Buch einen Selbsttest, eine Standortbestimmung oder einen Fragebogen enthält:

> ` Die Standortbestimmung in diesem Buch ist kein geeichtes psychologisches Testverfahren.`

`{{SATZ_FALLGESCHICHTEN}}` – nur einsetzen, wenn das Buch Fallgeschichten, Beispielpersonen oder Dialoge mit erfundenen Figuren enthält:

> ` Die Fallgeschichten sind erfunden; sie fassen typische Verläufe zusammen und beschreiben keine realen Personen.`

Trifft ein Punkt nicht zu, wird der Platzhalter ersatzlos entfernt – nicht umformuliert.

### Satzbild

- Jeder Block ist ein eigener Absatz mit Abstand, keine Aufzählungszeichen.
- „Wichtiger Hinweis:" und „Hinweis zu KI-generierten Inhalten:" sind fette Lead-ins, der Text läuft in derselben Zeile weiter. Es sind keine Überschriften.
- „Verantwortlich für den Inhalt (Impressum):" steht fett allein auf einer Zeile, Anschrift und E-Mail folgen darunter.
- Buchtitel, Copyright-Zeile, Anschrift, E-Mail und Auflage stehen je auf einer eigenen Zeile. Der Buchtitel steht ohne Untertitel da.
- `{{JAHR}}` steht zweimal auf der Seite (Copyright und Auflage) und muss beide Male gleich sein.

### Checkliste vor dem Export

- [ ] KI-Hinweis vorhanden und an der richtigen Stelle
- [ ] Kein `{{...}}`-Platzhalter mehr im Text
- [ ] Bedingte Sätze passen zum tatsächlichen Buchinhalt
- [ ] Anschrift ist echt und ladungsfähig, nicht nur ein Pseudonym oder Postfach
- [ ] Auflage und Jahr stimmen mit der KDP-Veröffentlichung überein

## Was dieses Buch NIE sein darf

Diese Grenzen definieren die Marke stärker als jede Stilregel. Halte sie ausnahmslos ein:

- **Kein Motivationsgeschrei.** Keine Ausrufezeichen-Kaskaden, kein „Du schaffst alles!", kein „dein bestes Leben". Der Autor grenzt sich im ersten Buch ausdrücklich davon ab.
- **Keine leeren Versprechen.** Nichts ändert sich „über Nacht". Veränderung passiert in kleinen, ehrlichen Schritten. Das ist die Kernbotschaft.
- **Keine Belehrung von oben.** Der Autor steht neben dem Leser, nicht über ihm. Er war selbst über zwanzig Jahre im Autopilot (Volkswagen, Krankenhaus als Wendepunkt).
- **Kein Fachjargon, keine Studien-Zitate-Schlacht.** Alltagssprache, konkrete Bilder (das schleichende Gewicht auf den Schultern, das Handy in der leeren Minute).

## Bausteine im Überblick

- `references/stimme.md` – die Autorenstimme: Ton, Rhythmus, Anrede, wiederkehrende Bilder, Do/Don't, Formulierungsbeispiele. **Immer zuerst lesen.**
- `references/struktur.md` – Architektur des Buchs, Anatomie eines Kapitels, die „Dein Moment"-Übung, das Manuskript-Format für den PDF-Builder.
- `assets/manuskript-vorlage.md` – ausfüllbares Manuskript-Gerüst mit allen Bausteinen.
- `assets/autorenprofil.md` – Name, Anschrift und E-Mail für den Verantwortlichkeits-Block im Impressum.
- `scripts/build_pdf.py` – erzeugt das druckfertige KDP-PDF aus dem Manuskript.
- `scripts/README.md` – Bedienung und Optionen des Builders (Seitenformat, Ränder, Schrift).
