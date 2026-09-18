# ContextMe 1.0.0

**Ein persönlicher Kontext-Skill für Codex und Claude Code.** Er lernt aus direkten
Aussagen, Interviews und freigegebenem Material, welche Rollen, Projekte,
Interessen, Ziele und Arbeitsweisen für dich relevant sind. Berufliche, private
und Hobby-Kontexte werden getrennt gewichtet, aber miteinander verknüpft.

Das Paket enthält den Skill **und ausführbare lokale Verwaltungslogik**, nicht
nur eine Ordnerbeschreibung. Die semantische Auswertung übernimmt das Modell des
Hosts; Python übernimmt Speicherung, Validierung, Historie und Gewichtung.

## Installation

Voraussetzung: Python **3.10+** sowie ein eingerichtetes Codex oder Claude Code mit
Datei- und Ausführungszugriff. Keine zusätzlichen Python-Pakete, Datenbankdienste
oder API-Schlüssel für ContextMe nötig.

ZIP entpacken. Im Ordner, der den entpackten Ordner `contextme` enthält:

```sh
python3 contextme/scripts/install.py --target both --workspace "$HOME/ContextMe"
```

Unter Windows in PowerShell:

```powershell
py -3 contextme/scripts/install.py --target both --workspace "$HOME\ContextMe"
```

Der Installer kopiert den Skill nach `~/.agents/skills/contextme` für Codex und
`~/.claude/skills/contextme` für Claude Code. Er initialisiert den privaten
Arbeitsordner und hinterlegt dessen Pfad in `~/.contextme/location.json`.
Bestehende Installationen werden nicht ohne `--replace` ersetzt; dabei wird eine
Sicherung der alten Skill-Dateien außerhalb der Skill-Suchverzeichnisse angelegt.

Die gleichen Dateien lassen sich projektlokal installieren:

```sh
python3 contextme/scripts/install.py --target both --project "/Pfad/zum/Projekt"
```

Der **persönliche Datenordner gehört nicht ins gemeinsame Projekt-Repository**.
`--workspace` bleibt bei Projektinstallation optional; im Gespräch den privaten
Datenpfad nennen oder `CONTEXTME_WORKSPACE` setzen.

Codex und Claude Code gegebenenfalls neu starten. Bei einer neuen Sitzung:

**Codex:**

```text
$contextme Nutze meinen eingerichteten Arbeitsordner. Erhebe mein Kontextprofil
zuerst aus dem Material, das ich dir gebe. Leite Rollen, Projekte, Status,
Interessen und Arbeitsweisen selbstständig ab. Unterscheide beruflich, privat
und Hobby. Frage nur die wichtigsten verbleibenden Lücken nach.
```

**Claude Code:**

```text
/contextme Nutze meinen eingerichteten Arbeitsordner. Erhebe mein Kontextprofil
zuerst aus dem Material, das ich dir gebe, und frage nur wesentliche Lücken nach.
```

Der Benutzer muss weder einen Batch schreiben noch alle Attribute selbst
aufschreiben. Der Host folgt dem Erhebungsablauf in `SKILL.md` und erzeugt die
strukturierten Eingaben selbst.

## Was enthalten ist

| Bereich | Inhalt |
|---|---|
| Profil | Identität/Biografie, Unternehmen, mehrere Rollen, Aufgaben und Teamkontext |
| Vorhaben | Projekte, Status, nächste Schritte, Ziele, Aufgaben und Kalenderbezüge |
| Interessen | Themen, Hobbys, persönliche Relevanz pro Kontext, aktuelle und historische Verbindung |
| Zusammenarbeit | Arbeitsweise, konkrete Entscheidungsmuster, Kommunikation, Werte, Stärken, Vorlieben, Grenzen |
| Wissensbezug | Life Library, persönliche Notizen zu Ressourcen, Anwendungsideen, Routinen/SOPs und Rückblicke |
| Laufzeit | JSON-Ereignisspeicher, Markdown-Sichten, Frequenz-/Trendindex, quellengestützte Kontextpakete |
| Betrieb | Installer, Datenschema, Extraktionsregeln, Testdaten und automatisierte Tests |

