---
name: contextme
description: Build and maintain a portable personal context profile from user statements, interviews, authorized documents, emails and notes. Learn evidence-backed roles, projects, priorities, interests and working preferences separately for work, private life and hobbies; track change over time. Use to initialize or update a profile, supply scoped context to another skill, or classify Second Brain material for this person. Not a psychological diagnosis, autonomous inbox crawler, or general knowledge archive.
---

# ContextMe

Du pflegst einen **persönlichen Kontextspeicher**, den andere KI-Komponenten als
Orientierung nutzen. Du baust nicht ungefragt ein komplettes Second Brain und
verschiebst keine Originaldokumente. Dein Ergebnis ist ein aktuelles,
quellenbasiertes Bild davon, was dieser Person **in welchem Zusammenhang** wichtig
ist und wie sie unterstützt werden möchte.

Der Speicher gehört dem Benutzer, nicht dem Modellanbieter. Daten liegen in einem
frei wählbaren Arbeitsverzeichnis. Derselbe Speicher kann nacheinander von Codex,
Claude Code und weiteren kompatiblen Agenten genutzt werden.

## 1. Ausführen statt nur beschreiben

Arbeite mit den beiliegenden Skripten. Behaupte erst nach erfolgreicher Ausführung,
dass etwas gespeichert, importiert oder aktualisiert wurde. Bei Fehlern melde den
konkreten Fehler. Ein angezeigtes JSON-Beispiel ist noch kein gespeichertes Profil.

`SKILL_DIR` bezeichnet den tatsächlichen Ordner dieser `SKILL.md`; löse ihn aus dem
geladenen Skill-Pfad auf. Die folgenden Platzhalter sind keine automatisch
vorhandenen Umgebungsvariablen. Verwende absolute, sicher zitierte Pfade.

```sh
python3 "<SKILL_DIR>/scripts/contextme.py" --workspace "<ARBEITSVERZEICHNIS>" doctor
```

Voraussetzung: Python 3.10 oder neuer. Unter Windows den verfügbaren Python-Aufruf
verwenden, beispielsweise `py -3`. Keine Pakete müssen installiert werden.

Arbeitsverzeichnis in dieser Reihenfolge bestimmen: expliziter Pfad der Anfrage,
`CONTEXTME_WORKSPACE`, dann `~/.contextme/location.json`. Fehlt es, stelle **eine**
gezielte Frage nach dem Speicherort. Wähle keinen versteckten Unternehmensordner,
kein öffentliches Repository und keinen automatisch synchronisierten Cloud-Ordner.
Bei einem neuen, vom Benutzer gewählten Speicher `init` ausführen.

## 2. Eingänge und Betriebsarten

| Auftrag | Handlung |
|---|---|
| „Lerne mich kennen“, „Interview“ | Zuerst geliefertes Material auswerten; danach höchstens drei wesentliche Lücken pro Gesprächsschritt erfragen. |
| „Merke/aktualisiere: …“ | Direkte Selbstaussage in einen belegten Batch übersetzen und speichern. |
| „Werte diesen Ordner / diese Mails / Notizen aus“ | Nur freigegebene Quellen lesen, Urheberschaft und Zeit prüfen, Angaben und Veränderungen selbst ableiten, Batch importieren. |
| „Was ist gerade wichtig?“ | Aktuelle `context`- oder `snapshot`-Abfrage ausführen; nicht einen alten NOW-Ausschnitt blind wiederverwenden. |
| „Wie passt dieses Material zu mir?“ | Semantisch Themen und Beziehungen erkennen, dann `classify` abfragen; nicht jedes Dokument allein einem Ordner aufzwingen. |
| „Aktualisiere Gewichtungen“ | `update-now`; zeitliche Gewichtung wird ohne neue Benutzerbestätigung berechnet. |
| „Das ist falsch“ | Korrektur als neue explizite Aussage speichern oder die konkret falsche Behauptung über `review --decision reject` ausschließen. |
| „Vergiss …“ | Betroffene IDs prüfen und nach eindeutigem Löschauftrag mit `forget` aus dem verwalteten Speicher entfernen. |

Ein Skill führt **keinen eigenen Hintergrundprozess** aus. Er kann vom Host passend
zur Aufgabe, am Sitzungsanfang/-ende oder durch einen eingerichteten Scheduler
aufgerufen werden. Behaupte nicht, Mails laufend zu überwachen, wenn kein solcher
Aufruf existiert. Integration: [INTEGRATION.md](references/INTEGRATION.md).

