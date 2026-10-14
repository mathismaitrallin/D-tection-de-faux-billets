import streamlit as st
import pandas as pd
import joblib  


# -----------------------------
# 🌐 Langue : français par défaut, anglais avec ?lang=en dans l'adresse
# -----------------------------
LANGUE = "en" if st.query_params.get("lang") == "en" else "fr"


def tr(fr, en):
    return en if LANGUE == "en" else fr


def selecteur_langue():
    """Boutons FR | EN en haut de page ; le choix est écrit dans l'adresse."""
    _, col = st.columns([3, 1])
    choix = col.radio("Langue / Language", ["FR", "EN"], index=0 if LANGUE == "fr" else 1,
                      horizontal=True, label_visibility="collapsed")
    if choix.lower() != LANGUE:
        st.query_params["lang"] = choix.lower()
        st.rerun()

# Charger le modèle 
model = joblib.load("svm_billets_model.pkl")

# Interface utilisateur
selecteur_langue()
st.title(tr("💵 Détection de Faux Billets", "💵 Counterfeit Banknote Detection"))
st.write(tr("Entrez les dimensions du billet pour vérifier s'il est authentique.",
            "Enter the banknote's dimensions to check whether it is genuine."))

# Champs d'entrée pour les dimensions du billet
diagonal = st.number_input ("Diagonal", min_value=0.0, step=1.0)
height_left = st.number_input("Height Left", min_value=0.0, step=1.0)
height_right = st.number_input("Height Right", min_value=0.0, step=1.0)
margin_low = st.number_input("Margin Low", min_value=0.0, step=1.0)
margin_up = st.number_input("Margin Up", min_value=0.0, step=1.0)
length = st.number_input("Length", min_value=0.0, step=1.0)

# Bouton pour faire la prédiction
if st.button(tr("🔍 Vérifier le billet", "🔍 Check the banknote")):
    # Préparer les données sous forme de DataFrame
    input_data = pd.DataFrame([{
    "diagonal" : diagonal,
        "height_left": height_left,
        "height_right": height_right,
        "margin_low": margin_low,
        "margin_up": margin_up,
        "length": length
    }])

    # Appliquer la même normalisation que lors de l'entraînement

    # Prédire si le billet est vrai ou faux
    prediction = model.predict(input_data)

    # Afficher le résultat
    if prediction[0] == 1:
        st.success(tr("✅ Le billet est AUTHENTIQUE !", "✅ This banknote is GENUINE!"))
    else:
        st.error(tr("❌ Le billet est FAUX !", "❌ This banknote is COUNTERFEIT!"))