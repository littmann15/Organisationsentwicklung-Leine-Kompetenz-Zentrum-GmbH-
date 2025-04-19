
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Qualitative Organisationsdiagnostik", layout="wide")
st.title("📊 Qualitative Organisationsdiagnostik nach Meihei")

wesenselemente = {
    "A. Identität": [
        "Ziele eng mit Lebensauffassung der Leitung",
        "Ziele in offiziellen Papieren",
        "Ziele werden regelmäßig diskutiert",
        "Ziele klar, dienen Partnerbeziehungen"
    ],
    "B. Strategie": [
        "Leitung hat Weitblick, selten ausformuliert",
        "Strategiegespräche oben",
        "Dialog zwischen Führungsebenen",
        "Einbeziehung Mitarbeitende & Partner"
    ],
    "C. Struktur": [
        "Wenig formell, nach Bedarf",
        "Formell klar abgegrenzt",
        "Struktur nach Prozessen mit Verantwortung",
        "Vernetzte Business Units"
    ],
    "D1. Führung (Entwicklung)": [
        "Tüchtigkeit wird gefördert",
        "Förderung nach Standards",
        "Entwicklungsgespräche",
        "Verantwortliche Förderung mit Partnern"
    ],
    "D2. Führung (Konflikte)": [
        "Beziehungen zu Führung wichtig",
        "Vorgesetzte entscheiden",
        "Konfliktlösung mit Führung",
        "Selbstständige Konfliktbearbeitung"
    ],
    "E1. Funktionen": [
        "Aufgabenvielfalt, Menschen im Fokus",
        "Funktionen klar gegliedert",
        "Funktionen mit Spielraum",
        "Selbstorganisierte Teams"
    ],
    "E2. Projekte": [
        "Vertrauensbasierte Vergabe",
        "Klare Richtlinien",
        "Zielverständnis, Spielraum",
        "Projektkompetenz mit Externen"
    ],
    "F1. Abläufe": [
        "Improvisation",
        "Standardisierte Regeln",
        "Grobpläne mit Eigenverantwortung",
        "Nahtstellen- und Prozessbewusstsein"
    ],
    "F2. Delegation": [
        "Delegation mit Vorbehalt",
        "Kontrollierte Aufgabenerfüllung",
        "Regelmäßige Reflexion",
        "Selbstständiges Management"
    ],
    "G. Ressourcen": [
        "Kundenkontakt im Fokus",
        "Einheitliche Ausstattung, transparente Finanzen",
        "Eigenverantwortliches Budget",
        "Zentrale Standards, offene Bücher"
    ]
}

bewertungen = []
st.subheader("🔹 IST- und SOLL-Zustände auswählen")
for bereich, beschreibungen in wesenselemente.items():
    st.markdown(f"**{bereich}**")
    col1, col2 = st.columns(2)
    with col1:
        ist = st.radio(f"IST ({bereich})", beschreibungen, key=f"ist_{bereich}")
    with col2:
        soll = st.radio(f"SOLL ({bereich})", beschreibungen, key=f"soll_{bereich}")
    ist_index = beschreibungen.index(ist)
    soll_index = beschreibungen.index(soll)
    differenz = abs(soll_index - ist_index)
    entwicklungsbedarf = "hoch" if differenz == 3 else "mittel" if differenz == 2 else "gering" if differenz == 1 else "kein"
    bewertungen.append({
        "Bereich": bereich,
        "IST": ist,
        "SOLL": soll,
        "Differenz": differenz,
        "Entwicklungsbedarf": entwicklungsbedarf,
        "IST Index": ist_index,
        "SOLL Index": soll_index
    })

df = pd.DataFrame(bewertungen)
st.subheader("📈 Auswertung")
st.dataframe(df, use_container_width=True)

max_diff = df["Differenz"].max()
schwerpunkte = df[df["Differenz"] == max_diff]["Bereich"].tolist()

st.markdown("### 🔍 Entwicklungsschwerpunkt")
if max_diff == 0:
    st.success("Kein Entwicklungsbedarf festgestellt. IST und SOLL sind identisch.")
else:
    st.warning(f"Größter Entwicklungsbedarf in: **{', '.join(schwerpunkte)}** (Differenz: {max_diff})")

st.subheader("📉 Radar-Plot der IST/SOLL-Werte")

categories = list(df["Bereich"])
ist_values = df["IST Index"].tolist()
soll_values = df["SOLL Index"].tolist()

N = len(categories)
angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
ist_values += ist_values[:1]
soll_values += soll_values[:1]
angles += angles[:1]

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
ax.plot(angles, ist_values, 'o-', linewidth=2, label='IST')
ax.fill(angles, ist_values, alpha=0.25)
ax.plot(angles, soll_values, 'o-', linewidth=2, label='SOLL')
ax.fill(angles, soll_values, alpha=0.25)
ax.set_thetagrids(np.degrees(angles[:-1]), categories)
ax.set_ylim(0, 3)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
st.pyplot(fig)

csv = df.to_csv(index=False).encode('utf-8')
st.download_button("📥 Ergebnisse als CSV herunterladen", csv, "organisationsdiagnose_ergebnisse.csv", "text/csv")