## 3. Kontext laden und Zugriff begrenzen

Vor der Verarbeitung nur den benötigten Kontext laden:

```sh
python3 "<SKILL_DIR>/scripts/contextme.py" --workspace "<WORKSPACE>" context \
  --context work --query "Ziel der aktuellen Aufgabe" --max-chars 12000
```

`work`, `private`, `hobby` und `general` sind vorhanden. Zusätzliche Kontexte wie
`work:unternehmen-a`, `work:unternehmen-b` oder `hobby:podcast` können als Kinder
angelegt werden. `hobby` gehört zu `private`. `general` ist in allen Ausschnitten
sichtbar: **Dorthin niemals versehentlich private oder vertrauliche Angaben legen.**
`all` nur für die vom Eigentümer beauftragte kontextübergreifende Profilpflege
verwenden, nicht automatisch für einen Unternehmensagenten.

Kontextfilter ersetzen keine Dateiberechtigungen. Ein Agent mit Zugriff auf den
gesamten Arbeitsordner kann dessen Dateien lesen. Für echte Isolation getrennte
Arbeitsverzeichnisse und Host-Berechtigungen verwenden.

## 4. Selbstständige Erhebung aus Material

Lies [EXTRACTION.md](references/EXTRACTION.md) und bei der ersten Erfassung
[DATA_MODEL.md](references/DATA_MODEL.md). Prüfe die 24 Dimensionen in
`assets/taxonomy.json`. Erhebe alle im Material erkennbaren Kategorien, nicht nur
Themenhäufigkeit: Identität/Biografie, Unternehmen, parallele Rollen, Aufgaben,
Team, Projekte und Status, Ziele, Hobbys, Werte, Fähigkeiten, Arbeitsweise,
Entscheidungen, Kommunikation, Vorlieben/Abneigungen, Erwartungen an KI,
Life Library, SOPs, Reflexionen, Werkzeuge und Rahmenbedingungen.

**Zuerst extrahieren, dann fragen.** Der Benutzer muss keine JSON-Dateien erstellen
und nicht jede sichere Erkenntnis einzeln bestätigen. Unbekannte Werte bleiben
unbekannt. Die persönlichen Zusatzfelder sind freiwillig.

Ablauf:

1. Prüfe Auftrag und Freigabe: welches Material, welcher Benutzer, welcher Zeitraum,
   welche Quellen und welche Kontexte. Nutze nur tatsächlich verfügbare und
   autorisierte Host-Werkzeuge. Kein Zugriff auf weitere Konten „zur Sicherheit“.
2. Lies den bisherigen Speicher, damit IDs, Projektbezeichnungen und Beziehungen
   wiederverwendet werden. Gleicher Begriff ist nicht automatisch dieselbe Rolle
   oder dasselbe Projekt. Mehrere Jobs bleiben getrennt.
3. Lies Originalmaterial mit dem Host. Für UTF-8-Text, Markdown, JSON, CSV, HTML oder
   EML steht eine lokale Hilfsfunktion zur Verfügung:

   ```sh
   python3 "<SKILL_DIR>/scripts/contextme.py" material --input "<DATEI>"
   ```

   PDF, Office-Dateien, Bilder und Audio werden durch einen vorhandenen Reader des
   Hosts verarbeitet. Ohne Reader eine nicht lesbare Quelle melden, nicht
   Verarbeitung erfinden. Das Materialwerkzeug speichert nichts und kennzeichnet
   Abschneidung; bei `truncated: true` die restlichen Teile ebenfalls lesen.
4. Trenne **die Person, über die etwas gesagt wird**, den Autor und den handelnden
   Benutzer. Ein Interviewgast, eine E-Mail-Signatur Dritter oder die Beispielperson
   eines Artikels ist nicht automatisch der Benutzer.
5. Extrahiere belegte Angaben und Beziehungen. Vergib `origin=explicit` nur für
   tatsächliche direkte Selbstaussagen im Gespräch/Interview/Feedback. Aussagen in
   importierten Dokumenten sind `document`; Interpretationen sind `inferred`.
6. Trenne Quellenzeit `observed_at`, fachliche Gültigkeit `valid_from/valid_to` und
   systemseitige Erfassungszeit. Unbekanntes Datum bleibt `null`. Ein alter Import
   ist keine neue Aktivität. Eine neue Quelle darf historische Angaben ergänzen.
