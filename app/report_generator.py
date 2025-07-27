"""
report_generator.py
--------------------

Diese Datei enthält die Kernlogik zur Verarbeitung hochgeladener CSV‑Dateien.
Sie liest die Daten ein, erzeugt daraus Diagramme und generiert einen
menschenlesbaren Text, der Highlights und Auffälligkeiten hervorhebt.

Die Diagramme werden mit Matplotlib erstellt und im Ordner
`app/static/plots` als PNG gespeichert. Die Texterstellung nutzt einfache
statistische Berechnungen. Wer einen API‑Key für ein Sprachmodell
verwendet, kann in der Funktion `generate_summary_gpt` eine externe
Zusammenfassung einbauen.
"""

import os
import uuid
from datetime import datetime
from typing import Dict

import pandas as pd
import matplotlib

# Verwende das Agg‑Backend, da kein GUI verfügbar ist.
matplotlib.use("Agg")  # type: ignore
import matplotlib.pyplot as plt


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PLOTS_DIR = os.path.join(BASE_DIR, "static", "plots")

# Stelle sicher, dass der Plot‑Ordner existiert
os.makedirs(PLOTS_DIR, exist_ok=True)


def read_csv(file_path: str) -> pd.DataFrame:
    """Lädt eine CSV‑Datei in ein Pandas DataFrame.

    Erwartet eine Datei mit mindestens folgenden Spalten:

    - Date: Datum (ISO‑Format YYYY-MM oder YYYY-MM-DD)
    - RiskCategory: Kategorie des Risikos (z. B. "Operational", "Market")
    - Risikoscore: numerischer Score
    - Kundenzahlen: Anzahl der Kunden (optional)
    - Verluste: monetärer Verlust (optional)

    Andere Spalten werden ignoriert, aber mitgeladen.
    """
    df = pd.read_csv(file_path)
    # Datumsfeld in datetime umwandeln; wenn Tag fehlt, den 1. setzen
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    return df


def generate_bar_chart(df: pd.DataFrame) -> str:
    """Erzeugt ein Balkendiagramm der Top‑Risiken nach Kategorie.

    Aggregiert die Spalte 'Risikoscore' nach 'RiskCategory' und zeichnet
    die Summe je Kategorie. Gibt den Dateinamen des gespeicherten PNG zurück.
    """
    if "RiskCategory" not in df.columns or "Risikoscore" not in df.columns:
        # Kein Balkendiagramm möglich
        return ""
    grouped = df.groupby("RiskCategory")["Risikoscore"].sum().sort_values(ascending=False)
    # Erzeuge Grafik
    fig, ax = plt.subplots(figsize=(8, 4))
    grouped.plot(kind="bar", color="skyblue", ax=ax)
    ax.set_title("Top-Risiken nach Kategorie")
    ax.set_xlabel("Risikokategorie")
    ax.set_ylabel("Summe Risikoscore")
    plt.tight_layout()
    # Speichern
    filename = f"bar_{uuid.uuid4().hex}.png"
    filepath = os.path.join(PLOTS_DIR, filename)
    fig.savefig(filepath)
    plt.close(fig)
    return filename


def generate_line_chart(df: pd.DataFrame) -> str:
    """Erzeugt ein Liniendiagramm des durchschnittlichen Risikoscores pro Monat.

    Gruppiert das DataFrame nach Monat und berechnet den Mittelwert des
    'Risikoscore'. Gibt den Dateinamen des gespeicherten PNG zurück.
    """
    if "Date" not in df.columns or "Risikoscore" not in df.columns:
        return ""
    # Nach Monat gruppieren
    df_monthly = df.copy()
    df_monthly["YearMonth"] = df_monthly["Date"].dt.to_period("M")
    grouped = df_monthly.groupby("YearMonth")["Risikoscore"].mean().sort_index()
    # Format für x‑Achse: Jahr‑Monat
    x_labels = [str(p) for p in grouped.index]
    y_values = grouped.values
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(x_labels, y_values, marker="o", color="steelblue")
    ax.set_title("Durchschnittlicher Risikoscore pro Monat")
    ax.set_xlabel("Monat")
    ax.set_ylabel("Risikoscore (Mittelwert)")
    ax.grid(True, linestyle="--", alpha=0.5)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    filename = f"line_{uuid.uuid4().hex}.png"
    filepath = os.path.join(PLOTS_DIR, filename)
    fig.savefig(filepath)
    plt.close(fig)
    return filename


