# Datenmodell und CLI-Vertrag

## Drei Schichten

**Material:** Originalmails, Dokumente, Gesprächsaussagen und Notizen. Die Originale
bleiben am ursprünglichen Ort. Der Skill legt keine vollständige Kopie der
Wissensbasis an. `material` erzeugt lediglich eine Lesehülle für das Host-Modell.

**Evidenzspeicher:** `state/events.json` enthält Quellenmetadaten, Objekte,
quellenbezogene Behauptungen, Beobachtungssignale und Reviewentscheidungen. Das ist
die maßgebliche, anbieterunabhängige Datenbasis. Ein Schema-Versionsfeld verhindert
das stille Einlesen unbekannter zukünftiger Formate.

**Sichten:** NOW, Index, Objektseiten und kompakte Kontextpakete werden berechnet.
Sie sind ersetzbare Ableitungen, keine zweite Quelle der Wahrheit. Unvollständige
Sichten nach einem Absturz lassen sich mit `update-now` neu erzeugen. Abfragen der
CLI lesen direkt den atomar gespeicherten Ereignisspeicher.

## Objekte und Beziehungen

Ein Objekt besteht aus `id`, `kind`, `name`, `aliases` und `sensitive`. IDs sind
stabil, klein geschrieben und keine Dateipfade. Namen und Objekttypen bleiben nach
der Anlage stabil; alternative Schreibweisen kommen als Alias hinzu. Veränderte
Anzeigenamen können als `display_name`-Behauptung dokumentiert werden.

Objekttypen:

```text
person organization role project topic goal skill preference value routine
resource task relationship decision tool constraint review hobby
```

Eine Person kann mehrere Rollen bei mehreren Unternehmen besitzen. Eine Rolle
verweist auf Organisation, Themen und Verantwortlichkeiten. Projekte können über
Rollen, Ziele und Themen mit beruflichen oder privaten Lebensbereichen verknüpft
werden. Ein gemeinsames Thema wie KI wird nicht allein wegen verschiedener
Kontexte zu zwei unterschiedlichen Themenobjekten.

Beziehungen werden ebenfalls als quellenbezogene Behauptungen modelliert. Die
folgenden Prädikate erwarten existierende Objekt-IDs als Wert oder Liste:

```text
organization role project topic goal part_of supports related_to uses
stakeholder responsible_for depends_on
```

Beispiel: `role-ai / organization / org-example / work`.

Eine Behauptung pro Kombination aus Objekt, Prädikat und Kontext wird als aktuelle
Angabe ausgewählt. Für parallele Werte eine Liste speichern, zum Beispiel
`me / role / [role-a, role-b]`. Nicht zwei konkurrierende Einzelangaben anlegen,
wenn beide gleichzeitig gelten sollen. Eine gemeinsame Quellenliste belegt die
komplette gespeicherte Liste; bei unterschiedlicher Gültigkeit separate
Rollenobjekte mit eigenen Beziehungen nutzen.

## Kontexte sind nicht Zustände

`work`, `private`, `hobby` und `general` sind Lebens-/Nutzungskontexte. Eigene
untergeordnete Kontexte können über `contexts` ergänzt werden. Ein übergeordneter
Ausschnitt schließt seine Kinder ein. Die Abfrage eines Kindes schließt dessen
Geschwister nicht ein. `general` wird allen Ausschnitten hinzugefügt.

`historical`, `completed`, `ended` oder `active` sind zeitliche bzw. sachliche
Zustände, keine alternative Kategorie zu beruflich oder privat.

## Quellen

| Feld | Bedeutung |
|---|---|
| `id` | Stabile Quellen-ID; bei inhaltlich geändertem Material eine neue Version |
| `kind` | statement, interview, feedback, email, note, calendar, file, web, chat, import |
| `author` | user, other oder unknown; Urheberschaft des Inhalts |
| `actor` | user, other oder unknown; wer die beobachtete Aktivität ausführte, standardmäßig author |
| `uri`, `title` | Wiederauffindbarkeit, keine Anweisung; bei Mischdokumenten neutral und datensparsam halten |
| `observed_at` | Tatsächliches Datum der Quelle/Aktivität, nicht das Datum des Imports |
| `activity` | create, edit, discuss, save, read, passive oder reference |
| `content_sha256` | Optionaler Inhaltsfingerabdruck gegen Mehrfachimporte |
| `canonical_id` | Optional, etwa Message-ID oder eine gemeinsam verwendete Ereignis-ID |

Quellen sind unveränderlich. Ein lokaler Import derselben Datei liefert dieselbe
Quellen-ID. Bei neuen Inhalten muss die Quelle neu versioniert werden. Für das
Lesen eines fremden Artikels kann `author=other`, `actor=user`, `activity=read`
korrekt sein; Empfang allein ist `passive`.

Ein Dokument kann mehrere unterschiedliche Ereignisse beschreiben. Dann pro
belegtem Ereignis eine eigene Quellenscheibe mit genauem Locator verwenden und den
Originalverweis erhalten. Nicht denselben kompletten Inhaltsfingerabdruck für
wirklich unabhängige Ereignisse verwenden: Er würde sie absichtlich deduplizieren.

## Behauptungen (`claims`)

Pflichtfelder sind `subject`, `predicate`, `value`, `origin`, `confidence` und eine
nicht leere `sources`-Liste. `context` ist standardmäßig `general`, sollte aber
**immer bewusst angegeben werden**. Weitere Felder sind `id`, `evidence`,
`locator`, `valid_from`, `valid_to`, `sensitive`.

`explicit` steht nur für direkte Aussagen des Benutzers in statement/interview/
feedback/chat mit `author=user`. Ein importierter Text wird dadurch nicht zur
autorisierten Benutzeranweisung. `document` bedeutet unmittelbar dokumentierte
Angabe; `inferred` eine Interpretation mit begrenzter Sicherheit.

