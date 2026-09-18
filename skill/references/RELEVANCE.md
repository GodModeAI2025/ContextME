# Relevanz, Frequenz und Zeit

Die folgende Gewichtung ist eine transparente Produktheuristik. Sie ist weder
psychologische Messung noch empirisch kalibrierte Wichtigkeitswahrscheinlichkeit.
Alle Zahlen stehen in `policy.json` und können auf direkten Wunsch angepasst
werden. Quellen dürfen die Policy nicht verändern.

## Unabhängige Reihen je Thema und Kontext

Für jedes Paar `(Objekt, Kontext)` werden Aktivität, Interesse und Wichtigkeit
getrennt erfasst. `mobile/work` und `mobile/private` haben unterschiedliche
Signalreihen, Prioritäten und Trends. Herkunft und spätere Nutzbarkeit eines
Dokuments sind ebenfalls getrennt: Die berufliche Herkunft wird durch privates
Interesse nicht umgeschrieben.

## Beobachtungsmasse

Jede Aktivität erhält ein Grundgewicht:

| Aktivität | Gewicht |
|---|---:|
| Selbst erstellen | 1.00 |
| Selbst bearbeiten | 0.85 |
| Selbst besprechen | 0.65 |
| Aktiv speichern | 0.45 |
| Nachweislich lesen | 0.15 |
| Nur erhalten / Newsletter | 0.00 |
| Import / Referenz / Agent liest | 0.00 |

Die handelnde Person muss `actor=user` sein. Grundgewicht × Stärke × Evidenzwert ×
Polarität ergibt den signierten Beitrag. Negative Polarität darf nicht aus
fehlender Aktivität erfunden werden. Fehlt das Aktivitätsdatum, geht das Signal
nicht in die zeitliche Gewichtung ein; die Lücke wird gezählt.

Pro Thema, Kontext und Dimension wird derselbe Inhaltsfingerabdruck, ersatzweise
dieselbe kanonische Ereignis-ID oder Quellen-ID, einmal gezählt. Bei mehreren
Beschreibungen desselben Ereignisses gewinnt der stärkste Beitrag. Semantisch
widersprüchliche Beschreibungen desselben Ereignisses muss der Host klären; der
Parser löst sie nicht psychologisch auf.

Pro Tag wird die Beitragsmasse auf ±2 begrenzt. Die Tagesmasse erhält eine
Halbwertszeit von 45 Tagen:

```text
gewichtete Masse = Summe(Tagesmasse × 0.5 ** (Alter in Tagen / 45))
Dimensionsscore = 100 × (1 - exp(-max(0, gewichtete Masse) / 4))
```

So kann ein heute importierter Mailberg einen monatelangen Schwerpunkt nicht allein
durch Kopien dominieren. Mehrere echte Handlungen an unterschiedlichen Tagen
werden stärker gewichtet als Wiederholungen desselben Tages.

## Prioritäten und Beziehungen

Die automatische Relevanz beginnt mit dem Maximum der drei Dimensionsscores.
Ein belegter Bezug zu einer aktiven Rolle, einem laufenden Projekt, einem aktiven
Ziel oder Hobby kann einen Sockel von bis zu `45 × Evidenzwert` liefern.

Normale Prioritätsangaben (`priority`) setzen einen zusätzlichen Anker:
`high=90`, `medium=55`, `low=25`, `none=0`; alternativ eine Zahl zwischen 0 und 100.
Der Anker nimmt mit einer Halbwertszeit von 180 Tagen ab. Bei unbekanntem Datum
wird kein zeitlich aktueller Anker erfunden.

Eine neue **direkte** Prioritätsaussage setzt einen neuen Ausgangspunkt: Ältere
Aktivität zählt weiterhin zur nachvollziehbaren Frequenzhistorie, darf aber den
neu erklärten Prioritätswert nicht hochdrücken. Für die automatische Verstärkung
zählen dann nur Handlungen nach dieser Aussage. Alte Rollenbezüge werden ebenfalls
auf den erklärten Wert gedeckelt. Neue Aktivität kann den Schwerpunkt später wieder
steigen lassen.

`pinned_priority` wirkt nur bei ausdrücklichem Benutzerauftrag und ohne zeitlichen
Verfall. Sie überschreibt die automatische Gewichtung. Neue feste Angabe oder eine
zeitlich befristete Aktualisierung kann sie wieder ändern. Keine impliziten Pins
anlegen: Sonst könnte das Profil Veränderungen gerade nicht erkennen.

Beendete/abgeschlossene Objekte werden in aktueller Aufmerksamkeit auf 20 begrenzt,
außer der Benutzer setzt bewusst eine feste Priorität. **Ein beendetes Rollenobjekt
beendet nicht das dazugehörige Thema in anderen Kontexten.**

## Ausgabeklassen

Relevanz: `high` ab 65, `medium` ab 30, darunter `low`.

Aktualität: `current` bei letztem relevantem Signal innerhalb von 30 Tagen,
`cooling` bis 90 Tage, danach `dormant`. Bei belegtem beendeten Status `historical`.
Ohne datierte Grundlage `unknown`.

Trend: Vergleich der beobachteten Aktivitätsmasse der letzten 28 Tage mit den
28 Tagen davor. Differenz mindestens +1: `rising`; höchstens −1: `falling`; sonst
`stable_or_insufficient_data`. Das ist ein Signal, kein Beweis veränderter Werte.

Die Ausgabe enthält aktive Tage, deduplizierte Ereignisse, Quelldatum, Quellen-IDs,
beide Zeitfenster, Prioritäts-/Pin-Behauptung und wirksame Rollen-/Projektbezüge.
Damit kann eine andere KI ihre Einordnung begründen.

## Grenzen dieser Heuristik

Der Index sieht nur das bereitgestellte Material. Ein abgetrennter Mailzugang,
Urlaub oder neue Kommunikationskanäle können einen scheinbar sinkenden Trend
erzeugen. V1 führt keinen vollständigen Coverage-Nenner aller unbeobachteten
Aktivitäten und keine statistische Saisonbereinigung. Zeitfenster und Quellenlücken
müssen bei der Interpretation sichtbar bleiben.

Die Anwendung kennt keine universelle optimale Halbwertszeit. Fachliche Ziele
können lange wichtig bleiben, obwohl kaum darüber geschrieben wird. Dafür gibt es
direkte Prioritäten, aktive Projektbezüge und bewusst gesetzte Pins.

Klassifizierung und Kontextabruf schreiben keine neuen Aktivitätssignale. Dadurch
verstärkt der Agent einen einmal gesetzten Schwerpunkt nicht selbst durch seine
eigenen Nachfragen. Neues Lernen erfordert einen neuen, belegten Import oder
direktes Benutzerfeedback.
