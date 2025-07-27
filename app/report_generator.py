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
from typing import Dict, Optional

import pandas as pd
import matplotlib

# Try to import OpenAI, fall back gracefully if not available
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("OpenAI package not available - using statistical analysis only")

try:
    from dotenv import load_dotenv
    # Load environment variables
    load_dotenv()
except ImportError:
    print("python-dotenv not available - please set environment variables manually")

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


def generate_report_data(file_path: str, use_gpt: bool = True) -> Dict[str, str]:
    """Liest Daten, erstellt Diagramme und fasst sie zusammen.

    Args:
        file_path: Path to the CSV file to analyze
        use_gpt: Whether to use GPT for enhanced analysis (default: True)

    Gibt ein Dictionary zurück, das an das HTML‑Template übergeben werden kann.
    """
    df = read_csv(file_path)
    bar_chart = generate_bar_chart(df)
    line_chart = generate_line_chart(df)
    
    # Try GPT analysis first, fall back to basic analysis if needed
    gpt_available = OPENAI_AVAILABLE and os.getenv('OPENAI_API_KEY') and os.getenv('OPENAI_API_KEY') != 'your-openai-api-key-here'
    
    if use_gpt and gpt_available:
        summary_dict = generate_summary_gpt(df)
        analysis_type = "GPT-Enhanced"
    else:
        summary_dict = generate_summary(df)
        analysis_type = "Statistical"
    
    return {
        "bar_chart": bar_chart,
        "line_chart": line_chart,
        "summary": summary_dict.get("summary", ""),
        "recommendations": summary_dict.get("recommendations", ""),
        "analysis_type": analysis_type
    }


def generate_summary_gpt(df: pd.DataFrame, api_key: Optional[str] = None) -> Dict[str, str]:
    """Generates advanced summary and recommendations using OpenAI GPT.

    Uses GPT to analyze the dataset and provide intelligent insights,
    recommendations, and detailed analysis of risk patterns.
    
    Args:
        df: The pandas DataFrame containing the risk data
        api_key: Optional OpenAI API key (if not provided, uses environment variable)
    
    Returns:
        Dictionary with 'summary' and 'recommendations' keys
    """
    # Check if OpenAI is available
    if not OPENAI_AVAILABLE:
        print("OpenAI package not available - falling back to statistical analysis")
        return generate_summary(df)
    
    try:
        # Get API key from parameter or environment
        if not api_key:
            api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key or api_key == 'your-openai-api-key-here':
            # Fallback to basic summary if no valid API key
            return generate_summary(df)
        
        # Initialize OpenAI client
        client = OpenAI(api_key=api_key)
        
        # Prepare data summary for GPT
        data_summary = prepare_data_for_gpt(df)
        
        # Create prompt for GPT analysis
        prompt = f"""
You are a senior risk analyst. Analyze the following business risk data and provide:

1. A comprehensive summary of the risk landscape
2. Specific, actionable recommendations

Data Summary:
{data_summary}

Please provide:
- A detailed analysis of risk patterns, trends, and key insights
- Specific recommendations for risk mitigation and management
- Identification of the most critical risk areas requiring immediate attention

Format your response as professional business analysis suitable for executive reporting.
Keep the summary concise but comprehensive (2-3 paragraphs) and recommendations actionable (3-5 specific points).
"""

        # Call GPT API
        response = client.chat.completions.create(
            model=os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo'),
            messages=[
                {"role": "system", "content": "You are an expert risk analyst providing professional business insights."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.7
        )
        
        # Parse the response
        full_response = response.choices[0].message.content
        
        # Split into summary and recommendations
        summary, recommendations = parse_gpt_response(full_response)
        
        return {
            "summary": summary,
            "recommendations": recommendations
        }
        
    except Exception as e:
        print(f"GPT API error: {e}")
        # Fallback to basic summary if GPT fails
        return generate_summary(df)


def prepare_data_for_gpt(df: pd.DataFrame) -> str:
    """Prepares a concise data summary for GPT analysis."""
    summary_parts = []
    
    # Basic dataset info
    summary_parts.append(f"Dataset contains {len(df)} records spanning from {df['Date'].min()} to {df['Date'].max()}")
    
    # Risk categories and scores
    if 'RiskCategory' in df.columns and 'Risikoscore' in df.columns:
        category_stats = df.groupby('RiskCategory')['Risikoscore'].agg(['sum', 'mean', 'count'])
        summary_parts.append("\nRisk Categories Analysis:")
        for category, stats in category_stats.iterrows():
            summary_parts.append(f"- {category}: {stats['count']} incidents, Total Score: {stats['sum']:.1f}, Avg: {stats['mean']:.2f}")
    
    # Temporal trends
    if 'Date' in df.columns and 'Risikoscore' in df.columns:
        monthly_trend = df.groupby(df['Date'].dt.to_period('M'))['Risikoscore'].mean()
        if len(monthly_trend) > 1:
            trend_direction = "increasing" if monthly_trend.iloc[-1] > monthly_trend.iloc[0] else "decreasing"
            summary_parts.append(f"\nTrend Analysis: Risk scores are {trend_direction} over time")
            summary_parts.append(f"Highest risk month: {monthly_trend.idxmax()} (avg: {monthly_trend.max():.2f})")
            summary_parts.append(f"Lowest risk month: {monthly_trend.idxmin()} (avg: {monthly_trend.min():.2f})")
    
    # Financial impact
    if 'Verluste' in df.columns:
        total_losses = df['Verluste'].sum()
        avg_losses = df['Verluste'].mean()
        max_loss = df['Verluste'].max()
        summary_parts.append(f"\nFinancial Impact: Total losses: {total_losses:.2f}, Average: {avg_losses:.2f}, Maximum single loss: {max_loss:.2f}")
    
    # Customer impact
    if 'Kundenzahlen' in df.columns:
        total_customers = df['Kundenzahlen'].sum()
        avg_customers = df['Kundenzahlen'].mean()
        summary_parts.append(f"\nCustomer Impact: Total affected customers: {total_customers}, Average per incident: {avg_customers:.1f}")
    
    return "\n".join(summary_parts)


def parse_gpt_response(response: str) -> tuple[str, str]:
    """Parses GPT response into summary and recommendations sections."""
    # Try to split by common section headers
    lower_response = response.lower()
    
    # Look for recommendations section
    rec_markers = ['recommendations:', 'recommendation:', 'suggested actions:', 'action items:', 'next steps:']
    rec_start = -1
    
    for marker in rec_markers:
        pos = lower_response.find(marker)
        if pos != -1:
            rec_start = pos
            break
    
    if rec_start != -1:
        summary = response[:rec_start].strip()
        recommendations = response[rec_start:].strip()
        
        # Clean up section headers
        for marker in rec_markers:
            recommendations = recommendations.replace(marker, '').replace(marker.title(), '').strip()
    else:
        # If no clear separation, split roughly in half
        mid_point = len(response) // 2
        # Find nearest sentence break
        sentence_break = response.find('.', mid_point)
        if sentence_break != -1:
            summary = response[:sentence_break + 1].strip()
            recommendations = response[sentence_break + 1:].strip()
        else:
            summary = response
            recommendations = "Please review the analysis above for actionable insights."
    
    return summary, recommendations