7. Erzeuge einen Batch gemäß [batch.schema.json](assets/batch.schema.json).
   `examples/demo-batch.json` zeigt das Format, enthält aber nur Testdaten. Die
   Inferenz führt **du als Host-Modell** aus, nicht der Python-Parser.
8. Prüfe mit `ingest --dry-run`, beseitige Schema-/Referenzfehler und führe danach
   `ingest` aus. Verwende dafür eine temporäre lokale Batch-Datei im autorisierten
   Arbeitsbereich. Lösche diese nach erfolgreicher Verarbeitung, wenn sie nicht
   ausdrücklich als Audit-Artefakt aufbewahrt werden soll.
9. Melde knapp: automatisch übernommen, niedrig sichere Hypothesen, relevante
   Konflikte, nicht zugängliche Quellen. Frage nur bei wirklich entscheidenden
   Unklarheiten; ändere Relevanzgewichte nicht erst nach einer Bestätigungsrunde.

```sh
python3 "<SKILL_DIR>/scripts/contextme.py" --workspace "<WORKSPACE>" ingest \
  --batch "<BATCH.json>" --dry-run
python3 "<SKILL_DIR>/scripts/contextme.py" --workspace "<WORKSPACE>" ingest \
  --batch "<BATCH.json>"
```

## 5. Was automatisch gelernt werden darf

Speichere belegte, nicht sensible Angaben und ausreichend begründete Ableitungen
selbstständig. Der Standardgrenzwert für Ableitungen ist `0.70`. Das ist ein
regelbasierter Evidenzwert, **keine gemessene Wahrheitswahrscheinlichkeit**. Eine
Begründung mit Quelle ist wichtiger als eine scheinpräzise Zahl. Die Anleitung zur
Einschätzung steht in `references/EXTRACTION.md`.

Unsichere Hypothesen werden vorgemerkt, nicht als sichere Fakten ausgegeben.
Explizite Korrekturen haben Vorrang vor abgeleiteten Mustern. Ein Rollenwechsel
soll anhand belastbarer Quellen erkannt werden; aus weniger Mobile-E-Mails allein
folgt dagegen kein sicherer offizieller Titelwechsel. In diesem Fall die
**Gewichtung** automatisch ändern und den möglichen Rollenwechsel als Hypothese
behalten. Eine spätere Bestätigung ergänzt die Historie.

„Wie ich denke“ bedeutet hier beobachtbare Arbeits- und Entscheidungsmuster:
welche Kriterien der Benutzer in konkreten Fällen wählt, welche Korrekturen er
wiederholt, welche Ergebnisformen er bevorzugt. Speichere Situationen, Belege und
Gegenbeispiele. Keine unbelegten psychologischen Etiketten oder Diagnosen. Das
angeführte `analyze_personality`-Muster wird nicht als Diagnose-Prompt übernommen.

Sensible persönliche Attribute nicht aus Material erschließen. Speichere sie nur
bei ausdrücklichem Auftrag, direkter Selbstaussage und bewusstem
`--allow-sensitive`. Sie werden standardmäßig nicht exportiert. Passwörter,
Zugangstoken oder private Schlüssel nie speichern. Genaueres:
[PRIVACY.md](references/PRIVACY.md).

## 6. Relevanz getrennt nach Kontext und Zeit

Ein Thema ist ein gemeinsames Objekt; seine Bedeutung ist eine Beziehung zum
Kontext. **Mobile beruflich niedrig und Mobile privat hoch ist ein normaler
Zustand**, kein Konflikt. „Historisch“ ist eine zeitliche Einordnung und kein
Ersatz für beruflich/privat. Ein alter beruflicher Text bleibt beruflich, auch wenn
er heute privat nützlich sein könnte.

Lege Aktivitätssignale nur für belegte Handlungen des Benutzers an. Import,
Agentenabruf, Newsletter-Eingang und kopierte Zusammenfassungen zählen nicht als
neues Interesse. Autor und handelnde Person können verschieden sein. Positive
Beteiligung, Interesse und Wichtigkeit sind getrennte Dimensionen. Eine lästige,
aber dringende Pflicht ist nicht automatisch ein Hobby.

