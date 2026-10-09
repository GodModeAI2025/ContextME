# Den Kontextspeicher täglich nutzen

## Finden und lesen

Die Beispiele verwenden den tatsächlichen installierten Skill-Pfad. Einmal mit
`python3 "<SKILL_DIR>/scripts/contextme.py" where` den absoluten Datenpfad prüfen.
`resolved_from` zeigt `explicit` (`--workspace`), `environment`
(`CONTEXTME_WORKSPACE`) oder `pointer` (`~/.contextme/location.json`). `where` liest
nur und legt keinen Speicher an. Ohne Auswahl gibt es einen Fehler statt einer
heimlichen Standardablage.

Im Arbeitsordner `NOW.md` für aktuelle Prioritäten und `INDEX.md` für die
Objektseiten unter `views/<kind>/<id>.md` öffnen. Für den aktuellen Stand
`update-now` ausführen; `snapshot` gibt eine aktuelle JSON-Sicht aus und schreibt
keine Markdown-Seiten. Zum Weitergeben an andere Agenten `context --context work`
(oder den passenden Kontext) verwenden. Die Gesamtsichten sind für den Eigentümer
bestimmt und können berufliche und private Angaben enthalten.

## Einen Import prüfen

`ingest --batch "<BATCH.json>" --dry-run` prüft vor dem Schreiben. Der Bericht hat
Zähler sowie `items`: Typ, ID, Status (`added`, `duplicate`, `unused_source`), bei
Claims außerdem Subjekt, Prädikat, Quellen-IDs und aktueller Prüfstatus
(`accepted`, `pending`, `rejected`). Ein Duplikat wird nicht neu gespeichert und
verstärkt keine Gewichtung; ein bereits abgelehnter Claim bleibt abgelehnt.
`accepted`/`pending` sind die anfängliche Einstufung der eingesandten Claims,
einschließlich Duplikaten; für deren heutigen Prüfstatus `items.disposition` lesen.
`added` zählt erzeugte Ereignisse vor der Entfernung ungenutzter neuer Quellen.
`unused_source` bedeutet: Die neue Quelle hatte am Ende keine Claim-/Signalreferenz
und wurde nicht im Speicher behalten. `skipped_sensitive` nennt ausgeschlossene
Angaben ohne sensible Werte.

Nach dem echten Import den Bericht im Host zusammenfassen und bei Bedarf als
autorisiertes Audit-Artefakt behalten. Die Laufzeit speichert ihn nicht dauerhaft.
Mit `review` offene Hypothesen und Konflikte prüfen. Schematisch ungültige Batches
scheitern atomar: Es wird kein Teilimport gespeichert. Material, das der Host vor
`ingest` auslässt, kann der Speicher nicht anzeigen; der Host muss solche
Auslassungen mit Grund in seinem Bericht nennen.

## Eine Angabe korrigieren

1. In der Objektseite die `claim-…`-ID finden, dann Herkunft nachlesen:
   `python3 "<SKILL_DIR>/scripts/contextme.py" show "<CLAIM-ID>"`.
2. Die falsche Aussage ausschließen:
   `python3 "<SKILL_DIR>/scripts/contextme.py" review --id "<CLAIM-ID>" --decision reject --note "Vom Benutzer korrigiert"`.
3. Die richtige Aussage als neuen Claim mit neuer ID und einer neuen direkten
   Benutzerquelle importieren (`origin: explicit`, mit tatsächlichem Quelldatum).
   Ein abgelehnter Claim wird durch bloßen Wiederimport nicht wieder angenommen.
4. `update-now` und `doctor` ausführen und die erzeugte Objektseite erneut lesen.

Bestehende Entity-IDs, Namen und Typen sind unveränderlich. Bei einem Tippfehler
dieselbe ID und denselben ursprünglichen Namen/Typ behalten, einen Alias ergänzen
oder eine `display_name`-Aussage speichern. Letztere ist eine normale Aussage;
sie ersetzt aktuell nicht die Überschriften der erzeugten Sichten. Bei einem
tatsächlich anderen Objekt eine neue Entity anlegen. Erzeugte Markdown-Seiten
nicht als Datenquelle bearbeiten: Sie werden beim nächsten Schreiben neu erzeugt.

## Quellen später nachprüfen

`show "<CLAIM-ID>"` liefert den Claim einschließlich Evidenz und Locator, die Entity,
den heutigen Prüfstatus, den letzten Review und vollständige Source-Datensätze:
Titel, URI, Canonical-ID, Quellezeit, Autor, Handelnder und gegebenenfalls Hash.
Es funktioniert auch für historische, vorgemerkte und abgelehnte Claims. Die URI
mit einem ausdrücklich autorisierten Reader öffnen; `show` lädt keine externe
Quelle herunter. Fehlende Locator/URI bleiben fehlend. Für sensible Claims ist
`--include-sensitive` nach ausdrücklicher Freigabe erforderlich. Vergessene
Claims sind nicht mehr abrufbar.
