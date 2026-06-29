import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Configuration de l'application web
st.set_page_config(page_title="VCS - Manager de Terrain", page_icon="🛡️", layout="wide")

# Fichier de stockage (Base de données locale)
DB_FILE = "base_donnees_vcs.csv"

# Les critères d'évaluation exacts pour automatiser les calculs du Tableau de Bord
CRITERES = {
    "📁 Zone de travail": ["Zone_Propre", "Zone_Rangee"],
    "🦺 Équipements (EPI)": ["EPI_Casquette", "EPI_Gilet", "EPI_Chaussures", "EPI_Gants", "EPI_Cutter"],
    "🧍 Gestes & Postures": ["Posture_Charges", "Posture_Hauteur"],
    "🚜 Chariots & Engins": ["Chariot_3Points", "Chariot_Fourche", "Chariot_Klaxon", "Chariot_Ceinture"]
}

# Initialisation de la base de données
if not os.path.exists(DB_FILE):
    colonnes = ["Date", "Contrôleur", "Collaborateur", "Tâche"]
    for cat, fields in CRITERES.items():
        colonnes.extend(fields)
    colonnes.extend(["Points_Negatifs", "Bonnes_Pratiques"])
    pd.DataFrame(columns=colonnes).to_csv(DB_FILE, index=False)

# Menu latéral de navigation
menu = st.sidebar.radio("Outils Manager", ["📝 Réaliser une VCS", "🗄️ Historique des données", "📈 Tableau de Bord Global"])

# -------------------------------------------------------------
# 1. ENREGISTREMENT D'UNE NOUVELLE VISITE
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
            p_hauteur = st.selectbox("Travail à bonne hauteur", ["Conforme", "Non Conforme", "Non Applicable"])

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
        
        if st.form_submit_button("Enregistrer la visite"):
            if not controleur or not collaborateur:
                st.error("⚠️ Erreur : Les noms du manager et du collaborateur sont obligatoires.")
            else:
                nouvelle_ligne = {
                    "Date": str(date_visite), "Contrôleur": controleur, "Collaborateur": collaborateur, "Tâche": tache,
                    "Zone_Propre": z_propre, "Zone_Rangee": z_rangee, "EPI_Casquette": epi_cas, "EPI_Gilet": epi_gil,
                    "EPI_Chaussures": epi_cha, "EPI_Gants": epi_gan, "EPI_Cutter": epi_cut,
                    "Posture_Charges": p_charge, "Posture_Hauteur": p_hauteur, "Chariot_3Points": ch_3p,
                    "Chariot_Fourche": ch_fo, "Chariot_Klaxon": ch_kl, "Chariot_Ceinture": ch_ce,
                    "Points_Negatifs": pts_neg, "Bonnes_Pratiques": bonnes_prat
                }
                df = pd.read_csv(DB_FILE)
                df = pd.concat([df, pd.DataFrame([nouvelle_ligne])], ignore_index=True)
                df.to_csv(DB_FILE, index=False)
                st.success(f"✅ La VCS pour {collaborateur} a bien été ajoutée au fichier !")

# -------------------------------------------------------------
# 2. HISTORIQUE
# -------------------------------------------------------------
elif menu == "🗄️ Historique des données":
    st.title("🗄️ Base de données historique")
    df = pd.read_csv(DB_FILE)
    if df.empty:
        st.info("Aucune visite enregistrée.")
    else:
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Exporter la base (CSV/Excel)", data=csv, file_name="export_vcs.csv", mime="text/csv")

# -------------------------------------------------------------
# 3. TABLEAU DE BORD GLOBAL ET EXHAUSTIF
# -------------------------------------------------------------
elif menu == "📈 Tableau de Bord Global":
    st.title("📈 Tableau de Bord Global de Sécurité")
    df = pd.read_csv(DB_FILE)
    
    if df.empty:
        st.info("📊 Enregistrez vos premières visites pour voir l'analyse complète de tous vos indicateurs.")
    else:
        # KPI d'en-tête
        total_vcs = len(df)
        unique_managers = df["Contrôleur"].nunique()
        unique_collabs = df["Collaborateur"].nunique()
        
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric("Total des VCS Réalisées", total_vcs)
        kpi2.metric("Managers Actifs", unique_managers)
        kpi3.metric("Collaborateurs Évalués", unique_collabs)
        
        st.markdown("---")
        st.subheader("🎯 Taux de Conformité par Point de Contrôle")
        st.markdown("Ce tableau calcule automatiquement le taux de conformité pour **chaque critère** saisi sur le terrain.")
        
        # Traduction des colonnes techniques en libellés clairs
        labels_trad = {
            "Zone_Propre": "Zone propre et dégagée", "Zone_Rangee": "Zone rangée",
            "EPI_Casquette": "Casquette / Casque", "EPI_Gilet": "Gilet Haute Visibilité",
            "EPI_Chaussures": "Chaussures de sécurité", "EPI_Gants": "Gants", "EPI_Cutter": "État du cutter",
            "Posture_Charges": "Port de charge conforme", "Posture_Hauteur": "Travail à la bonne hauteur",
            "Chariot_3Points": "Respect des 3 points (Engins)", "Chariot_Fourche": "Fourche basse à l'arrêt",
            "Chariot_Klaxon": "Klaxon aux intersections", "Chariot_Ceinture": "Port de la ceinture"
        }
        
        stats_data = []
        for categorie, champs in CRITERES.items():
            for champ in champs:
                # Filtrer les valeurs 'Non Applicable' pour ne pas fausser la statistique réelle
                data_filtree = df[df[champ] != "Non Applicable"]
                total_eval = len(data_filtree)
                
                if total_eval > 0:
                    conformes = (data_filtree[champ] == "Conforme").sum()
                    taux = (conformes / total_eval) * 100
                    affichage_taux = f"{taux:.1f} %"
                else:
                    affichage_taux = "Aucune évaluation"
                
                stats_data.append({
                    "Catégorie": categorie,
                    "Élément de Contrôle": labels_trad.get(champ, champ),
                    "Taux de Conformité (Impact Réel)": affichage_taux,
                    "Nombre d'observations valides": total_eval
                })
        
        # Affichage du tableau de bord complet
        df_stats = pd.DataFrame(stats_data)
        st.dataframe(df_stats, use_container_width=True, hide_index=True)
        
        # Journal des alertes terrain (Plan d'action direct)
        st.markdown("---")
        st.subheader("⚠️ Journal des points critiques et actions prises")
        df_alertes = df[df["Points_Negatifs"].notna() & (df["Points_Negatifs"] != "")]
        if not df_alertes.empty:
            st.dataframe(df_alertes[["Date", "Collaborateur", "Points_Negatifs"]], use_container_width=True, hide_index=True)
        else:
            st.success("Aucun point critique ou alerte à signaler sur le terrain pour le moment ! 👍")