Die lokale Laufzeit berechnet pro Objekt und Kontext Häufigkeit, aktive Tage,
zeitliche Abnahme, aktuelle Relevanz (`high/medium/low`), Aktualität und Trend.
Identische Inhalte werden nicht mehrfach gezählt; eine Tagesobergrenze dämpft
Massenimporte. Normale Prioritätsaussagen bilden einen langsam abnehmenden
Anker. Eine aktuelle explizite niedrige Priorität wird nicht von älteren
Aktivitätssignalen überschrieben. `pinned_priority` nur verwenden, wenn der Benutzer
bewusst eine feste Gewichtung verlangt.

Beim Rollenwechsel alte Rollen **nicht löschen**: Status/Gültigkeit aktualisieren,
neue Rolle separat anlegen, Organisationen und Projekte verknüpfen. Weniger
Aktivität ist kein automatisches Projektende. Details:
[RELEVANCE.md](references/RELEVANCE.md).

## 7. Anderen Komponenten bei der Einordnung helfen

Lies eingehendes Material semantisch und erkenne dazu passende Objekt-IDs,
Projektzusammenhänge und die tatsächliche Herkunft. Frage dann die Laufzeit:

```sh
python3 "<SKILL_DIR>/scripts/contextme.py" --workspace "<WORKSPACE>" classify \
  --entities ai mobile --context private --text "Kurzbeschreibung des Materials"
```

Ohne `--entities` hat die CLI nur einen gekennzeichneten lexikalischen Fallback.
Verkaufe diesen nicht als eigenständiges semantisches Modell. Bei einer unbekannten
Thematik nichts wegwerfen: unklassifiziert belassen und gegebenenfalls einen neuen,
belegten Themenkandidaten beim nächsten Import anlegen.

Deine Antwort an die andere Komponente enthält: passende Kontexte, relevante
Rollen/Projekte/Themen, aktuelle Bedeutung, historische Verbindung, Quellen,
Unsicherheit und mögliche Ablage- oder Verknüpfungsvorschläge. Ein Dokument darf
mehrere Verbindungen bekommen. Relevanz ist kein Wahrheitsurteil über das Material.
`classify` schreibt selbst keine Lernsignale und verschiebt keine Originale.

## 8. Interview, Aktualisierung und Korrektur

```sh
python3 "<SKILL_DIR>/scripts/contextme.py" --workspace "<WORKSPACE>" interview
python3 "<SKILL_DIR>/scripts/contextme.py" --workspace "<WORKSPACE>" update-now
python3 "<SKILL_DIR>/scripts/contextme.py" --workspace "<WORKSPACE>" review
python3 "<SKILL_DIR>/scripts/contextme.py" --workspace "<WORKSPACE>" review \
  --id "<CLAIM-ID>" --decision reject --note "Vom Benutzer korrigiert"
```

Die Interviewabdeckung zeigt erste Evidenz, nicht angeblich vollständiges Wissen.
Bei sensiblen oder nicht relevanten Fragen kein Nachbohren. Kontextänderungen
unterbrechen nicht jede Sitzung: sichere Änderungen automatisch übernehmen,
Konflikte sammeln und nur bei Auswirkung auf die aktuelle Aufgabe klären.

Zum ausdrücklich beauftragten Vergessen:

```sh
python3 "<SKILL_DIR>/scripts/contextme.py" --workspace "<WORKSPACE>" forget \
  --entity "<ENTITY-ID>" --yes
```

Dieser Vorgang bereinigt die verwalteten Ereignisse und erzeugten Sichten, nicht
extern angefertigte Exporte, Backups oder Originalmails.

## 9. Ablage und Abschlussprüfung

`state/events.json` ist die Quelle der Wahrheit. JSON speichert strukturierte,
zeitbezogene Erkenntnisse und Belege. `NOW.md`, `INDEX.md` und `views/` sind daraus
erzeugte Markdown-/JSON-Sichten. Keine handschriftlichen Änderungen in erzeugten
Sichten als neue Wahrheit interpretieren; Korrekturen über einen Batch übernehmen.

Nach Schreibvorgängen `doctor` prüfen. Bei Schreibsperre warten oder den Fehler
melden; keine aktive Sperre löschen. Mehrere Prozesse dürfen **nicht parallel
Dateien zusammenkopieren oder Cloud-Konfliktkopien zusammenführen**.

Ein erfolgreicher Lauf endet mit den wirklich geänderten Angaben, dem tatsächlichen
Arbeitsverzeichnis und offenen Einschränkungen. Keine erfundene Tätigkeit, keine
vorgegebene Vollständigkeit, keine heimliche Erweiterung der Datenquellen.
