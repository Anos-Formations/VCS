import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Configuration de l'application web
st.set_page_config(page_title="VCS - Manager de Terrain", page_icon="🛡️", layout="wide")

# Fichier de stockage (Base de données locale)
DB_FILE = "base_donnees_vcs.csv"

# Initialisation de la base de données à la première ouverture
if not os.path.exists(DB_FILE):
    colonnes = [
        "Date", "Contrôleur", "Collaborateur", "Tâche",
        "Zone_Propre", "Zone_Rangee", "EPI_Casquette", "EPI_Gilet", 
        "EPI_Chaussures", "EPI_Gants", "EPI_Cutter",
        "Posture_Charges", "Posture_Hauteur", "Chariot_3Points", 
        "Chariot_Fourche", "Chariot_Klaxon", "Chariot_Ceinture", 
        "Points_Negatifs", "Bonnes_Pratiques"
    ]
    pd.DataFrame(columns=colonnes).to_csv(DB_FILE, index=False)

# Menu latéral de navigation
menu = st.sidebar.radio("Outils Manager", ["📝 Réaliser une VCS", "🗄️ Historique des données", "📈 Tableau de Bord"])

# -------------------------------------------------------------
# ENREGISTREMENT D'UNE NOUVELLE VISITE
# -------------------------------------------------------------
if menu == "📝 Réaliser une VCS":
    st.title("🛡️ Visite Comportementale de Sécurité (V.C.S)")
    st.markdown("> *L'échange doit être constructif afin de garder l'attention de notre interlocuteur. Restez toujours sur un échange positif.*")
    
    with st.form("formulaire_vcs", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            date_visite = st.date_input("Date de l'observation", datetime.now())
            controleur = st.text_input("Nom du Manager (Contrôleur)")
        with col2:
            collaborateur = st.text_input("Nom du collaborateur observé")
            tache = st.text_input("Tâche / Poste observé")
            
        st.write("### 📊 Grille de conformité terrain")
        c1, c2, c3 = st.columns(3)
        
        with c1:
            st.markdown("**📁 Zone de travail**")
            z_propre = st.selectbox("Zone propre et dégagée", ["Conforme", "Non Conforme"])
            z_rangee = st.selectbox("Zone rangée", ["Conforme", "Non Conforme"])
            
            st.markdown("**🧍 Gestes et Postures**")
            p_charge = st.selectbox("Port de charge", ["Conforme", "Non Conforme", "Non Applicable"])
            p_hauteur = st.selectbox("Travail à bonne hauteur", ["Conforme", "Non Conforme"])

        with c2:
            st.markdown("**🦺 Port des EPI**")
            epi_cas = st.selectbox("Casquette / Casque", ["Conforme", "Non Conforme", "Non Applicable"])
            epi_gil = st.selectbox("Gilet Haute Visibilité", ["Conforme", "Non Conforme"])
            epi_cha = st.selectbox("Chaussures de sécurité", ["Conforme", "Non Conforme"])
            epi_gan = st.selectbox("Gants", ["Conforme", "Non Conforme"])
            epi_cut = st.selectbox("État du cutter", ["Conforme", "Non Conforme", "Non Applicable"])

        with c3:
            st.markdown("**🚜 Chariots & Engins**")
            ch_3p = st.selectbox("Respect des 3 points", ["Conforme", "Non Conforme", "Non Applicable"])
            ch_fo = st.selectbox("Fourche basse à l'arrêt", ["Conforme", "Non Conforme", "Non Applicable"])
            ch_kl = st.selectbox("Klaxon intersections", ["Conforme", "Non Conforme", "Non Applicable"])
            ch_ce = st.selectbox("Port de la ceinture", ["Conforme", "Non Conforme", "Non Applicable"])

        st.write("### 💬 Débriefing et plan d'action")
        pts_neg = st.text_area("Point(s) négatif(s) constaté(s) / Action corrective prise")
        bonnes_prat = st.text_area("Bonne(s) pratique(s) observée(s) (à féliciter)")
        
        # Validation du formulaire
        bouton_valider = st.form_submit_button("Enregistrer la visite")
        
        if bouton_valider:
            if not controleur or not collaborateur:
                st.error("⚠️ Erreur : Les noms du manager et du collaborateur sont obligatoires.")
            else:
                # Structuration des données
                nouvelle_ligne = {
                    "Date": str(date_visite), "Contrôleur": controleur, "Collaborateur": collaborateur, "Tâche": tache,
                    "Zone_Propre": z_propre, "Zone_Rangee": z_rangee, "EPI_Casquette": epi_cas, "EPI_Gilet": epi_gil,
                    "EPI_Chaussures": epi_cha, "EPI_Gants": epi_gan, "EPI_Cutter": epi_cut,
                    "Posture_Charges": p_charge, "Posture_Hauteur": p_hauteur, "Chariot_3Points": ch_3p,
                    "Chariot_Fourche": ch_fo, "Chariot_Klaxon": ch_kl, "Chariot_Ceinture": ch_ce,
                    "Points_Negatifs": pts_neg, "Bonnes_Pratiques": bonnes_prat
                }
                # Injection dans le fichier CSV (sans écraser l'historique)
                df = pd.read_csv(DB_FILE)
                df = pd.concat([df, pd.DataFrame([nouvelle_ligne])], ignore_index=True)
                df.to_csv(DB_FILE, index=False)
                st.success(f"✅ La VCS pour {collaborateur} a été figée dans la base de données !")

# -------------------------------------------------------------
# HISTORIQUE ET EXTRACTION DES DONNÉES
# -------------------------------------------------------------
elif menu == "🗄️ Historique des données":
    st.title("🗄️ Base de données historique")
    df = pd.read_csv(DB_FILE)
    
    if df.empty:
        st.info("Aucune visite enregistrée pour le moment.")
    else:
        st.dataframe(df, use_container_width=True)
        # Bouton d'export pour Excel / Tableur classique
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Exporter la base de données au format Excel/CSV", data=csv, file_name="export_vcs_terrain.csv", mime="text/csv")

# -------------------------------------------------------------
# TABLEAU DE BORD AUTOMATIQUE
# -------------------------------------------------------------
elif menu == "📈 Tableau de Bord":
    st.title("📈 Statistiques de Sécurité")
    df = pd.read_csv(DB_FILE)
    
    if df.empty:
        st.info("Le tableau de bord s'activera dès la première visite enregistrée.")
    else:
        total_vcs = len(df)
        st.metric("Total des Visites Réalisées", total_vcs)
        
        # Calcul de la conformité globale sur les EPI
        epi_ok = (df["EPI_Chaussures"] == "Conforme").sum()
        taux = (epi_ok / total_vcs) * 100
        st.metric("Taux de conformité du port des Chaussures", f"{taux:.1f}%")