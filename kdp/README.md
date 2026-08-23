# KDP-Skills

Arbeitsstand der Skills rund um die KDP-Bücher. Die Skills selbst laufen aus der
Skill-Bibliothek auf claude.ai; dieses Verzeichnis hält die bearbeiteten Dateien
versioniert fest, damit Änderungen nachvollziehbar bleiben.

## kdp-buch-becker-stil

`kdp-buch-becker-stil/SKILL.md` ist die neue Fassung der Skill-Datei. Geändert
gegenüber der bisherigen Version:

- Neuer Abschnitt **Impressum** mit der verbindlichen Vorlage für die
  Impressum-Seite, inklusive des Pflichtabsatzes **„Hinweis zu KI-generierten
  Inhalten"** (Coverbild und Text KI-gestützt). Der Absatz steht fest zwischen
  dem Telefonseelsorge-Absatz und dem Verantwortlichkeits-Block.
- Regeln für die zwei bedingten Sätze (Standortbestimmung, Fallgeschichten),
  für das Satzbild und eine Checkliste vor dem PDF-Export.
- Neuer Ablaufschritt „Impressum setzen" zwischen Manuskript und PDF-Bau. Der
  Abschnitt hat Vorrang vor dem älteren Impressum-Text in
  `assets/manuskript-vorlage.md`.
- Neuer Baustein `assets/autorenprofil.md` als Quelle für Name, Anschrift und
  E-Mail im Verantwortlichkeits-Block.

### Übernehmen

1. `kdp-buch-becker-stil/SKILL.md` in der Skill-Bibliothek als `SKILL.md` des
   Skills `kdp-buch-becker-stil` einsetzen.
2. `assets/autorenprofil.md` im Skill anlegen. Die Muster-Fassung mit
   Platzhaltern liegt hier als `kdp-buch-becker-stil/assets/autorenprofil.beispiel.md`.

Die übrigen Bausteine des Skills (`references/stimme.md`,
`references/struktur.md`, `assets/manuskript-vorlage.md`, `scripts/build_pdf.py`,
`scripts/README.md`) bleiben unverändert und liegen weiterhin nur in der
Skill-Bibliothek.

### Personenbezogene Daten

Dieses Repository ist öffentlich. Die echten Impressum-Angaben (Name, Anschrift,
E-Mail) stehen deshalb bewusst **nicht** hier, sondern nur in
`assets/autorenprofil.md` innerhalb der Skill-Bibliothek.