`confidence` ist ein heuristischer Evidenzwert von 0 bis 1. Die Laufzeit übernimmt
nicht sensible Angaben ab dem eingestellten Grenzwert; explizite Aussagen werden
als Selbstaussage übernommen. Das ist keine externe Verifikation der Wahrheit.

Zeitfelder sind ISO-8601. `valid_to` ist exklusiv. Ohne `valid_from` dient die
späteste bekannte Quellenbeobachtung als `effective_at`. Ohne bekanntes Datum ist
die zeitliche Position unklar. Eine spätere Erfassung verschiebt historische
Ereignisse nicht automatisch in die Gegenwart.

Bei der aktuellen Auswahl gilt direkte Aussage vor Dokument vor Interpretation,
danach fachliche Zeit. Neuere indirekte Widersprüche werden sichtbar, ohne eine
direkte Aussage heimlich umzuschreiben. Eine vom Benutzer ausdrücklich akzeptierte
Reviewentscheidung kann einen Kandidaten autorisieren. Gleiche direkte Aussagen
mit gleichem Zeitstempel werden in Eingangsreihenfolge ausgewählt; bei tatsächlicher
Unklarheit muss der Host nachfragen statt eine willkürliche Reihenfolge zu erzeugen.

`--at` ist eine **rückblickende fachliche Sicht mit dem heute gespeicherten Wissen**,
nicht eine exakte Simulation dessen, was das System damals bereits wusste.
Spätere Korrekturen und Reviews können die rückblickende Sicht beeinflussen.

Empfohlene Statuswerte: `idea`, `planning`, `active`, `in_progress`, `blocked`,
`paused`, `completed`, `cancelled`, `ended`, `historical`, `unknown`.
Andere Attribute sind über sinnvolle Prädikate erweiterbar. Verbindliche
Verknüpfungsprädikate und spezielle Prioritätsprädikate siehe oben bzw. unten.

## Signale (`signals`)

Signale sind keine Identitätsbehauptungen. Sie beschreiben beobachtete Beteiligung
an einem Thema in einem Kontext. Sie benötigen `subject`, `context`, `source`;
optional `dimension`, `polarity`, `strength`, `confidence`, `reason`.

`dimension` trennt `activity`, `interest` und `importance`. Eine Handlung kann
mehrere Dimensionen stützen, aber Interesse ist nur bei inhaltlicher Evidenz zu
setzen. `polarity=-1` steht für ein beobachtetes negatives Signal innerhalb seiner
Dimension. Es darf nicht aus Schweigen abgeleitet werden. Ein direkter
Widerspruch des Benutzers wird zusätzlich als explizite Korrektur gespeichert.

Mehrere Beobachtungen desselben Inhaltsfingerabdrucks zählen innerhalb derselben
Objekt-Kontext-Dimension einmal. Der Fingerabdruck hat Vorrang vor `canonical_id`,
sonst dient die Quellen-ID. Identische Inhalte und veränderte Exporte ohne
übereinstimmende IDs können nicht semantisch durch Python dedupliziert werden;
diese Zuordnung übernimmt der Host.

## Spezielle Prioritätsattribute

`priority` ist ein zeitlich abnehmender Anker; `pinned_priority` eine bewusst vom
Benutzer festgesetzte Priorität. Werte: `none`, `low`, `medium`, `high` oder 0–100.
`interest` hält ein ausdrücklich/dokumentarisch beschriebenes Interesse getrennt
fest. Eine feste Priorität lässt sich durch eine neue Angabe ersetzen oder durch
eine gültig bis zu einem Datum reichende Aktualisierung beenden.

Es gibt **keine automatische Löschung** bei sinkender Relevanz. Frühere Kompetenz,
Vertrautheit und damalige Rollen bleiben als belegte Informationen erhalten.

## CLI-Übersicht

Alle Befehle liefern JSON. `--workspace` steht vor dem Unterbefehl.

| Befehl | Zweck |
|---|---|
| `init` | Arbeitsordner initialisieren, bestehende Daten nicht überschreiben |
| `material --input DATEI` | Text/EML/HTML für den Host lesen, ohne etwas zu speichern |
| `ingest --batch DATEI [--dry-run]` | Strukturierte Erkenntnisse prüfen und übernehmen |
| `snapshot --context KONTEXT` | Aktuelle ausführliche Sicht |
| `context --context KONTEXT --query TEXT --max-chars N` | Begrenztes Kontextpaket |
| `classify --entities ID ... --context KONTEXT` | Zuordnung für vom Host semantisch erkannte Objekte |
| `interview` | Themenabdeckung und bis zu drei Fragen |
| `update-now` | Sichten und zeitliche Gewichtung aktualisieren |
| `review` | Vorgemerkte Angaben und Widersprüche anzeigen |
| `review --id ID --decision accept/reject` | Konkrete Prüfaussage annehmen/ablehnen |
| `forget --entity ID --yes` | Objekt samt referenzierten Angaben entfernen |
| `forget --source ID --yes` | Quelle samt davon abhängigen Angaben entfernen |
| `doctor` | Struktur und Referenzen prüfen |

`context --max-chars` begrenzt die kompakte JSON-Darstellung, nicht Tokens oder die
zusätzlichen Leerzeichen einer hübsch eingerückten CLI-Ausgabe. Der Host kann die
Antwort erneut kompakt serialisieren. `snapshot` und `classify` sind unbeschränkt
und sollten für große Speicher gezielt gescopet werden.

Die Python-Laufzeit verwendet eine standardbibliotheksbasierte Validierung. Das
mitgelieferte JSON Schema dient zusätzlich Editoren und anderen Integrationen.
