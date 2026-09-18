# Testbericht — ContextMe 1.0.0

Datum: **17. September 2026**. Dies sind tatsächlich ausgeführte lokale Prüfungen,
keine behaupteten Tests in einem Codex- oder Claude-Code-Modell.

## Umgebung

- Python: `3.13.5` (`CPython`).
- Betriebssystem der Prüfung: `Linux` / `x86_64`.
- Runtime: ausschließlich Python-Standardbibliothek. Keine Modelle, Konten,
  Zugangsdaten oder Netzwerkdienste im Laufzeittest.
- Mindestversion laut verwendeter Syntax/API: Python 3.10. Ältere unterstützte
  Python-Versionen und echte macOS-/Windows-Installationen wurden nicht separat ausgeführt.

## Ergebnis

**55 automatisierte Tests erfolgreich, 0 Fehler.** Letzter Lauf: 1,671 Sekunden.
Der unveränderte Testlauf steht in [tests/last-run.txt](tests/last-run.txt).

Geprüft wurden getrennte berufliche/private Relevanz, historische Rollen,
automatisches Abklingen, direkte Korrekturen, dauerhaft fixierte Prioritäten,
Quellenzeit und fachliche Gültigkeit, Duplikatvermeidung, Tagesdämpfung,
Urheber/Handelnder, passive Materialflut, unsichere und abgelehnte Hypothesen,
kontextbegrenzte Ausgabe, Metadatenbegrenzung, explizite sensible Angaben,
Vergessen, Pfadsicherheit, JSON-Validierung, Dateileser, Budget und Schreibsperre.

## Zusätzlicher Installationstest

Der Installer wurde in einem temporären Test-Home aufgerufen. Beide Zielordner
wurden angelegt. Anschließend wurde **die installierte Kopie** des Python-Skripts
verwendet, mit Leerzeichen in Home- und Workspace-Pfaden.

```json
{
  "installed_targets": 2,
  "demo_claims_accepted": 19,
  "classification": "multi_context",
  "mobile_work": "low",
  "mobile_private": "high",
  "doctor_ok": true,
  "paths_with_spaces": true
}
```

Danach wurden ein begrenztes berufliches Kontextpaket und aktualisierte
Markdown-Sichten erzeugt; `doctor` meldete einen konsistenten Speicher.
Die Daten waren fiktiv und der temporäre Speicher wurde wieder entfernt.

## Paket- und Formatprüfung

Alle JSON-Dateien wurden geparst. `batch.schema.json` wurde mit einem
JSON-Schema-2020-12-Validator geprüft; `examples/demo-batch.json` entspricht dem
Schema. Der Validator wurde nur beim Paketbau genutzt und ist **keine** zusätzliche
Installation für Benutzer. SKILL-Frontmatter und `agents/openai.yaml` wurden
geparst. Der gemeinsame Skill hat Namen und Beschreibung gemäß Paketformat.

## Nicht durch diesen Bericht belegt

Ein tatsächlicher semantischer Durchlauf in Codex oder Claude Code wurde hier
**nicht** ausgeführt. Insbesondere nicht geprüft: Interpretation beliebiger Mails,
PDF-/Office-/Audio-Reader eines Hosts, echte Account-Anbindungen, Hintergrund-
Scheduler, macOS-/Windows-Dateirechte und Langzeitverhalten in sehr großen Profilen.
Auch sichere Erkennung beliebiger sensibler Inhalte oder Prompt-Injection-Muster
wird nicht garantiert. Dateibasierte Schutzmaßnahmen ersetzen keine Host-Isolation.

Die offene Host-Abnahme ist konkret in
[references/ACCEPTANCE.md](references/ACCEPTANCE.md) beschrieben. Der Skill enthält
die nötigen Arbeitsanweisungen; die Tests zeigen die Funktion der lokalen Logik,
nicht die Unfehlbarkeit eines extrahierenden Modells.

## Wiederholen

Im übergeordneten Ordner des entpackten Pakets:

```sh
python3 -m unittest discover -s contextme/tests -v
```
