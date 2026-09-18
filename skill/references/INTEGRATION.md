# Integration in Codex, Claude Code und weitere Komponenten

## Gemeinsames Format

Der Skill verwendet eine `SKILL.md` mit den gemeinsamen Feldern `name` und
`description`, ergänzt um Skripte, Referenzen und Assets. In Claude Code lautet der
explizite Aufruf `/contextme`; in Codex kann `$contextme` verwendet werden.
`agents/openai.yaml` ergänzt optionale Codex-Anzeigedaten und erlaubt implizite
Auswahl. Es werden keine hostfremden Hooks oder Berechtigungsdateien installiert.

Der Installer nutzt persönliche Skill-Pfade oder die projektlokalen Entsprechungen.
Der Arbeitsordner ist davon getrennt. Beide Hosts können denselben lokalen Speicher
verwenden; Schreibvorgänge werden gesperrt. Ein zweiter gleichzeitiger Schreibversuch
wird mit Fehler beendet, statt den anderen zu überschreiben. Nach Ende des ersten
Laufs kann der zweite Auftrag erneut ausgeführt werden. Keine Lock-Datei während
eines laufenden Prozesses entfernen.

## Am Anfang und Ende einer Sitzung mitlaufen lassen

Ein installierter Skill wird nicht garantiert vor jeder beliebigen Aufgabe geladen.
Die Beschreibung ermöglicht passende Auswahl; verlässliche eigene Abläufe benötigen
eine Host-Regel. Den folgenden Block **nach Prüfung durch den Benutzer** in die
persönliche/projektbezogene `AGENTS.md` bzw. `CLAUDE.md` einfügen. Den Pfad ersetzen;
nicht ungefragt bestehende Dateien überschreiben.

```markdown
## Persönlicher Kontext mit ContextMe

Für Aufgaben, deren Ergebnis von meinen Rollen, Projekten, Prioritäten,
Interessen oder Arbeitsweisen abhängt, nutze den installierten Skill contextme.
Der Arbeitsordner ist /ABSOLUTER/PFAD/ContextMe.

Bestimme vor dem Abruf den erlaubten Kontext: work, private, hobby oder einen
Unterkontext. Lade nur den dafür nötigen Ausschnitt. General enthält ausschließlich
von mir für alle Kontexte freigegebenen Hintergrund. Nie den vollständigen
persönlichen Speicher in berufliche Antworten oder externe Artefakte kopieren.

Nach einer von mir beauftragten Auswertung oder ausdrücklichen Kontextkorrektur
übernimm neue, belegte, nicht sensible Erkenntnisse über den Skill. Gewichte dürfen
sich automatisch verändern. Erfinde keine Fakten und zähle deine eigenen
Materialabrufe nicht als meine Aktivität. Offene Fragen nur stellen, wenn sie die
aktuelle Aufgabe wesentlich beeinflussen. Sonst Unsicherheit transparent vorhalten.
```

Das ist eine Anweisung an den Host, kein Betriebssystemdienst. Das Paket ändert
keine systemweiten Prompts und behauptet keine bereits laufende Überwachung.

## Geplante Aktualisierung

Ein Host-Scheduler kann einen wiederkehrenden Auftrag aufrufen, etwa:

```text
Nutze contextme mit /ABSOLUTER/PFAD/ContextMe.
Lies ausschließlich die seit dem letzten erfolgreichen Lauf neu hinzugekommenen
Dokumente im freigegebenen Ordner /ABSOLUTER/PFAD/Eingang. Ermittle daraus neue
Kontextangaben und relevante Veränderungen. Erhalte ursprüngliche Zeitstempel,
dedupliziere Dokumente und übernimm sichere nicht sensible Erkenntnisse automatisch.
Aktualisiere anschließend NOW. Berichte nur wesentliche Änderungen und Fehler.
```

Zeitplan, Zugangsdaten, Toolrechte und Modellaufruf gehören zum Host. Diese Vorlage
ist **kein eingerichteter Zeitplan**. Für Mails/Kalender entsprechend bereits
verbundene, autorisierte Werkzeuge des Hosts nutzen; der Skill enthält keine
providerabhängige Mailimplementation. Zugriffsprobleme müssen sichtbar bleiben.

## Nutzung durch ein Second Brain

Der einordnende Agent liest das Material, erkennt semantisch Entitäten, fragt
ContextMe mit geeigneten IDs ab und kombiniert persönliche Relevanz mit der
Herkunft des Materials. Der Rückgabewert ist ein Vorschlag, keine Pflicht zur
Ablage in genau einem Ordner.

Wichtig ist die Trennung von:

- **Was ist das Material?** Inhalt, Entstehung, Autor, tatsächlicher beruflicher
  oder privater Zusammenhang.
- **Was bedeutet es für diese Person?** Aktuelle Relevanz, laufende Projekte,
  historische Kompetenz, private oder berufliche Nutzbarkeit.
- **Was folgt daraus?** Verlinken, priorisieren oder in der Inbox belassen; keine
  unautorisierte Löschung, Veröffentlichung oder automatische Ausführung.

Für kleinere Kontextpakete `context`, für ausführliche Objekt-/Trenddetails
`snapshot` oder `classify` verwenden. Eine Komponente ohne lokalen Dateizugriff
kann explizit exportierte, gescopete JSON-/Markdown-Pakete erhalten. Ein echter
MCP-Server ist in dieser Version nicht enthalten. Ein späterer Adapter kann die
vorhandenen CLI-Aufrufe kapseln; dazu ist keine Änderung des Datenmodells nötig.

## Zwei Hosts, mehrere Rechner

Der lokale Schreiblock schützt auf einem gemeinsamen lokalen Dateisystem. Er ist
kein verteilter Lock über iCloud, OneDrive oder mehrere Rechner. Für solche
Szenarien entweder einen einzigen schreibenden Host nutzen oder vor jeder
Synchronisation Schreibvorgänge beenden und Konflikte prüfen. Gleichzeitiges
Bearbeiten synchronisierter Kopien wird nicht unterstützt.

Eine abgebrochene Ausführung kann eine `.write-lock` zurücklassen. Erst prüfen,
dass der darin genannte Prozess wirklich nicht mehr arbeitet, dann die Sperre
manuell entfernen und `doctor` sowie `update-now` ausführen. Nicht automatisiert
nach Zeitablauf entsperren: Ein langsamer Schreibvorgang könnte noch aktiv sein.
