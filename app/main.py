"""
main.py
--------

Dies ist das Entrypoint der Flask‑Anwendung. Die App stellt eine Seite
bereit, auf der eine CSV‑Datei hochgeladen werden kann. Nach dem Upload
wird der Datensatz analysiert, Diagramme werden erzeugt und ein
HTML‑Bericht gerendert.

Starten Sie die Anwendung mit:

```
python app/main.py
```

oder unter Verwendung der Umgebungsvariable `FLASK_APP`:

```
export FLASK_APP=app/main.py
flask run
```
"""

import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

from .report_generator import generate_report_data


ALLOWED_EXTENSIONS = {"csv"}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

# Verzeichnis für hochgeladene Dateien anlegen
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename: str) -> bool:
    """Prüft, ob die Dateiendung erlaubt ist (hier nur CSV)."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def index():
    """Landing‑Page: Upload‑Formular und Bericht.

    Bei GET wird das Upload‑Formular angezeigt. Bei POST wird die
    hochgeladene Datei verarbeitet und der Bericht gerendert.
    """
    if request.method == "POST":
        # Datei aus dem Formular lesen
        file = request.files.get("file")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)
            # Reportdaten generieren
            report_data = generate_report_data(file_path)
            return render_template(
                "report.html",
                summary=report_data.get("summary"),
                recommendations=report_data.get("recommendations"),
                bar_chart=report_data.get("bar_chart"),
                line_chart=report_data.get("line_chart"),
            )
        else:
            error = "Bitte laden Sie eine gültige CSV‑Datei hoch."
            return render_template("upload.html", error=error)
    # GET‑Anfrage: Upload‑Formular anzeigen
    return render_template("upload.html")


if __name__ == "__main__":
    # Lokales Testing mit Debug‑Modus
    app.run(debug=True)