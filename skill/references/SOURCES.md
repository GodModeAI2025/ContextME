# Quellen und Designentscheidungen

Geprüft am **17. September 2026**. Die Implementierung ist eigenständig; es wurde
kein fremder Programmcode oder vollständiger kommerzieller Prompt übernommen.
Quellen liefern Anregungen und Formatvorgaben, keine Garantie der Modellqualität.

## Offizielle Format- und Installationsquellen

**OpenAI — Build skills / Codex Skills**

- https://developers.openai.com/codex/skills/
- Weiterleitung beim Abruf: https://learn.chatgpt.com/docs/build-skills

Grundlage für `SKILL.md`, progressive Bereitstellung ergänzender Dateien,
`$contextme`, `.agents/skills` sowie optionales `agents/openai.yaml`. Das Paket
verwendet diese Struktur. Ein tatsächlicher Codex-Modelllauf war in der
Erstellungsumgebung nicht verfügbar und wird nicht als getestet ausgegeben.

**Anthropic — Extend Claude with skills**

- https://code.claude.com/docs/en/skills

Grundlage für persönliche/projectbezogene `.claude/skills`-Ordner, Skill-Metadaten
und `/contextme`. Der gemeinsame Kern kommt ohne Claude-exklusive dynamische
Promptsyntax aus. Damit bleiben die gleichen Instruktionen für beide Hosts lesbar.

## Vom Benutzer genannte fachliche Anregungen

**NousResearch — Hermes Agent, Persistent Memory**

- https://github.com/NousResearch/hermes-agent/blob/main/website/docs/user-guide/features/memory.md

Die Datei wurde über den GitHub-Lesezugriff abgerufen. Übernommen wurde das
Prinzip einer kompakten aktuellen Gedächtnissicht neben umfangreicherem gespeicherten
Kontext. ContextMe implementiert weder Hermes' eigene Werkzeuge noch dessen
Sitzungssuche. Stattdessen dienen NOW und gescopete Pakete als kleine Eingangssicht;
Quellen, Behauptungen und Verlauf liegen getrennt im lokalen Ereignisspeicher.

**AI FIRST — Persönliches KI-Setup**

- https://ai-first.ai/insights/wenn-ich-heute-mit-ki-neu-starten-wuerde

Anregung für die Trennung von persönlichem Kontext, wiederkehrenden Abläufen und
verfügbaren Werkzeugen. Behauptete Zeitersparnisse wurden nicht übernommen oder
als geprüft ausgegeben.

**AI FIRST — Kontext-Interviewer**

- https://ai-first.ai/hub/agents-context-interviewer

Anregung für strukturierte Erhebung von Organisation, Rolle, Team, Prioritäten und
Kommunikation sowie das Ergänzen vorhandenen Materials. ContextMe erweitert dies
um private/Hobby-Kontexte, mehrere Rollen, automatische Ableitungen und Zeitbezüge.
Die dortige ausführliche Interview-/Freigabefolge wurde nicht kopiert.

**AI FIRST — Chief of Staff Agent**

- https://ai-first.ai/hub/agents-chief-of-staff

Anregung für die Nutzung eines aktuellen Kontextprofils vor einer Aufgabe und die
Trennung zwischen Kontext, Spezial-Skills und Datenquellen. ContextMe bleibt die
Kontextkomponente; es wird nicht selbst zum umfassenden ausführenden Büroagenten.

**KissMySkills — AI-Persönlichkeit für Claude**

- https://kissmyskills.com/de/blogs/news/ai-persona-for-claude-custom-characters-business

Nützlich ist die Unterscheidung zwischen Arbeitsmethode, Kommunikationsverhalten,
Wissen über den Benutzer und Handlungsgrenzen. ContextMe speichert dafür konkrete,
belegte Muster statt einer erfundenen Charakterrolle. Anbieter-/Tarifbehauptungen
des Artikels wurden nicht als technische Grundlage übernommen.

**Vom Benutzer eingefügtes Fabric-Muster `analyze_personality`**

Das gelieferte Muster wurde inhaltlich berücksichtigt, aber nicht eingebaut.
Konfrontative Charakterurteile, vermeintliche psychologische Allwissenheit und
unbegründete Denkzeitvorgaben sind keine belastbare Grundlage für diesen Speicher.
Verwendet wird stattdessen eine evidenzbezogene Beschreibung von Arbeits- und
Entscheidungsverhalten mit Unsicherheitsmarkierung. Keine fremde Lizenzangabe wurde
ungeprüft auf den neuen Code übertragen.

## Vom Benutzer bereitgestellte Screenshots

Inhaltlich ausgewertet: Life Library; Projects & Tasks; About Me; die umfangreiche
Attributliste; Daily Reviews; SOPs; das Schema zur Verbindung eines Second Brain
mit einem KI-System; die drei abgebildeten AI-FIRST-Links. Daraus entstand die
Abdeckungskarte in `assets/taxonomy.json`. Es wurden keine Personen auf den Bildern
identifiziert. Die Originalscreenshots werden aus Gründen der Datensparsamkeit
nicht mit diesem Softwarepaket verteilt.

## Eigene Entscheidungen dieses Pakets

Kontextabhängige Zeitreihen, ausdrückliche Pins, lokale Schreibsperre,
JSON-Ereignisformat, Scoreformeln, Reviewlogik und Klassifizierungsvertrag sind
eigene Entwurfsentscheidungen. Sie sind nicht mit einem externen Standard oder
wissenschaftlich bewiesener persönlicher Relevanz gleichzusetzen.
