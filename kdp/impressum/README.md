# Impressum-Standard für die KDP-Bücher

Verbindliche Vorlage für die Impressum-Seite **aller künftigen Bücher**. Sie ersetzt
den bisherigen Impressum-Baustein im Skill `kdp-buch-becker-stil`.

Neu gegenüber der alten Fassung ist der Absatz **„Hinweis zu KI-generierten Inhalten"**.
Er steht fest zwischen dem Telefonseelsorge-Absatz und dem Verantwortlichkeits-Block und
wird nicht mehr weggelassen.

## Dateien

| Datei | Inhalt |
| --- | --- |
| `impressum-vorlage.md` | Vorlage mit Platzhaltern – das ist die Quelle, die in den Skill gehört |
| `impressum-beispiel.md` | dieselbe Seite ausgefüllt, zum Gegenlesen des fertigen Satzes |

## Reihenfolge der Blöcke

Die Reihenfolge ist Teil der Vorlage und wird nicht umgestellt:

1. Überschrift „Impressum"
2. Buchtitel
3. Copyright-Zeile
4. „Alle Rechte vorbehalten."
5. Vervielfältigungs-Hinweis
6. **Wichtiger Hinweis** (Haftung / keine Therapie)
7. Telefonseelsorge / Notruf
8. **Hinweis zu KI-generierten Inhalten**
9. **Verantwortlich für den Inhalt (Impressum):** mit Name, Anschrift, E-Mail
10. Auflage und Jahr

## Platzhalter

| Platzhalter | Bedeutung |
| --- | --- |
| `{{BUCHTITEL}}` | Titel des Buchs, ohne Untertitel |
| `{{AUTOR_NAME}}` | Autorenname, wie er auf dem Cover steht |
| `{{JAHR}}` | Erscheinungsjahr – steht zweimal in der Seite (Copyright und Auflage) |
| `{{AUFLAGE}}` | Zahl der Auflage, in der Regel `1` |
| `{{STRASSE_NR}}`, `{{PLZ}}`, `{{ORT}}` | ladungsfähige Anschrift des Verantwortlichen |
| `{{EMAIL}}` | Kontaktadresse |
| `{{SATZ_STANDORTBESTIMMUNG}}` | siehe unten |
| `{{SATZ_FALLGESCHICHTEN}}` | siehe unten |

### Die zwei bedingten Sätze

Beide gehören in den Absatz „Wichtiger Hinweis" und beginnen jeweils mit einem
Leerzeichen, damit sie sich sauber an den vorherigen Satz anschließen.

`{{SATZ_STANDORTBESTIMMUNG}}` – nur einsetzen, wenn das Buch einen Selbsttest,
eine Standortbestimmung oder einen Fragebogen enthält:

> ` Die Standortbestimmung in diesem Buch ist kein geeichtes psychologisches Testverfahren.`

`{{SATZ_FALLGESCHICHTEN}}` – nur einsetzen, wenn das Buch Fallgeschichten,
Beispielpersonen oder Dialoge mit erfundenen Figuren enthält:

> ` Die Fallgeschichten sind erfunden; sie fassen typische Verläufe zusammen und beschreiben keine realen Personen.`

Trifft ein Punkt nicht zu, wird der Platzhalter ersatzlos entfernt – nicht umformuliert.

### Der KI-Hinweis

Standard ist der volle Absatz aus der Vorlage: Cover **und** Text sind KI-gestützt
entstanden. Weicht ein Buch davon ab, wird nur der betroffene Satz angepasst:

- Cover nicht KI-generiert → ersten Satz streichen.
- Text ohne KI geschrieben → zweiten Satz streichen.
- Beides trifft nicht zu → der ganze Absatz entfällt.

Der Absatz wird nie abgeschwächt oder in eine Fußnote verschoben.

## Satzbild

- Die Impressum-Seite steht im Backmatter, auf einer eigenen Seite, ohne Kolumnentitel.
- Jeder Block ist ein eigener Absatz mit Abstand, keine Aufzählungszeichen.
- „Wichtiger Hinweis:" und „Hinweis zu KI-generierten Inhalten:" sind fette Lead-ins,
  der Text läuft in derselben Zeile weiter – es sind keine Überschriften.
- „Verantwortlich für den Inhalt (Impressum):" steht fett allein auf einer Zeile,
  Anschrift und E-Mail folgen darunter.
- Buchtitel, Copyright, Anschrift, E-Mail und Auflage stehen je auf einer eigenen Zeile.

## Einbau in den Skill `kdp-buch-becker-stil`

Der Skill liegt in der Skill-Bibliothek auf claude.ai, nicht in diesem Repo. Zum
Übernehmen:

1. In `assets/manuskript-vorlage.md` den bisherigen Impressum-Abschnitt durch den
   Inhalt von `impressum-vorlage.md` ersetzen.
2. In `references/struktur.md` beim Backmatter vermerken, dass die Impressum-Seite
   dieser Vorlage folgt und der KI-Hinweis Pflichtbestandteil ist.

## Rechtliches

Name und Anschrift im Verantwortlichkeits-Block müssen echt und ladungsfähig sein;
ein Postfach oder ein reines Pseudonym reicht nicht. Ob für ein konkretes Buch
weitere Pflichtangaben nötig sind, ist hier nicht geprüft – im Zweifel vor der
Veröffentlichung rechtlich abklären.
