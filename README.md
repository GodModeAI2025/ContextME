# ContextMe

**Ein portabler, persönlicher Kontextspeicher für KI-Agenten.**
Ein Skill für [Claude Code](https://claude.com/claude-code) und Codex, der lernt,
wer du bist, woran du arbeitest und wie du unterstützt werden willst — getrennt
nach **beruflich**, **privat** und **Hobby**, belegt mit Quellen, nachvollziehbar
über die Zeit.

[![Tests](https://github.com/GodModeAI2025/ContextME/actions/workflows/tests.yml/badge.svg)](https://github.com/GodModeAI2025/ContextME/actions/workflows/tests.yml)
![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)
![License](https://img.shields.io/badge/license-Apache--2.0-lightgrey)

→ **[Landingpage ansehen](https://godmodeai2025.github.io/ContextME/)**

---

## Wofür das gedacht ist

Jede neue Sitzung mit einem KI-Agenten beginnt bei null. Du erklärst wieder deine
Rolle, dein aktuelles Projekt, deine Arbeitsweise, deine No-Gos. Der Agent rät den
Rest — und liegt daneben. Am Ende der Sitzung ist alles wieder weg.

Die üblichen Gegenmittel greifen zu kurz:

| Ansatz | Problem |
|---|---|
| Ein langer Prompt in `CLAUDE.md` | Statisch. Veraltet still. Kennt keine Quellen und keine Historie. |
| Anbieter-Memory | Gehört dem Anbieter. Nicht portabel. Nicht prüfbar. Kein Kontextschnitt. |
| Ein komplettes Second Brain | Ein Dokumentenarchiv beantwortet nicht, *was dir gerade wichtig ist*. |

ContextMe löst genau diese Lücke. Es ist **kein** Wissensarchiv, sondern ein
Modell deiner **Relevanz**: welche Rollen aktuell sind, welche Projekte laufen,
welche Themen beruflich hoch und privat niedrig wiegen — oder umgekehrt.

### Das zentrale Beispiel

„Mobile" existiert als Thema **einmal**. Seine Bedeutung ist eine Beziehung zum
Kontext, nicht eine Eigenschaft des Themas:

| Thema | Beruflich | Privat |
|---|---|---|
| Mobile | niedrig | **hoch** |
| KI | **hoch** | **hoch** |

Das ist kein Widerspruch, den man auflösen muss — das ist der Normalzustand eines
Menschen. Ein Agent, der das nicht trennt, gibt dir private Antworten im Meeting
und berufliche Antworten am Wochenende.

Wechselst du die Rolle, wird die alte Rolle **historisch, nicht gelöscht**. Ein
altes berufliches Dokument bleibt beruflicher Herkunft, auch wenn sein Inhalt
heute privat nützlich ist.

### Wofür du es konkret benutzt

- **Kontext an einen Agenten geben** — ein begrenztes, kontextgeschnittenes
  JSON-Paket statt „kopiere mein ganzes Leben in den Prompt".
- **Profil aus Material erheben** — du gibst Notizen, Transkripte, freigegebene
  Mails; der Agent extrahiert Rollen, Projekte, Ziele, Arbeitsweisen selbst.
  Du schreibst **kein** JSON.
- **Fremdes Material einordnen** — „wie passt dieses Dokument zu mir?" liefert
  passende Kontexte, Projekte und Themen für ein separates Second Brain.
- **Veränderung verfolgen** — Rollenwechsel, abklingende Projekte, neue
  Schwerpunkte, mit Quelle und Zeitpunkt.
- **Korrigieren und vergessen** — explizite Korrektur schlägt jede Ableitung;
  `forget` entfernt eine Entität wirklich aus dem verwalteten Speicher.

### Wofür es ausdrücklich **nicht** gedacht ist

Keine psychologische Diagnose. Kein autonomer Postfach-Crawler. Kein allgemeines
Wissensarchiv. Kein Hintergrunddienst — ein Skill läuft nur, wenn der Host ihn
aufruft.

---

## Wie es funktioniert

Die Arbeit ist bewusst zweigeteilt:

```
┌──────────────────────────────┐        ┌──────────────────────────────┐
│  Host-Modell                 │        │  Lokale Python-Laufzeit      │
│  (Claude Code / Codex)       │        │  (Standardbibliothek)        │
├──────────────────────────────┤        ├──────────────────────────────┤
│  • Material lesen            │ Batch  │  • Schema & Referenzen       │
│  • Semantik verstehen        │ ─────► │  • Historie & Gültigkeit     │
│  • Angaben ableiten          │        │  • Gewichtung & Trend        │
│  • Quelle & Herkunft trennen │ ◄───── │  • Sichten erzeugen          │
└──────────────────────────────┘ Kontext└──────────────────────────────┘
```

Das Modell interpretiert, Python speichert, validiert und rechnet. Deshalb ist
die Gewichtung reproduzierbar und die Herkunft jeder Angabe nachvollziehbar —
auch wenn das Modell sich einmal irrt.

### Vier Prinzipien

1. **Alles ist belegt.** Jede Angabe trägt Quelle, Zeitpunkt und Herkunft:
   `explicit` (direkte Selbstaussage), `document` (aus importiertem Material),
   `inferred` (Interpretation). Eine Aussage in einem Dokument wird nie zu einer
   Selbstaussage hochgestuft.
2. **Relevanz ist zeit- und kontextabhängig.** Häufigkeit wird zeitlich
   abklingend gewichtet, Massenimporte werden gedämpft, Duplikate zählen nicht
   doppelt. Ein Agentenabruf ist **keine** Aktivität von dir.
3. **Explizit schlägt abgeleitet.** Eine Korrektur setzt sich gegen jedes
   statistische Muster durch. Ableitungen unter dem Grenzwert `0.70` landen in
   einer Prüfliste statt im Profil.
4. **Der Speicher gehört dir.** Klartext-JSON in einem Ordner deiner Wahl. Kein
   Konto, kein Dienst, kein API-Schlüssel. Du kannst ihn lesen, sichern, löschen.

### Die 24 Erhebungsdimensionen

Identität · Unternehmen · Rollen · Team · Projekte · Aufgaben · Ziele ·
Interessen · Hobbys · Werte · Stärken · Arbeitsweise · Entscheidungen ·
Kommunikation · Vorlieben · Abneigungen · Erwartungen an die KI · Life Library ·
Routinen/SOPs · Reflexionen · Werkzeuge · Rahmenbedingungen · *persönlicher
Kontext (optional)* · *Selbstbeschreibung (optional)*

Alle sind ab dem ersten Start vorhanden. Es ist **kein** Interview mit 60
Pflichtfragen: Was im Material steht, wird erhoben; was fehlt, bleibt als
unbekannt gekennzeichnet.

---

## Installation

Voraussetzung: **Python 3.10+** und ein eingerichtetes Claude Code oder Codex mit
Datei- und Ausführungszugriff. Keine Pakete, keine Dienste, keine Schlüssel.

```sh
git clone https://github.com/GodModeAI2025/ContextME.git
cd ContextME
python3 skill/scripts/install.py --target both --workspace "$HOME/ContextMe"
```

Windows (PowerShell):

```powershell
py -3 skill\scripts\install.py --target both --workspace "$HOME\ContextMe"
```

Der Installer kopiert den Skill nach `~/.claude/skills/contextme` (Claude Code)
und `~/.agents/skills/contextme` (Codex), initialisiert den privaten Arbeitsordner
und hinterlegt dessen Pfad in `~/.contextme/location.json`. Bestehende
Installationen werden ohne `--replace` nicht überschrieben; mit `--replace` wird
eine Sicherung außerhalb der Skill-Suchpfade angelegt.

Projektlokal statt im Home-Verzeichnis:

```sh
python3 skill/scripts/install.py --target both --project "/Pfad/zum/Projekt"
```

> **Der Arbeitsordner gehört nicht ins Repository.** Wähle einen geschützten
> lokalen Pfad — keinen automatisch synchronisierten Cloud-Ordner und kein
> öffentliches Repo. Dieses Repository enthält bewusst **nur den Skill**, keine
> echten Profildaten.

Danach den Host neu starten und in einer neuen Sitzung aufrufen:

```text
/contextme   Nutze meinen eingerichteten Arbeitsordner. Erhebe mein Kontextprofil
             zuerst aus dem Material, das ich dir gebe, und frage nur wesentliche
             Lücken nach.
```

In Codex entsprechend `$contextme`.

## Einmal ausprobieren

Mit fiktiven Demo-Daten, in einem separaten Ordner — nicht in deinem echten Profil:

```sh
python3 skill/scripts/contextme.py --workspace ./contextme-demo init
python3 skill/scripts/contextme.py --workspace ./contextme-demo ingest --batch skill/examples/demo-batch.json
python3 skill/scripts/contextme.py --workspace ./contextme-demo classify --text "Mobile und KI" --at 2026-09-17T12:00:00Z
python3 skill/scripts/contextme.py --workspace ./contextme-demo doctor
```

Das feste `--at` macht die Demo reproduzierbar; im Alltag weglassen.
`examples/demo-batch.json` beschreibt eine **fiktive Person in einem fiktiven
Unternehmen** und wird nie automatisch in einen echten Arbeitsordner importiert.

## Befehle

| Befehl | Zweck |
|---|---|
| `init` | Neuen Arbeitsordner anlegen |
| `doctor` | Speicher auf Konsistenz prüfen |
| `material --input` | Lokale Datei lesen (Text, Markdown, JSON, CSV, HTML, EML) — speichert nichts |
| `ingest --batch [--dry-run]` | Belegten Batch validieren und übernehmen |
| `snapshot --context` | Aktuelle Sicht für einen Kontext |
| `context --context --query` | Begrenztes Kontextpaket für einen anderen Agenten |
| `classify --text [--entities]` | Material einordnen — **lesend**, erzeugt kein Lernsignal |
| `interview` | Offene Lücken je Dimension zeigen |
| `update-now` | Gewichtungen und Sichten neu berechnen |
| `review [--id --decision]` | Unsichere Hypothesen annehmen oder ablehnen |
| `forget --entity --yes` | Entität aus dem verwalteten Speicher entfernen |

## Arbeitsordner

```text
ContextMe/
├── policy.json               # Einstellbare Gewichtungsregeln und Kontexte
├── state/events.json         # Maßgeblicher Ereignisspeicher mit Quellen
├── NOW.md                    # Kompakte aktuelle Sicht
├── INDEX.md                  # Einstieg in die Objektseiten
└── views/                    # Erzeugt — nicht manuell editieren
    ├── CONTEXT.json          # Strukturierte Sicht
    ├── FREQUENCY.json        # Häufigkeit, Aktivität, Trend je Kontext
    ├── REVIEW.json           # Unsichere Hypothesen und Widersprüche
    ├── COVERAGE.md           # Welche Dimensionen belegt sind
    ├── scopes/work/NOW.md    # Beruflicher Ausschnitt
    ├── scopes/private/NOW.md # Privater Ausschnitt inkl. Hobby
    └── role|project|topic/*.md
```

`state/events.json` ist die Quelle der Wahrheit; alles andere wird daraus erzeugt.
Handschriftliche Änderungen in `views/` gelten nicht als neue Wahrheit —
Korrekturen laufen über einen Batch. Atomarer Austausch und eine lokale
Schreibsperre schützen vor parallelen Schreibern; ein verteiltes
Mehrbenutzersystem ist das bewusst nicht.

## Schnittstelle für andere Skills

```sh
# Kontextpaket für einen Agenten — begrenzt, mit Quellen und Unsicherheit
python3 skill/scripts/contextme.py --workspace "$HOME/ContextMe" context \
  --context work --query "Aktuelle Rolle und Prioritäten" --max-chars 12000

# Material einordnen — liest nur, verstärkt kein Interesse
python3 skill/scripts/contextme.py --workspace "$HOME/ContextMe" classify \
  --entities ai mobile --context private --text "Zusammenfassung des Materials"
```

Kontexte: `work`, `private`, `hobby`, `general`. Unterkontexte wie
`work:firma-a` oder `hobby:podcast` sind möglich; `hobby` gehört zu `private`.

> `general` ist in **allen** Ausschnitten sichtbar. Dorthin gehört nur, was du
> für jeden Kontext freigegeben hast — nie Vertrauliches.

Für dauerhaftes Mitlaufen enthält
[`skill/references/INTEGRATION.md`](skill/references/INTEGRATION.md) einen
Regelblock für `CLAUDE.md` / `AGENTS.md`.

## Grenzen und Datenschutz

Ehrlich statt beruhigend:

- Die **lokalen Skripte** arbeiten ohne Netzwerk. Das heißt **nicht**, dass die
  semantische Verarbeitung lokal bleibt — was beim Modellanbieter landet,
  entscheidet der gewählte Host und dessen Einstellungen.
- ContextMe hat **keine eigene Verschlüsselung**. Die Daten liegen als Klartext
  vor. Dateiberechtigungen, verschlüsselter Datenträger und
  Unternehmensvorgaben bleiben erforderlich.
- Die Kontextfilter sind **keine Zugriffssteuerung** gegenüber einem Agenten, der
  ohnehin alle Dateien lesen darf. Für echte Isolation: getrennte Arbeitsordner
  und Host-Berechtigungen.
- Der Skill liest nur, was der Host bereitstellt. Er bringt keine Mail- oder
  Drive-Zugangsdaten und keinen Hintergrunddienst mit.
- Sensible persönliche Attribute werden **nicht aus Material erschlossen** — nur
  bei ausdrücklichem Auftrag, direkter Selbstaussage und bewusstem
  `--allow-sensitive`. Sie werden standardmäßig nicht exportiert.
- Passwörter, Zugangstoken und private Schlüssel werden nie gespeichert.

Details: [`skill/references/PRIVACY.md`](skill/references/PRIVACY.md).

## Tests

```sh
python3 -m unittest discover -s skill/tests
```

55 lokale Tests prüfen getrennte berufliche/private Relevanz, historische Rollen,
Abklingen, Korrekturen, fixierte Prioritäten, Quellenzeit und Gültigkeit,
Duplikatvermeidung, Tagesdämpfung, Urheber/Handelnder, unsichere und abgelehnte
Hypothesen, kontextbegrenzte Ausgabe, explizite sensible Angaben, Vergessen,
Pfadsicherheit, JSON-Validierung, Dateileser, Budget und Schreibsperre.

Sie sagen nichts darüber aus, ob ein bestimmtes Modell jedes Dokument richtig
versteht. Der semantische Abnahmeplan steht in
[`skill/references/ACCEPTANCE.md`](skill/references/ACCEPTANCE.md), der
durchgeführte Lauf in [`skill/TEST_REPORT.md`](skill/TEST_REPORT.md).

## Repository

```text
README.md                  Dieses Dokument
docs/index.html            Landingpage (GitHub Pages)
skill/                     Der Skill — unverändert installierbar
├── SKILL.md               Einstieg für den Agenten
├── README.md              Skill-eigene Dokumentation
├── scripts/               contextme.py (Laufzeit) · install.py
├── references/            Datenmodell, Extraktion, Relevanz,
│                          Integration, Datenschutz, Abnahme, Quellen
├── assets/                Batch-Schema, Standard-Policy, Taxonomie
├── examples/              Fiktive Demo-Daten
├── tests/                 55 Tests
└── MANIFEST.sha256.json   Integritätsliste aller Skill-Dateien
```

Manifest prüfen:

```sh
cd skill && python3 -c "import json,hashlib,pathlib; m=json.load(open('MANIFEST.sha256.json')); print([p for p,h in m.items() if hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()!=h] or 'ok')"
```

## Lizenz

[Apache-2.0](LICENSE)
