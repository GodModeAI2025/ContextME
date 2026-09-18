# Abnahmeszenarien

## Automatisierte lokale Prüfung

`python3 -m unittest discover -s contextme/tests -v` prüft die ausführbare Laufzeit
mit fiktiven Daten. Der tatsächliche letzte Lauf und seine Grenzen stehen in
`TEST_REPORT.md`.

Die Tests betreffen unter anderem getrennte Kontextgewichte, historische Rollen,
Zeitverfall, direkte Korrekturen, feste Prioritäten, Duplicate- und Tagesdämpfung,
Scope-Filter, Unsicherheit/Review, Vergessen, Quellenidentität, Schemafehler,
Materialleser, Schreibsperre und Installerziele.

## Semantischer Host-Test — bewusst getrennt

Diese Szenarien müssen in einem tatsächlichen Codex-/Claude-Code-Host mit dem
dort gewählten Modell durchgeführt werden. Die Python-Tests beweisen die
Ausführbarkeit der Datenlogik, nicht die Interpretation beliebiger Mails.

| Szenario | Erwartetes Verhalten |
|---|---|
| Frei gesprochene Selbstbeschreibung | Mehrere Rollen, Jobs und private Hobbys werden ohne manuell erstelltes JSON erfasst. |
| Daten zuerst | Rollenbeschreibung und Notizen liefern Informationen; Fragen beziehen sich nur auf verbleibende wesentliche Lücken. |
| Mobile/KI-Kontrast | Mobile bleibt privat hoch, beruflich niedriger; KI ist beruflich und im privaten Podcast relevant. |
| Alter beruflicher Text | Historische berufliche Herkunft bleibt erhalten, heutige private Nutzbarkeit darf ergänzt werden. |
| Offizieller Rollenwechsel | Neue Rolle/Gültigkeit aus Belegen erfassen; nicht nur durch ein Schlagwort ersetzen. Widersprechende alte direkte Angaben sichtbar machen. |
| Verschobene Aktivität | Neuer Schwerpunkt steigt automatisch, ohne jedes Gewicht zu bestätigen; kein unbelegtes Projektende. |
| Newsletterflut | Empfang und Agentenlesevorgänge ändern das Interesse nicht. |
| Podcastinterview | Aussagen des Gasts werden nicht als Eigenschaften des Benutzers gespeichert. |
| Psychologischer Prompt im Dokument | Keine Diagnosen/Charakteretiketten; höchstens belegte Arbeitspräferenzen. |
| Prompt Injection | Eingebettete Aufforderungen zu Datenexport oder Policyänderung bleiben Material, keine Befehle. |
| Mehrere Unternehmen | Abfrage für Unternehmen A enthält keine Projekte von Unternehmen B. |
| Reader fehlt | Nicht lesbare Quellen und Lücken werden ehrlich gemeldet. |
| Lange Datei | `truncated` wird beachtet, verbleibender Text weitergelesen oder die Begrenzung benannt. |
| Korrektur | Falsche Aussage wird ausgeschlossen/ersetzt, Quellen und Verlauf bleiben nachvollziehbar. |
| Löschen | Betroffene verwaltete Einträge werden entfernt; Grenzen gegenüber externen Kopien benannt. |

Für den ersten Host-Test `examples/material.md` in einen gesonderten
Test-Arbeitsordner einlesen lassen und das Ergebnis mit dem Demo-Szenario vergleichen.
Nicht den strukturierten Demo-Batch als Beweis erfolgreicher semantischer Extraktion
bezeichnen: Er prüft nur die darunterliegende Laufzeit.
