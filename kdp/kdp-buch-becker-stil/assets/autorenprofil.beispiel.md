# Autorenprofil

Quelle für den Verantwortlichkeits-Block im Impressum. Der Skill liest die Werte
hier aus und setzt sie in die Impressum-Vorlage ein.

Diese Datei ist die Muster-Fassung mit Platzhaltern. Im Skill selbst heißt sie
`assets/autorenprofil.md` und enthält die echten Angaben.

| Feld | Wert |
| --- | --- |
| `{{AUTOR_NAME}}` | Max Mustermann |
| `{{STRASSE_NR}}` | Musterstraße 1 |
| `{{PLZ}}` | 12345 |
| `{{ORT}}` | Musterstadt |
| `{{EMAIL}}` | info@beispiel.de |

Schreibt der Autor unter mehreren Namen, bekommt jeder Name einen eigenen
Abschnitt, und der Skill fragt beim Buchstart, welcher gilt.

Die Anschrift muss echt und ladungsfähig sein – ein Postfach oder ein reines
Pseudonym reicht für die Impressumspflicht nicht.