Alle 24 Dimensionen sind vom ersten Start an vorhanden. Es ist kein Interview mit
60 Pflichtfragen: Der Skill erhebt verfügbare Angaben aus Material und kennzeichnet
fehlende Informationen als unbekannt.

## Das zentrale Beispiel

„Mobile“ existiert als Thema einmal. Seine Bedeutung kann gleichzeitig lauten:

| Thema | Kontext | Relevanz |
|---|---|---|
| Mobile | Beruflich | Niedrig |
| Mobile | Privat | Hoch |
| KI | Beruflich | Hoch |
| KI | Privat / privater Podcast | Hoch |

Die frühere Mobile-Rolle wird historisch, nicht gelöscht. Ein damaliges berufliches
Mobile-Dokument bleibt beruflicher Herkunft, auch wenn sein Inhalt heute zusätzlich
für private Projekte interessant ist. Die automatische Klassifizierung schlägt
Verknüpfungen vor; sie verschiebt keine Originaldateien.

`examples/demo-batch.json` stellt dieses Szenario mit einer **fiktiven Person und
einem fiktiven Unternehmen** dar. Es wird niemals automatisch in deinen echten
Arbeitsordner importiert.

## Einmal lokal ausprobieren

In einem separaten Demo-Arbeitsordner, nicht in deinem echten Profil:

```sh
python3 contextme/scripts/contextme.py --workspace ./contextme-demo init
python3 contextme/scripts/contextme.py --workspace ./contextme-demo ingest --batch contextme/examples/demo-batch.json
python3 contextme/scripts/contextme.py --workspace ./contextme-demo classify --text "Mobile und KI" --at 2026-09-17T12:00:00Z
python3 contextme/scripts/contextme.py --workspace ./contextme-demo doctor
```

Das feste Datum macht die Demo reproduzierbar. Im Alltag `--at` weglassen.

## Arbeitsverzeichnis

```text
ContextMe/
├── policy.json                    # Einstellbare Gewichtungsregeln und Kontexte
├── state/
│   └── events.json                # Maßgeblicher Ereignisspeicher mit Quellen
├── NOW.md                         # Kompakte aktuelle Sicht für den Eigentümer
├── INDEX.md                       # Einstieg in die lesbaren Objektseiten
└── views/                         # Automatisch erzeugt, nicht manuell editieren
    ├── CONTEXT.json                # Aktuelle strukturierte Sicht
    ├── FREQUENCY.json              # Häufigkeit, Aktivität, Trend je Kontext
    ├── REVIEW.json                 # Unsichere Hypothesen und Widersprüche
    ├── COVERAGE.md                 # Welche Attributgruppen bereits belegt sind
    ├── scopes/work/NOW.md          # Beruflicher Ausschnitt
    ├── scopes/private/NOW.md       # Privater Ausschnitt einschließlich Hobby
    ├── role/*.md
    ├── project/*.md
    ├── topic/*.md
    └── ...                        # Weitere Objekttypen nach Bedarf
```

`events.json` wird bei normalen Änderungen fortgeschrieben; ältere Aussagen
bleiben nachvollziehbar. Das ausdrücklich ausgelöste `forget` bereinigt den
betroffenen gespeicherten Verlauf. Atomarer Austausch und eine lokale Schreibsperre
schützen vor parallelen lokalen Schreibern. Der Speicher ist kein verteiltes
Mehrbenutzersystem; Cloud-Sync-Konflikte werden nicht automatisch zusammengeführt.

## Schnittstelle für andere Skills und Second Brains

```sh
python3 contextme/scripts/contextme.py --workspace "/Pfad/ContextMe" context \
  --context work --query "Aktuelle Rolle und Prioritäten" --max-chars 12000

python3 contextme/scripts/contextme.py --workspace "/Pfad/ContextMe" classify \
  --entities ai mobile --context private --text "Zusammenfassung des Materials"
```

