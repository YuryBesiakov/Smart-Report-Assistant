# Smart Report Assistant

Der **Smart Report Assistant** ist ein kleines Python‑Projekt, das den Upload einer strukturierten CSV‑Datei erlaubt, daraus automatisch Visualisierungen erstellt und diese zusammen mit einer automatisch generierten Zusammenfassung in einem HTML‑Bericht präsentiert. Das Projekt ist als einfaches Showcase für Vorstellungsgespräche gedacht, um den Umgang mit Daten, Visualisierung und Textgenerierung zu demonstrieren.

## Features

- **Datei‑Upload**: Über die Weboberfläche können Anwender eine CSV‑Datei hochladen, die Metriken wie `Kundenzahlen`, `Risikoscore`, `Verluste` und eine Kategorie (`RiskCategory`) enthält.
- **Automatische Visualisierung**:
  - *Balkendiagramm*: Zeigt die Top‑Risiken nach Kategorie an. Dafür werden die Risikowerte pro Kategorie aggregiert und die Kategorien nach absteigender Risikosumme sortiert.
  - *Liniendiagramm*: Zeigt den zeitlichen Verlauf des durchschnittlichen Risikoscores über die Monate. Dazu werden die Daten nach Datum gruppiert und der mittlere Wert pro Monat berechnet.
- **GPT‑ähnliche Zusammenfassung**: Im MVP nutzt der Report Generator einfache statistische Kennzahlen (Maximum, Mittelwert, Trends), um Highlights und Auffälligkeiten textuell zusammenzufassen. Optional lassen sich auch Empfehlungen ausgeben, wenn etwa ein signifikanter Anstieg in einem Quartal festgestellt wird. Der Code ist modular aufgebaut, sodass bei Vorhandensein eines API‑Keys problemlos eine externe Sprachmodell‑API eingebunden werden kann.
- **HTML‑Bericht**: Aus Daten, Plots und Text wird ein HTML‑Report mit Jinja2 erstellt. Dieser lässt sich direkt im Browser anzeigen. Für den Export als PDF kann ein Tool wie `pdfkit` nachinstalliert und integriert werden (siehe Hinweise in `requirements.txt`).

## Projektstruktur

```
smart-report-assistant/
├── README.md                # Diese Projektbeschreibung
├── app/
│   ├── main.py              # Flask‑App zum Upload und zur Anzeige des Berichts
│   ├── report_generator.py  # Logik für Visualisierung und Zusammenfassung
│   ├── templates/
│   │   └── report.html      # Jinja2‑Template für den HTML‑Report
│   └── static/
│       └── plots/           # In dieser Unterordner werden generierte Diagramme gespeichert
├── data/
│   └── beispiel.csv         # Beispiel‑Datensatz für Tests
├── requirements.txt         # Liste der Python‑Abhängigkeiten
└── .gitignore               # Git‑Ignorierliste
```

## Schnellstart

1. **Abhängigkeiten installieren**

   ```bash
   cd smart-report-assistant
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Server starten**

   ```bash
   python app/main.py
   ```

   oder mit Flask‑Umgebungsvariablen:

   ```bash
   export FLASK_APP=app/main.py
   flask run
   ```

3. **Anwendung im Browser öffnen**

   Nach dem Start läuft die Web‑App auf `http://localhost:5000`. Dort kann eine CSV hochgeladen werden; anschließend erscheint der generierte Bericht.

## Beispiel‑Datensatz

Die Datei `data/beispiel.csv` enthält fiktive Daten über mehrere Monate und Risikokategorien. Sie besteht aus den Spalten `Date`, `Kundenzahlen`, `Risikoscore`, `Verluste` und `RiskCategory`. Die Werte wurden so gewählt, dass sie bei der Generierung des Berichts aussagekräftige Diagramme und eine sinnvolle Zusammenfassung liefern.

## Hinweise zur Erweiterung

- **Integration externer Sprachmodelle**: Die Funktion zur Textzusammenfassung ist bewusst einfach gehalten. Wer einen API‑Key für GPT‑Modelle besitzt, kann in `report_generator.py` die Funktion `generate_summary_gpt` erweitern, um echte KI‑gestützte Analysen durchzuführen.
- **PDF‑Export**: Für den Export des HTML‑Berichts als PDF kann eine Bibliothek wie `pdfkit` oder `WeasyPrint` eingebunden werden. Bitte beachten, dass dafür ein zusätzliches Systempaket (z. B. `wkhtmltopdf`) notwendig sein kann.
- **Weiterführende Visualisierungen**: Der Code ist modular gestaltet; zusätzliche Diagrammarten lassen sich leicht ergänzen, indem weitere Plot‑Funktionen implementiert und im Bericht eingebunden werden.

Viel Spaß beim Ausprobieren und Anpassen des Smart Report Assistant!