def generate_summary(df: pd.DataFrame) -> Dict[str, str]:
    """Generiert eine einfache textuelle Zusammenfassung der Daten.

    Erstellt einen zusammenhängenden Fließtext, der die wichtigsten
    Erkenntnisse beschreibt, sowie eine optionale Empfehlung.

    Gibt ein Dictionary mit Schlüsseln `summary` und `recommendations` zurück.
    """
    summary_lines = []
    recommendation_lines = []
    # Anzahl der Datensätze
    num_records = len(df)
    summary_lines.append(f"Der Datensatz enthält insgesamt {num_records} Einträge.")

    # Top‑Risiko‑Kategorien
    if "RiskCategory" in df.columns and "Risikoscore" in df.columns:
        category_scores = df.groupby("RiskCategory")["Risikoscore"].sum()
        top_categories = category_scores.sort_values(ascending=False).head(3)
        cats = ", ".join([f"{cat} (Summe: {score:.1f})" for cat, score in top_categories.items()])
        summary_lines.append(
            f"Die drei wichtigsten Risikokategorien sind {cats}."
        )
    
    # Monat mit höchstem Risiko
    if "Date" in df.columns and "Risikoscore" in df.columns:
        df_monthly = df.copy()
        df_monthly["YearMonth"] = df_monthly["Date"].dt.to_period("M")
        monthly_mean = df_monthly.groupby("YearMonth")["Risikoscore"].mean()
        if not monthly_mean.empty:
            highest_month = monthly_mean.idxmax()
            highest_value = monthly_mean.max()
            summary_lines.append(
                f"Der höchste durchschnittliche Risikoscore wurde im Monat {highest_month} mit {highest_value:.2f} erreicht."
            )
            # Trendanalyse: Vergleich Q1 vs. Q2
            # Ermittle Durchschnitt pro Quartal
            df_monthly["Quarter"] = df_monthly["Date"].dt.to_period("Q")
            quarterly_mean = df_monthly.groupby("Quarter")["Risikoscore"].mean().sort_index()
            if len(quarterly_mean) >= 2:
                q1, q2 = quarterly_mean.iloc[0], quarterly_mean.iloc[1]
                if q2 > q1 * 1.1:  # Anstieg größer als 10%
                    recommendation_lines.append(
                        "Achten Sie auf den signifikanten Anstieg des Risikoscores im zweiten Quartal."
                    )
                elif q2 < q1 * 0.9:
                    recommendation_lines.append(
                        "Der Risikoscore hat sich im zweiten Quartal deutlich verringert – nutzen Sie diese positive Entwicklung."
                    )

    # Statistische Kennzahlen für Verluste
    if "Verluste" in df.columns:
        losses = df["Verluste"].dropna()
        if not losses.empty:
            avg_loss = losses.mean()
            max_loss = losses.max()
            summary_lines.append(
                f"Die durchschnittlichen Verluste betragen {avg_loss:.2f} Einheiten, der maximale Verlust lag bei {max_loss:.2f}."
            )
            # Empfehlung bei hohen Verlusten
            if max_loss > avg_loss * 1.5:
                recommendation_lines.append(
                    "Es gibt einzelne Monate mit außergewöhnlich hohen Verlusten – prüfen Sie diese genauer."
                )

    summary_text = " ".join(summary_lines)
    recommendations = " ".join(recommendation_lines)
    return {"summary": summary_text, "recommendations": recommendations}


def generate_report_data(file_path: str) -> Dict[str, str]:
    """Liest Daten, erstellt Diagramme und fasst sie zusammen.

    Gibt ein Dictionary zurück, das an das HTML‑Template übergeben werden kann.
    """
    df = read_csv(file_path)
    bar_chart = generate_bar_chart(df)
    line_chart = generate_line_chart(df)
    summary_dict = generate_summary(df)
    return {
        "bar_chart": bar_chart,
        "line_chart": line_chart,
        "summary": summary_dict.get("summary", ""),
        "recommendations": summary_dict.get("recommendations", ""),
    }


def generate_summary_gpt(df: pd.DataFrame, api_key: str) -> str:
    """Platzhalter für die Integration eines externen Sprachmodells.

    Aktuell wird diese Funktion nicht verwendet. Wenn ein API‑Key vorliegt,
    kann hier die Anbindung an ein Modell wie GPT erfolgen, um eine
    fortgeschrittene Zusammenfassung zu erzeugen.
    """
    # Beispielhafte Implementierung (pseudo-code):
    # import openai
    # prompt = f"Analysiere den folgenden Datensatz: {df.head().to_string()}"
    # openai.api_key = api_key
    # response = openai.ChatCompletion.create(...)
    # return response.choices[0].message['content']
    raise NotImplementedError("External GPT summarization not implemented.")