`context` liefert ein begrenztes JSON-Paket mit Angaben, Quellen-IDs, Herkunft,
Unsicherheit und Relevanz. `classify` liefert passende Kontexte und Links, ist aber
**lesend**: Eine bloße Klassifizierungsabfrage verstärkt nicht das Interesse an
dem Thema. Ohne semantisch vom Host bestimmte `--entities` nutzt die CLI einen
ausdrücklich gekennzeichneten Alias-/Wortabgleich.

## Automatisch lernen – ohne ständige Bestätigung

Ausreichend belegte, nicht sensible Angaben werden automatisch übernommen.
Unsichere Hypothesen landen in der Prüfliste. Direkte Aussagen und Korrekturen
haben Vorrang vor Ableitungen. Häufigkeit wird zeitlich gewichtet und gegen
Mehrfachimporte und Tagesmengen gedämpft. Eine normale Priorität kann sich
weiterentwickeln; eine ausdrücklich gesetzte feste Priorität bleibt bestehen.

Nicht ausbleibende Mails, sondern belastbare Angaben beenden eine Rolle oder ein
Projekt. Gewichte dürfen sich ohne Rückfrage verändern. Ein Modell kann beim
Interpretieren trotzdem irren; Quellen, Herkunft und Korrekturen bleiben deshalb
Teil jeder belastbaren Aussage.

## Grenzen und Datenschutz

Die **lokalen Skripte** arbeiten ohne Netzwerk. Das bedeutet nicht, dass die
semantische Verarbeitung durch Codex oder Claude Code automatisch lokal bleibt.
Welche Daten an einen Modellanbieter gelangen, hängt vom gewählten Host und
dessen Einstellungen ab. ContextMe besitzt keine eigene Verschlüsselung; die
Daten liegen als Klartext vor. Betriebssystemberechtigungen, verschlüsselter
Datenträger und Unternehmensvorgaben bleiben erforderlich.

Der Skill kann nur Material lesen, das der Host tatsächlich bereitstellt oder über
autorisierte Werkzeuge erreichen kann. Er bringt keine Mail-/Drive-Zugangsdaten
und keinen eigenen Hintergrunddienst mit. Für automatisches Mitlaufen enthält
`references/INTEGRATION.md` Sitzungsregeln zum Einfügen in `AGENTS.md`/`CLAUDE.md`.
Ein dauerhafter Scheduler ist separat im Host einzurichten.

Die JSON-Scope-Filter sind **keine Zugriffssteuerung gegenüber einem Agenten, der
alle Dateien lesen darf**. Die allgemeine NOW-Datei und die Objektseiten können
berufliche und private Informationen enthalten. Für andere Systeme nur passende
Kontextpakete freigeben oder getrennte Arbeitsordner nutzen.

## Tests

```sh
python3 -m unittest discover -s contextme/tests -v
```

Die Tests überprüfen die lokale Laufzeit und Installation in temporären Ordnern.
Sie sind keine Aussage darüber, dass ein bestimmtes Modell alle Dokumente richtig
versteht. Den semantischen End-to-End-Testplan findest du in
`references/ACCEPTANCE.md`. Der tatsächlich durchgeführte Testlauf steht in
`TEST_REPORT.md`.

## Dokumentation

`SKILL.md` ist der Einstieg für den Agenten. `references/` beschreibt Datenmodell,
Materialauswertung, Gewichtung, Integration, Datenschutz, Quellen und
Abnahmeszenarien. `assets/batch.schema.json` beschreibt die strukturierte Eingabe;
die Laufzeit prüft darüber hinaus Referenzen und semantische Grundregeln.

Erstellt am 17. September 2026. Installationspfade und Skill-Aufruf wurden anhand
der offiziellen Dokumentation geprüft; siehe `references/SOURCES.md`.
