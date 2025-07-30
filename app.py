import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from database import DatabaseManager
from backup_manager import BackupManager
from datetime import datetime, timedelta
import os
import numpy as np
import hashlib
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration de la page
st.set_page_config(
    page_title="Bureau d'Étude - Tourisme Castagniccia Casinca",
    page_icon="logo.jpg",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Fonction pour hasher le mot de passe
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Configuration du mot de passe depuis le fichier .env
CORRECT_PASSWORD = os.getenv("ADMIN_PASSWORD")

# Vérifier que le mot de passe est défini
if not CORRECT_PASSWORD:
    st.error("❌ **Erreur de configuration**")
    st.error(
        "Le fichier `.env` n'existe pas ou la variable `ADMIN_PASSWORD` n'est pas définie."
    )
    st.info("**Solution :**")
    st.code(
        """
# Créez un fichier .env dans le répertoire du projet avec :
ADMIN_PASSWORD=votre_mot_de_passe_ici
    """
    )
    st.stop()

HASHED_PASSWORD = hash_password(CORRECT_PASSWORD)


# Fonction d'authentification
def check_password():
    """Retourne True si l'utilisateur a saisi le bon mot de passe"""

    def password_entered():
        """Vérifie si le mot de passe saisi est correct"""
        # Vérifier que password_input existe dans session_state
        if (
            "password_input" not in st.session_state
            or not st.session_state["password_input"]
        ):
            st.session_state["password_correct"] = False
            return

        if hash_password(st.session_state["password_input"]) == HASHED_PASSWORD:
            st.session_state["password_correct"] = True
            del st.session_state["password_input"]  # Ne pas stocker le mot de passe
        else:
            st.session_state["password_correct"] = False

    # Première visite ou mot de passe incorrect
    if "password_correct" not in st.session_state:
        # Interface de connexion
        st.markdown(
            """
            <div style="
                display: flex;
                justify-content: center;
                align-items: center;
                margin: -1rem;
                border-radius: 10px;
            ">
                <div style="
                    text-align: center;
                ">
                    <h1 style="color: #2d3748; margin-bottom: 1rem;">Accès Sécurisé</h1>
                    <h2 style="color: #4a5568; margin-bottom: 2rem; font-weight: 400;">Bureau d'Étude Tourisme</h2>
                    <p style="color: #718096; margin-bottom: 2rem;">Castagniccia Casinca</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Formulaire de connexion centré
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.text_input(
                "Mot de passe",
                type="password",
                on_change=password_entered,
                key="password_input",
                placeholder="Saisissez votre mot de passe",
            )

            if st.button("Se connecter", type="primary", use_container_width=True):
                password_entered()

        return False

    elif not st.session_state["password_correct"]:
        # Mot de passe incorrect
        st.error("Mot de passe incorrect")

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.text_input(
                "Mot de passe",
                type="password",
                on_change=password_entered,
                key="password_input",
                placeholder="Saisissez votre mot de passe",
            )

            if st.button("Se connecter", type="primary", use_container_width=True):
                password_entered()

        return False

    else:
        # Mot de passe correct
        return True


# Vérifier l'authentification avant d'afficher l'application
if not check_password():
    st.stop()


# Initialisation de la base de données
@st.cache_resource
def init_db():
    return DatabaseManager()


@st.cache_resource
def init_backup():
    return BackupManager()


db = init_db()
backup_manager = init_backup()

# CSS pour le style
st.markdown(
    """
<style>
    /* Masquer le bouton Deploy */
    [data-testid="stToolbar"] .st-emotion-cache-xnz43d {  
        display: none;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Header principal
st.markdown(
    """
<div class="main-header">
    <h1>Bureau d'Étude - Tourisme Castagniccia Casinca</h1>
    <p>Analyse des données de fréquentation et des profils visiteurs</p>
</div>
""",
    unsafe_allow_html=True,
)

# Sidebar pour la navigation
with st.sidebar:
    page = st.selectbox(
        "Navigation",
        [
            "Vue d'ensemble",
            "Gestion des Visiteurs",
            "Gestion des Pages",
            "Analyses Détaillées",
            "Suppression en Masse",
            "Gestion des Sauvegardes",
        ],
    )

    st.divider()

    # Bouton de déconnexion
    if st.button("Se déconnecter", type="secondary", use_container_width=True):
        # Réinitialiser l'état d'authentification
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

if page == "Vue d'ensemble":

    #  Métriques principales - design sobre et professionnel
    col1, col2, col3, col4 = st.columns(4)

    visiteurs = db.get_visiteurs()
    vues_pages = db.get_vues_pages()
    vues_totales = db.get_vues_totales()
    stats = db.get_stats_visiteurs()

    with col1:
        st.markdown(
            """
        <div style="
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            border-left: 4px solid #e53e3e;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
        ">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <h3 style="color: #2d3748; margin: 0; font-size: 1.8rem; font-weight: 700;">{}</h3>
                    <p style="color: #718096; margin: 0; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;">Vues Totales</p>
                </div>
                <div style="color: #e53e3e; font-size: 2rem;"></div>
            </div>
        </div>
        """.format(
                vues_totales
            ),
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
        <div style="
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            border-left: 4px solid #38a169;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
        ">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <h3 style="color: #2d3748; margin: 0; font-size: 1.8rem; font-weight: 700;">{}</h3>
                    <p style="color: #718096; margin: 0; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;">Visiteurs</p>
                </div>
                <div style="color: #38a169; font-size: 2rem;"></div>
            </div>
        </div>
        """.format(
                len(visiteurs)
            ),
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
        <div style="
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            border-left: 4px solid #3182ce;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
        ">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <h3 style="color: #2d3748; margin: 0; font-size: 1.8rem; font-weight: 700;">{}</h3>
                    <p style="color: #718096; margin: 0; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;">Pages Trackées</p>
                </div>
                <div style="color: #3182ce; font-size: 2rem;"></div>
            </div>
        </div>
        """.format(
                len(vues_pages)
            ),
            unsafe_allow_html=True,
        )

    with col4:
        moyenne_vues = (
            sum([vue[2] for vue in vues_pages]) / len(vues_pages) if vues_pages else 0
        )
        st.markdown(
            """
        <div style="
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            border-left: 4px solid #805ad5;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
        ">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <h3 style="color: #2d3748; margin: 0; font-size: 1.8rem; font-weight: 700;">{:.1f}</h3>
                    <p style="color: #718096; margin: 0; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;">Vues Moy./Page</p>
                </div>
                <div style="color: #805ad5; font-size: 2rem;"></div>
            </div>
        </div>
        """.format(
                moyenne_vues
            ),
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ANALYSES PROFESSIONNELLES PERTINENTES
    if visiteurs and vues_pages:
        # Données pour les analyses
        df_visiteurs = pd.DataFrame(
            visiteurs, columns=["ID", "Type", "Temps", "Age", "Interet", "Date"]
        )
        df_pages = pd.DataFrame(
            vues_pages, columns=["Page", "Categorie", "Vues", "Date"]
        )

        # Analyse 1: Segmentation clientèle par profil démographique
        st.subheader("Analyse Stratégique de la Clientèle")

        col1, col2 = st.columns(2)

        with col1:
            # Matrice Âge vs Type de visiteur (pertinente pour le tourisme)
            if len(visiteurs) > 5:
                cross_age_type = pd.crosstab(df_visiteurs["Age"], df_visiteurs["Type"])

                fig_matrix = px.imshow(
                    cross_age_type.values,
                    x=cross_age_type.columns,
                    y=cross_age_type.index,
                    color_continuous_scale="Blues",
                    text_auto=True,
                    aspect="auto",
                )

                fig_matrix.update_layout(
                    title="Matrice Démographique: Âge × Type de Visiteur",
                    height=400,
                    font=dict(size=12),
                    xaxis_title="Type de Visiteur",
                    yaxis_title="Tranche d'Âge",
                )

                st.plotly_chart(fig_matrix, use_container_width=True)
            else:
                st.info(
                    "Données insuffisantes pour l'analyse démographique (minimum 5 visiteurs)"
                )

        with col2:
            # Analyse de la durée de séjour par centre d'intérêt
            if stats["temps_sejour"] and stats["type_personna"]:
                # Calculer les parts de marché par intérêt
                interests_data = stats["type_personna"]
                total_interests = sum([item[1] for item in interests_data])

                df_interests_share = pd.DataFrame(
                    [
                        {
                            "Intérêt": item[0],
                            "Visiteurs": item[1],
                            "Part de marché (%)": round(
                                (item[1] / total_interests) * 100, 1
                            ),
                        }
                        for item in interests_data
                    ]
                )

                fig_share = px.bar(
                    df_interests_share,
                    x="Part de marché (%)",
                    y="Intérêt",
                    orientation="h",
                    color="Part de marché (%)",
                    color_continuous_scale="Viridis",
                    text="Part de marché (%)",
                )

                fig_share.update_layout(
                    title="Parts de Marché par Centre d'Intérêt",
                    height=400,
                    showlegend=False,
                )

                fig_share.update_traces(texttemplate="%{text}%", textposition="outside")

                st.plotly_chart(fig_share, use_container_width=True)

        # Analyse 2: Performance des contenus par catégorie
        st.subheader(" Performance des Contenus Touristiques")

        col1, col2 = st.columns(2)

        with col1:
            # Analyse ROI par catégorie de page (vues vs nombre de pages)
            if len(vues_pages) > 0:
                category_performance = (
                    df_pages.groupby("Categorie")
                    .agg({"Vues": ["sum", "mean", "count"]})
                    .round(1)
                )

                category_performance.columns = [
                    "Total_Vues",
                    "Vues_Moyenne",
                    "Nb_Pages",
                ]
                category_performance = category_performance.reset_index()
                category_performance["Efficacité"] = (
                    category_performance["Total_Vues"]
                    / category_performance["Nb_Pages"]
                ).round(1)

                fig_efficiency = px.scatter(
                    category_performance,
                    x="Nb_Pages",
                    y="Total_Vues",
                    size="Efficacité",
                    color="Categorie",
                    hover_data=["Vues_Moyenne", "Efficacité"],
                    title="Matrice Performance: Volume vs Efficacité par Catégorie",
                )

                fig_efficiency.update_layout(
                    height=400,
                    xaxis_title="Nombre de Pages",
                    yaxis_title="Total des Vues",
                )

                st.plotly_chart(fig_efficiency, use_container_width=True)

        with col2:
            # Top 10 des pages avec analyse de performance
            top_pages = df_pages.nlargest(10, "Vues")

            fig_top_pages = px.bar(
                top_pages,
                x="Vues",
                y="Page",
                orientation="h",
                color="Categorie",
                color_discrete_sequence=px.colors.qualitative.Set2,
            )

            fig_top_pages.update_layout(
                title="Top 10 des Pages les Plus Consultées",
                height=400,
                yaxis={"categoryorder": "total ascending"},
            )

            st.plotly_chart(fig_top_pages, use_container_width=True)

        # Analyse 3: Indicateurs de performance touristique
        st.subheader(" Indicateurs Clés de Performance (KPI)")

        col1, col2, col3, col4 = st.columns(4)

        # KPI 1: Taux de conversion intérêt/séjour
        with col1:
            if stats["temps_sejour"]:
                long_stays = sum(
                    [item[1] for item in stats["temps_sejour"] if "mois" in item[0]]
                )
                total_visitors = len(visiteurs)
                conversion_rate = (
                    (long_stays / total_visitors * 100) if total_visitors > 0 else 0
                )

                st.metric(
                    "Taux de Séjour Long",
                    f"{conversion_rate:.1f}%",
                    help="Pourcentage de visiteurs restant plus d'un mois",
                )

        # KPI 2: Diversité des intérêts (indice Shannon)
        with col2:
            if stats["type_personna"]:
                interests = [item[1] for item in stats["type_personna"]]
                total = sum(interests)
                if total > 0:
                    shannon_index = -sum(
                        [(p / total) * np.log(p / total) for p in interests if p > 0]
                    )
                    diversity_score = (
                        (shannon_index / np.log(len(interests))) * 100
                        if len(interests) > 1
                        else 0
                    )

                    st.metric(
                        "Diversité Intérêts",
                        f"{diversity_score:.0f}%",
                        help="Indice de diversité des centres d'intérêt (Shannon)",
                    )

        # KPI 3: Engagement moyen par page
        with col3:
            if len(vues_pages) > 0:
                engagement_score = vues_totales / len(vues_pages)
                st.metric(
                    "Engagement Moyen",
                    f"{engagement_score:.1f}",
                    help="Nombre moyen de vues par page créée",
                )

        # KPI 4: Score de maturité touristique
        with col4:
            # Calcul d'un score composite basé sur la diversité des contenus et visiteurs
            category_diversity = (
                len(df_pages["Categorie"].unique()) if len(vues_pages) > 0 else 0
            )
            visitor_diversity = (
                len(df_visiteurs["Type"].unique()) if len(visiteurs) > 0 else 0
            )
            maturity_score = min(
                100,
                (category_diversity * 12.5)
                + (visitor_diversity * 20)
                + min(25, len(visiteurs)),
            )

            st.metric(
                "Maturité Touristique",
                f"{maturity_score:.0f}/100",
                help="Score composite: diversité contenus + profils visiteurs + volume",
            )

    else:
        # Message professionnel pour données manquantes
        st.markdown(
            """
        <div style="
            background: #f7fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 2rem;
            text-align: center;
            margin: 2rem 0;
        ">
            <h3 style="color: #4a5568; margin-bottom: 1rem;">Données Insuffisantes pour l'Analyse</h3>
            <p style="color: #718096; margin-bottom: 1.5rem;">
                Pour générer des analyses pertinentes, veuillez ajouter des données via les sections "Gestion des Visiteurs" et "Gestion des Pages".
            </p>
            <p style="color: #718096; font-size: 0.9rem;">
                <strong>Minimum requis:</strong> 5 visiteurs et 3 pages pour des analyses statistiquement significatives.
            </p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    #  Section des graphiques principaux - Version professionnelle
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
        <div style="
            background: #2d3748;
            color: white;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
        ">
            <h3 style="margin: 0; font-size: 1.1rem; font-weight: 600;"> Performance des Pages</h3>
        </div>
        """,
            unsafe_allow_html=True,
        )

        if vues_pages:
            df_pages = pd.DataFrame(
                vues_pages, columns=["Page", "Catégorie", "Vues", "Dernière vue"]
            )
            df_pages_top = df_pages.head(8)

            fig_pages = px.bar(
                df_pages_top,
                x="Vues",
                y="Page",
                orientation="h",
                color="Catégorie",
                color_discrete_sequence=px.colors.qualitative.Set2,
            )

            fig_pages.update_layout(
                height=400,
                plot_bgcolor="white",
                paper_bgcolor="white",
                font=dict(color="#2d3748", size=11),
                margin=dict(l=0, r=0, t=30, b=0),
                yaxis={"categoryorder": "total ascending"},
            )

            fig_pages.update_traces(marker_line_color="white", marker_line_width=1)

            st.plotly_chart(fig_pages, use_container_width=True)
        else:
            st.info(" Aucune donnée de page disponible")

    with col2:
        st.markdown(
            """
        <div style="
            background: #2d3748;
            color: white;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
        ">
            <h3 style="margin: 0; font-size: 1.1rem; font-weight: 600;"> Segmentation Clientèle</h3>
        </div>
        """,
            unsafe_allow_html=True,
        )

        if stats["type_visiteur"]:
            df_visiteurs = pd.DataFrame(
                stats["type_visiteur"], columns=["Type", "Nombre"]
            )

            fig_visiteurs = px.pie(
                df_visiteurs,
                values="Nombre",
                names="Type",
                color_discrete_sequence=px.colors.qualitative.Set2,
            )

            fig_visiteurs.update_traces(
                textposition="inside",
                textinfo="percent+label",
                hovertemplate="<b>%{label}</b><br>%{value} visiteurs<br>%{percent}<extra></extra>",
                marker=dict(line=dict(color="white", width=2)),
            )

            fig_visiteurs.update_layout(
                height=400,
                plot_bgcolor="white",
                paper_bgcolor="white",
                font=dict(color="#2d3748", size=11),
                margin=dict(l=0, r=0, t=30, b=0),
            )

            st.plotly_chart(fig_visiteurs, use_container_width=True)
        else:
            st.info(" Aucune donnée de visiteur disponible")

elif page == "Gestion des Visiteurs":
    st.header("Gestion des Visiteurs")

    # Formulaire d'ajout de visiteur
    with st.expander("➕ Ajouter un nouveau visiteur", expanded=True):
        col1, col2 = st.columns(2)

        with col1:
            type_visiteur = st.selectbox(
                "Type de visiteur", ["Couple", "Famille", "Solitaire"]
            )

            temps_sejour = st.selectbox(
                "Temps de séjour",
                [
                    "Moins d'une semaine",
                    "1-2 semaines",
                    "Plus d'un mois",
                    "Plus de 3 mois",
                ],
            )

        with col2:
            tranche_age = st.selectbox(
                "Tranche d'âge",
                [
                    "18-25 ans",
                    "26-35 ans",
                    "36-45 ans",
                    "46-55 ans",
                    "56-65 ans",
                    "Plus de 65 ans",
                ],
            )

            type_personna = st.selectbox(
                "Centres d'intérêt",
                [
                    "Culture/Patrimoine",
                    "Randonnée",
                    "Plage",
                    "Gastronomie",
                    "Sport",
                    "Détente",
                ],
            )

        if st.button("Ajouter le visiteur", type="primary"):
            db.add_visiteur(type_visiteur, temps_sejour, tranche_age, type_personna)
            st.success("Visiteur ajouté avec succès!")
            st.rerun()

    st.divider()

    # Liste des visiteurs
    st.subheader("Liste des Visiteurs")
    visiteurs = db.get_visiteurs()

    if visiteurs:
        df_visiteurs = pd.DataFrame(
            visiteurs,
            columns=[
                "ID",
                "Type Visiteur",
                "Temps Séjour",
                "Tranche Âge",
                "Centres d'intérêt",
                "Date Visite",
            ],
        )
        df_visiteurs["Date Visite"] = pd.to_datetime(
            df_visiteurs["Date Visite"]
        ).dt.strftime("%d/%m/%Y %H:%M")

        # Interface pour la gestion des visiteurs
        col1, col2 = st.columns([3, 1])

        with col1:
            st.dataframe(df_visiteurs, use_container_width=True, hide_index=True)

        with col2:
            st.subheader("Actions")

            # Sélection d'un visiteur pour modification/suppression
            visiteur_ids = [v[0] for v in visiteurs]
            selected_id = st.selectbox(
                "Sélectionner un visiteur",
                visiteur_ids,
                format_func=lambda x: f"ID: {x}",
            )

            if selected_id:
                # Boutons d'action
                col_edit, col_delete = st.columns(2)

                with col_edit:
                    if st.button("Modifier", use_container_width=True):
                        st.session_state.edit_visiteur_id = selected_id

                with col_delete:
                    if st.button(
                        "Supprimer", use_container_width=True, type="secondary"
                    ):
                        st.session_state.confirm_delete_visiteur = selected_id

        # Modal de confirmation de suppression
        if "confirm_delete_visiteur" in st.session_state:
            visiteur_data = db.get_visiteur_by_id(
                st.session_state.confirm_delete_visiteur
            )
            if visiteur_data:
                st.error(
                    f"Confirmer la suppression du visiteur ID: {visiteur_data[0]} ?"
                )
                st.write(
                    f"**Type:** {visiteur_data[1]} | **Séjour:** {visiteur_data[2]} | **Âge:** {visiteur_data[3]} | **Intérêts:** {visiteur_data[4]}"
                )

                col1, col2, col3 = st.columns([1, 1, 2])
                with col1:
                    if st.button("Confirmer", type="primary"):
                        # Créer une sauvegarde automatique avant suppression
                        backup_path = backup_manager.auto_backup()
                        if backup_path:
                            st.info(
                                f"Sauvegarde créée: {os.path.basename(backup_path)}"
                            )

                        if db.delete_visiteur(st.session_state.confirm_delete_visiteur):
                            st.success("Visiteur supprimé avec succès!")
                            if "confirm_delete_visiteur" in st.session_state:
                                del st.session_state.confirm_delete_visiteur
                            st.rerun()
                        else:
                            st.error("Erreur lors de la suppression")

                with col2:
                    if st.button(" Annuler"):
                        if "confirm_delete_visiteur" in st.session_state:
                            del st.session_state.confirm_delete_visiteur
                        st.rerun()

        # Modal de modification
        if "edit_visiteur_id" in st.session_state:
            visiteur_data = db.get_visiteur_by_id(st.session_state.edit_visiteur_id)
            if visiteur_data:
                st.subheader(f"Modifier le visiteur ID: {visiteur_data[0]}")

                with st.form("edit_visiteur_form"):
                    col1, col2 = st.columns(2)

                    with col1:
                        edit_type_visiteur = st.selectbox(
                            "Type de visiteur",
                            ["Couple", "Famille", "Solitaire"],
                            index=["Couple", "Famille", "Solitaire"].index(
                                visiteur_data[1]
                            ),
                        )

                        edit_temps_sejour = st.selectbox(
                            "Temps de séjour",
                            [
                                "Moins d'une semaine",
                                "1-2 semaines",
                                "Plus d'un mois",
                                "Plus de 3 mois",
                            ],
                            index=[
                                "Moins d'une semaine",
                                "1-2 semaines",
                                "Plus d'un mois",
                                "Plus de 3 mois",
                            ].index(visiteur_data[2]),
                        )

                    with col2:
                        edit_tranche_age = st.selectbox(
                            "Tranche d'âge",
                            [
                                "18-25 ans",
                                "26-35 ans",
                                "36-45 ans",
                                "46-55 ans",
                                "56-65 ans",
                                "Plus de 65 ans",
                            ],
                            index=[
                                "18-25 ans",
                                "26-35 ans",
                                "36-45 ans",
                                "46-55 ans",
                                "56-65 ans",
                                "Plus de 65 ans",
                            ].index(visiteur_data[3]),
                        )

                        edit_type_personna = st.selectbox(
                            "Centres d'intérêt",
                            [
                                "Culture/Patrimoine",
                                "Randonnée",
                                "Plage",
                                "Gastronomie",
                                "Sport",
                                "Détente",
                            ],
                            index=[
                                "Culture/Patrimoine",
                                "Randonnée",
                                "Plage",
                                "Gastronomie",
                                "Sport",
                                "Détente",
                            ].index(visiteur_data[4]),
                        )

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.form_submit_button(
                            "Sauvegarder", type="primary", use_container_width=True
                        ):
                            if db.update_visiteur(
                                st.session_state.edit_visiteur_id,
                                edit_type_visiteur,
                                edit_temps_sejour,
                                edit_tranche_age,
                                edit_type_personna,
                            ):
                                st.success("Visiteur modifié avec succès!")
                                if "edit_visiteur_id" in st.session_state:
                                    del st.session_state.edit_visiteur_id
                                st.rerun()
                            else:
                                st.error("Erreur lors de la modification")

                    with col2:
                        if st.form_submit_button(" Annuler", use_container_width=True):
                            if "edit_visiteur_id" in st.session_state:
                                del st.session_state.edit_visiteur_id
                            st.rerun()

        # Bouton de téléchargement
        csv = df_visiteurs.to_csv(index=False)
        st.download_button(
            label="📥 Télécharger les données CSV",
            data=csv,
            file_name=f"visiteurs_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
        )
    else:
        st.info("Aucun visiteur enregistré pour le moment")

elif page == "Gestion des Pages":
    st.header("Gestion des Pages")

    # Formulaire d'ajout de vue de page
    with st.expander("➕ Enregistrer une vue de page", expanded=True):
        col1, col2 = st.columns(2)

        with col1:
            nom_page = st.text_input("Nom de la page")

        with col2:
            categorie = st.selectbox(
                "Catégorie",
                [
                    "Accueil",
                    "Activités",
                    "Hébergement",
                    "Restauration",
                    "Culture",
                    "Nature",
                    "Événements",
                    "Pratique",
                ],
            )

        if st.button("Enregistrer la vue", type="primary"):
            if nom_page:
                db.add_vue_page(nom_page, categorie)
                st.success("Vue de page enregistrée!")
                st.rerun()
            else:
                st.error("Veuillez saisir un nom de page")

    st.divider()

    # Statistiques des pages
    st.subheader("Statistiques des Pages")
    vues_pages_with_id = db.get_vues_pages_with_id()

    if vues_pages_with_id:
        df_pages = pd.DataFrame(
            vues_pages_with_id,
            columns=["ID", "Page", "Catégorie", "Vues", "Dernière vue"],
        )
        df_pages["Dernière vue"] = pd.to_datetime(df_pages["Dernière vue"]).dt.strftime(
            "%d/%m/%Y %H:%M"
        )

        # Interface pour la gestion des pages
        col1, col2 = st.columns([2, 1])

        with col1:
            # Afficher le tableau sans l'ID pour les utilisateurs
            df_display = df_pages.drop("ID", axis=1)
            st.dataframe(df_display, use_container_width=True, hide_index=True)

        with col2:
            # Stats par catégorie
            stats_cat = df_pages.groupby("Catégorie")["Vues"].sum().reset_index()
            fig = px.pie(
                stats_cat, values="Vues", names="Catégorie", title="Vues par catégorie"
            )
            st.plotly_chart(fig, use_container_width=True)

        # Section de gestion des pages
        st.subheader("Gestion des Pages")
        col1, col2 = st.columns([2, 1])

        with col1:
            # Sélection d'une page pour modification/suppression
            page_options = [
                (row[0], f"{row[1]} ({row[2]}) - {row[3]} vues")
                for row in vues_pages_with_id
            ]
            selected_page = st.selectbox(
                "Sélectionner une page", page_options, format_func=lambda x: x[1]
            )

        with col2:
            if selected_page:
                # Boutons d'action
                col_edit, col_delete = st.columns(2)

                with col_edit:
                    if st.button("Modifier", key="edit_page", use_container_width=True):
                        st.session_state.edit_page_id = selected_page[0]

                with col_delete:
                    if st.button(
                        "Supprimer",
                        key="delete_page",
                        use_container_width=True,
                        type="secondary",
                    ):
                        st.session_state.confirm_delete_page = selected_page[0]

        # Modal de confirmation de suppression de page
        if "confirm_delete_page" in st.session_state:
            page_data = db.get_page_by_id(st.session_state.confirm_delete_page)
            if page_data:
                st.error(f"Confirmer la suppression de la page ID: {page_data[0]} ?")
                st.write(
                    f"**Page:** {page_data[1]} | **Catégorie:** {page_data[2]} | **Vues:** {page_data[3]}"
                )

                col1, col2, col3 = st.columns([1, 1, 2])
                with col1:
                    if st.button(
                        "Confirmer", key="confirm_delete_page_btn", type="primary"
                    ):
                        # Créer une sauvegarde automatique avant suppression
                        backup_path = backup_manager.auto_backup()
                        if backup_path:
                            st.info(
                                f"Sauvegarde créée: {os.path.basename(backup_path)}"
                            )

                        if db.delete_page(st.session_state.confirm_delete_page):
                            st.success("Page supprimée avec succès!")
                            if "confirm_delete_page" in st.session_state:
                                del st.session_state.confirm_delete_page
                            st.rerun()
                        else:
                            st.error("Erreur lors de la suppression")

                with col2:
                    if st.button(" Annuler", key="cancel_delete_page"):
                        if "confirm_delete_page" in st.session_state:
                            del st.session_state.confirm_delete_page
                        st.rerun()

        # Modal de modification de page
        if "edit_page_id" in st.session_state:
            page_data = db.get_page_by_id(st.session_state.edit_page_id)
            if page_data:
                st.subheader(f"Modifier la page ID: {page_data[0]}")

                categories = [
                    "Accueil",
                    "Activités",
                    "Hébergement",
                    "Restauration",
                    "Culture",
                    "Nature",
                    "Événements",
                    "Pratique",
                ]

                with st.form("edit_page_form"):
                    col1, col2 = st.columns(2)

                    with col1:
                        edit_nom_page = st.text_input(
                            "Nom de la page", value=page_data[1]
                        )

                    with col2:
                        edit_categorie = st.selectbox(
                            "Catégorie",
                            categories,
                            index=(
                                categories.index(page_data[2])
                                if page_data[2] in categories
                                else 0
                            ),
                        )

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.form_submit_button(
                            "Sauvegarder", type="primary", use_container_width=True
                        ):
                            if edit_nom_page:
                                if db.update_page(
                                    st.session_state.edit_page_id,
                                    edit_nom_page,
                                    edit_categorie,
                                ):
                                    st.success("Page modifiée avec succès!")
                                    if "edit_page_id" in st.session_state:
                                        del st.session_state.edit_page_id
                                    st.rerun()
                                else:
                                    st.error("Erreur lors de la modification")
                            else:
                                st.error("Le nom de la page ne peut pas être vide")

                    with col2:
                        if st.form_submit_button(" Annuler", use_container_width=True):
                            if "edit_page_id" in st.session_state:
                                del st.session_state.edit_page_id
                            st.rerun()

        # Analyse temporelle réelle des pages
        st.subheader(" Analyse Temporelle des Pages")

        # Créer une évolution basée sur les vraies données
        if len(vues_pages_with_id) > 0:
            # Convertir les dates en format datetime pour l'analyse
            df_pages_temporal = pd.DataFrame(
                vues_pages_with_id,
                columns=["ID", "Page", "Catégorie", "Vues", "Dernière vue"],
            )
            df_pages_temporal["Date"] = pd.to_datetime(
                df_pages_temporal["Dernière vue"]
            )

            # Grouper par date et sommer les vues
            df_evolution = (
                df_pages_temporal.groupby(df_pages_temporal["Date"].dt.date)["Vues"]
                .sum()
                .reset_index()
            )
            df_evolution.columns = ["Date", "Vues_Cumulées"]

            # Si nous avons suffisamment de données temporelles
            if len(df_evolution) > 1:
                fig = px.line(
                    df_evolution,
                    x="Date",
                    y="Vues_Cumulées",
                    title="Évolution Réelle des Vues par Date",
                    markers=True,
                )
                fig.update_layout(
                    height=400, xaxis_title="Date", yaxis_title="Nombre de Vues"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                # Graphique alternatif : distribution des vues par catégorie
                category_views = (
                    df_pages_temporal.groupby("Catégorie")["Vues"].sum().reset_index()
                )

                fig = px.bar(
                    category_views,
                    x="Catégorie",
                    y="Vues",
                    title="Distribution des Vues par Catégorie de Page",
                    color="Vues",
                    color_continuous_scale="Blues",
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info(" Aucune donnée temporelle disponible pour l'analyse")

    else:
        st.info("Aucune donnée de page disponible")

elif page == "Analyses Détaillées":
    st.header("Analyses Détaillées")

    stats = db.get_stats_visiteurs()

    if any(stats.values()):
        # Graphiques détaillés
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Types de Visiteurs")
            if stats["type_visiteur"]:
                df = pd.DataFrame(stats["type_visiteur"], columns=["Type", "Nombre"])
                fig = px.bar(
                    df,
                    x="Type",
                    y="Nombre",
                    color="Type",
                    title="Répartition des types de visiteurs",
                )
                st.plotly_chart(fig, use_container_width=True)

            st.subheader("Durée de Séjour")
            if stats["temps_sejour"]:
                df = pd.DataFrame(stats["temps_sejour"], columns=["Durée", "Nombre"])
                fig = px.bar(
                    df,
                    x="Durée",
                    y="Nombre",
                    color="Durée",
                    title="Répartition des durées de séjour",
                )
                fig.update_xaxes(tickangle=45)
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Tranches d'Âge")
            if stats["tranche_age"]:
                df = pd.DataFrame(stats["tranche_age"], columns=["Âge", "Nombre"])
                fig = px.pie(
                    df,
                    values="Nombre",
                    names="Âge",
                    title="Répartition par tranche d'âge",
                )
                st.plotly_chart(fig, use_container_width=True)

            st.subheader("Centres d'Intérêt")
            if stats["type_personna"]:
                df = pd.DataFrame(stats["type_personna"], columns=["Intérêt", "Nombre"])
                fig = px.bar(
                    df,
                    x="Intérêt",
                    y="Nombre",
                    color="Intérêt",
                    title="Centres d'intérêt des visiteurs",
                )
                fig.update_xaxes(tickangle=45)
                st.plotly_chart(fig, use_container_width=True)

        # Analyse croisée
        st.divider()
        st.subheader("Analyse Croisée")

        visiteurs = db.get_visiteurs()
        if visiteurs:
            df_visiteurs = pd.DataFrame(
                visiteurs,
                columns=[
                    "ID",
                    "Type Visiteur",
                    "Temps Séjour",
                    "Tranche Âge",
                    "Centres d'intérêt",
                    "Date Visite",
                ],
            )

            # Heatmap des corrélations
            col1, col2 = st.columns(2)

            with col1:
                # Croiser type visiteur et centres d'intérêt
                cross_tab = pd.crosstab(
                    df_visiteurs["Type Visiteur"], df_visiteurs["Centres d'intérêt"]
                )
                fig = px.imshow(
                    cross_tab,
                    text_auto=True,
                    aspect="auto",
                    title="Type de Visiteur vs Centres d'Intérêt",
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                # Croiser âge et durée de séjour
                cross_tab2 = pd.crosstab(
                    df_visiteurs["Tranche Âge"], df_visiteurs["Temps Séjour"]
                )
                fig = px.imshow(
                    cross_tab2,
                    text_auto=True,
                    aspect="auto",
                    title="Tranche d'Âge vs Temps de Séjour",
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)

    else:
        st.info(
            "Aucune donnée disponible pour l'analyse. Ajoutez des visiteurs pour voir les statistiques."
        )

elif page == "Suppression en Masse":
    st.header("Suppression en Masse")
    st.warning(
        "**Attention:** Ces actions sont irréversibles. Assurez-vous d'avoir sauvegardé vos données importantes."
    )

    # Informations sur les données actuelles
    visiteurs = db.get_visiteurs()
    vues_pages_with_id = db.get_vues_pages_with_id()
    vues_totales = db.get_vues_totales()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Visiteurs", len(visiteurs))
    with col2:
        st.metric("Pages", len(vues_pages_with_id))
    with col3:
        st.metric("Vues totales", vues_totales)

    st.divider()

    # Section de suppression des visiteurs
    with st.expander("Suppression des Visiteurs", expanded=False):
        st.subheader("Supprimer des visiteurs par critères")

        col1, col2 = st.columns(2)
        with col1:
            filter_type = st.selectbox(
                "Filtrer par type de visiteur",
                ["Tous", "Couple", "Famille", "Solitaire"],
                key="filter_visiteur_type",
            )

            filter_sejour = st.selectbox(
                "Filtrer par temps de séjour",
                [
                    "Tous",
                    "Moins d'une semaine",
                    "1-2 semaines",
                    "Plus d'un mois",
                    "Plus de 3 mois",
                ],
                key="filter_sejour",
            )

        with col2:
            filter_age = st.selectbox(
                "Filtrer par tranche d'âge",
                [
                    "Tous",
                    "18-25 ans",
                    "26-35 ans",
                    "36-45 ans",
                    "46-55 ans",
                    "56-65 ans",
                    "Plus de 65 ans",
                ],
                key="filter_age",
            )

            filter_personna = st.selectbox(
                "Filtrer par centres d'intérêt",
                [
                    "Tous",
                    "Culture/Patrimoine",
                    "Randonnée",
                    "Plage",
                    "Gastronomie",
                    "Sport",
                    "Détente",
                ],
                key="filter_personna",
            )

        # Compter les visiteurs qui correspondent aux critères
        if visiteurs:
            df_visiteurs = pd.DataFrame(
                visiteurs,
                columns=[
                    "ID",
                    "Type Visiteur",
                    "Temps Séjour",
                    "Tranche Âge",
                    "Centres d'intérêt",
                    "Date Visite",
                ],
            )

            # Appliquer les filtres
            filtered_df = df_visiteurs.copy()
            if filter_type != "Tous":
                filtered_df = filtered_df[filtered_df["Type Visiteur"] == filter_type]
            if filter_sejour != "Tous":
                filtered_df = filtered_df[filtered_df["Temps Séjour"] == filter_sejour]
            if filter_age != "Tous":
                filtered_df = filtered_df[filtered_df["Tranche Âge"] == filter_age]
            if filter_personna != "Tous":
                filtered_df = filtered_df[
                    filtered_df["Centres d'intérêt"] == filter_personna
                ]

            st.info(
                f"{len(filtered_df)} visiteur(s) correspondent aux critères sélectionnés"
            )

            if len(filtered_df) > 0:
                st.dataframe(filtered_df, use_container_width=True, hide_index=True)

                if st.button(
                    "Supprimer les visiteurs filtrés",
                    type="secondary",
                    key="delete_filtered_visitors",
                ):
                    st.session_state.confirm_mass_delete_visitors = filtered_df[
                        "ID"
                    ].tolist()

    # Section de suppression des pages
    with st.expander("Suppression des Pages", expanded=False):
        st.subheader("Supprimer des pages par catégorie")

        if vues_pages_with_id:
            df_pages = pd.DataFrame(
                vues_pages_with_id,
                columns=["ID", "Page", "Catégorie", "Vues", "Dernière vue"],
            )
            categories = df_pages["Catégorie"].unique().tolist()

            selected_categories = st.multiselect(
                "Sélectionner les catégories à supprimer",
                categories,
                key="categories_to_delete",
            )

            if selected_categories:
                filtered_pages = df_pages[
                    df_pages["Catégorie"].isin(selected_categories)
                ]
                st.info(f"{len(filtered_pages)} page(s) seront supprimées")

                st.dataframe(
                    filtered_pages.drop("ID", axis=1),
                    use_container_width=True,
                    hide_index=True,
                )

                if st.button(
                    "Supprimer les pages sélectionnées",
                    type="secondary",
                    key="delete_selected_pages",
                ):
                    st.session_state.confirm_mass_delete_pages = filtered_pages[
                        "ID"
                    ].tolist()

    # Section de remise à zéro complète
    with st.expander("Remise à Zéro Complète", expanded=False):
        st.error(
            "**DANGER:** Cette action supprimera TOUTES les données de l'application"
        )

        col1, col2 = st.columns([2, 1])
        with col1:
            st.write("Cette action supprimera :")
            st.write("- Tous les visiteurs enregistrés")
            st.write("- Toutes les pages et leurs statistiques")
            st.write("- Le compteur de vues totales (remis à 0)")

        with col2:
            if st.button("TOUT SUPPRIMER", type="secondary", key="reset_all_data"):
                st.session_state.confirm_reset_all = True

    # Modals de confirmation
    if "confirm_mass_delete_visitors" in st.session_state:
        visitor_ids = st.session_state.confirm_mass_delete_visitors
        st.error(f"Confirmer la suppression de {len(visitor_ids)} visiteur(s) ?")

        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button(
                "Confirmer la suppression",
                type="primary",
                key="confirm_mass_delete_visitors_btn",
            ):
                # Créer une sauvegarde automatique avant suppression en masse
                backup_path = backup_manager.auto_backup()
                if backup_path:
                    st.info(f"Sauvegarde créée: {os.path.basename(backup_path)}")

                deleted_count = 0
                for visitor_id in visitor_ids:
                    if db.delete_visiteur(visitor_id):
                        deleted_count += 1

                st.success(f"{deleted_count} visiteur(s) supprimé(s) avec succès!")
                if "confirm_mass_delete_visitors" in st.session_state:
                    del st.session_state.confirm_mass_delete_visitors
                st.rerun()

        with col2:
            if st.button(" Annuler", key="cancel_mass_delete_visitors"):
                if "confirm_mass_delete_visitors" in st.session_state:
                    del st.session_state.confirm_mass_delete_visitors
                st.rerun()

    if "confirm_mass_delete_pages" in st.session_state:
        page_ids = st.session_state.confirm_mass_delete_pages
        st.error(f"Confirmer la suppression de {len(page_ids)} page(s) ?")

        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button(
                "Confirmer la suppression",
                type="primary",
                key="confirm_mass_delete_pages_btn",
            ):
                # Créer une sauvegarde automatique avant suppression en masse
                backup_path = backup_manager.auto_backup()
                if backup_path:
                    st.info(f"Sauvegarde créée: {os.path.basename(backup_path)}")

                deleted_count = 0
                for page_id in page_ids:
                    if db.delete_page(page_id):
                        deleted_count += 1

                st.success(f"{deleted_count} page(s) supprimée(s) avec succès!")
                if "confirm_mass_delete_pages" in st.session_state:
                    del st.session_state.confirm_mass_delete_pages
                st.rerun()

        with col2:
            if st.button(" Annuler", key="cancel_mass_delete_pages"):
                if "confirm_mass_delete_pages" in st.session_state:
                    del st.session_state.confirm_mass_delete_pages
                st.rerun()

    if "confirm_reset_all" in st.session_state:
        st.error(
            "**DERNIÈRE CONFIRMATION** - Vous allez supprimer TOUTES les données !"
        )
        st.write("Tapez 'SUPPRIMER TOUT' pour confirmer :")

        confirmation_text = st.text_input("Confirmation", key="reset_confirmation_text")

        col1, col2 = st.columns(2)
        with col1:
            if st.button(
                "CONFIRMER LA SUPPRESSION TOTALE",
                type="primary",
                key="final_reset_confirm",
            ):
                if confirmation_text == "SUPPRIMER TOUT":
                    # Créer une sauvegarde automatique avant remise à zéro complète
                    backup_path = backup_manager.auto_backup()
                    if backup_path:
                        st.info(
                            f"Sauvegarde de sécurité créée: {os.path.basename(backup_path)}"
                        )

                    # Supprimer toutes les données
                    if db.reset_all_data():
                        st.success("Toutes les données ont été supprimées!")
                        if "confirm_reset_all" in st.session_state:
                            del st.session_state.confirm_reset_all
                        st.rerun()
                    else:
                        st.error(" Erreur lors de la suppression des données")
                else:
                    st.error(" Texte de confirmation incorrect")

        with col2:
            if st.button(" Annuler", key="cancel_reset_all"):
                if "confirm_reset_all" in st.session_state:
                    del st.session_state.confirm_reset_all
                st.rerun()

elif page == "Gestion des Sauvegardes":
    st.header("Gestion des Sauvegardes")
    st.info(
        "💡 **Conseil:** Les sauvegardes automatiques sont créées avant chaque suppression de données"
    )

    # Bouton pour créer une sauvegarde manuelle
    col1, col2 = st.columns([2, 1])
    with col1:
        backup_name = st.text_input(
            "Nom de la sauvegarde (optionnel)",
            placeholder="Ex: avant_modification_importante",
        )
    with col2:
        st.write("")  # Espacement
        if st.button("Créer une sauvegarde", type="primary", use_container_width=True):
            if backup_name:
                custom_name = (
                    f"{backup_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
                )
                backup_path = backup_manager.create_backup(custom_name)
            else:
                backup_path = backup_manager.create_backup()

            if backup_path:
                st.success(f"Sauvegarde créée: {os.path.basename(backup_path)}")
            else:
                st.error(" Erreur lors de la création de la sauvegarde")

    st.divider()

    # Liste des sauvegardes existantes
    st.subheader("Sauvegardes Existantes")
    backups = backup_manager.list_backups()

    if backups:
        for i, backup in enumerate(backups):
            with st.expander(
                f"{backup['name']} - {backup['date'].strftime('%d/%m/%Y %H:%M:%S')}",
                expanded=False,
            ):
                col1, col2, col3 = st.columns([2, 1, 1])

                with col1:
                    st.write(f"**Taille:** {backup['size'] / 1024:.1f} KB")
                    st.write(
                        f"**Date:** {backup['date'].strftime('%d/%m/%Y à %H:%M:%S')}"
                    )
                    st.write(f"**Chemin:** {backup['path']}")

                with col2:
                    if st.button(
                        "Restaurer",
                        key=f"restore_{i}",
                        type="secondary",
                        use_container_width=True,
                    ):
                        st.session_state[f"confirm_restore_{i}"] = backup["path"]

                with col3:
                    if st.button(
                        "Supprimer",
                        key=f"delete_backup_{i}",
                        use_container_width=True,
                    ):
                        st.session_state[f"confirm_delete_backup_{i}"] = backup["path"]

                # Modal de confirmation de restauration
                if f"confirm_restore_{i}" in st.session_state:
                    st.warning(
                        "**Attention:** La restauration remplacera toutes les données actuelles par celles de cette sauvegarde!"
                    )

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(
                            "Confirmer la restauration",
                            key=f"confirm_restore_btn_{i}",
                            type="primary",
                        ):
                            if backup_manager.restore_backup(
                                st.session_state[f"confirm_restore_{i}"]
                            ):
                                st.success("Sauvegarde restaurée avec succès!")
                                # Nettoyer le cache pour recharger les données
                                st.cache_resource.clear()
                                if f"confirm_restore_{i}" in st.session_state:
                                    del st.session_state[f"confirm_restore_{i}"]
                                st.rerun()
                            else:
                                st.error(" Erreur lors de la restauration")

                    with col2:
                        if st.button(" Annuler", key=f"cancel_restore_{i}"):
                            if f"confirm_restore_{i}" in st.session_state:
                                del st.session_state[f"confirm_restore_{i}"]
                            st.rerun()

                # Modal de confirmation de suppression de sauvegarde
                if f"confirm_delete_backup_{i}" in st.session_state:
                    st.error(
                        f"Confirmer la suppression de la sauvegarde {backup['name']} ?"
                    )

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(
                            "Confirmer",
                            key=f"confirm_delete_backup_btn_{i}",
                            type="primary",
                        ):
                            if backup_manager.delete_backup(
                                st.session_state[f"confirm_delete_backup_{i}"]
                            ):
                                st.success("Sauvegarde supprimée!")
                                if f"confirm_delete_backup_{i}" in st.session_state:
                                    del st.session_state[f"confirm_delete_backup_{i}"]
                                st.rerun()
                            else:
                                st.error(" Erreur lors de la suppression")

                    with col2:
                        if st.button(" Annuler", key=f"cancel_delete_backup_{i}"):
                            if f"confirm_delete_backup_{i}" in st.session_state:
                                del st.session_state[f"confirm_delete_backup_{i}"]
                            st.rerun()

        # Nettoyage automatique des anciennes sauvegardes
        st.divider()
        st.subheader("Nettoyage Automatique")

        col1, col2 = st.columns([2, 1])
        with col1:
            st.write(f"**Nombre total de sauvegardes:** {len(backups)}")
            st.write(
                "Le nettoyage automatique garde les 10 sauvegardes les plus récentes"
            )

        with col2:
            if st.button(
                "Nettoyer les anciennes sauvegardes",
                type="secondary",
                use_container_width=True,
            ):
                deleted_count = backup_manager.cleanup_old_backups(keep_count=10)
                if deleted_count > 0:
                    st.success(
                        f"{deleted_count} ancienne(s) sauvegarde(s) supprimée(s)"
                    )
                    st.rerun()
                else:
                    st.info("Aucune sauvegarde à nettoyer")

    else:
        st.info(
            "Aucune sauvegarde trouvée. Les sauvegardes automatiques seront créées lors des suppressions de données."
        )

# Footer
st.divider()
st.markdown(
    """
<div style="text-align: center; color: #666; padding: 1rem;">
    <p style="margin-bottom: 0.5rem;">Bureau d'Étude - Tourisme Castagniccia Casinca | Données mises à jour en temps réel</p>
    <p style="margin-bottom: 1rem;">Total des vues du site: <strong>{}</strong></p>
    <hr style="border: none; border-top: 1px solid #e2e8f0; margin: 1rem 0;">
    <p style="margin-bottom: 0.2rem; font-size: 0.9rem; color: #718096;">
        Créé par <strong>Anthony Menghi - antocreadev</strong>
    </p>
    <p style="margin: 0; font-size: 0.8rem;">
        <a href="https://www.antocrea.dev/" target="_blank" style="color: #3182ce; text-decoration: none;">
            🌐 Site web : www.antocrea.dev
        </a>
    </p>
</div>
""".format(
        db.get_vues_totales()
    ),
    unsafe_allow_html=True,
)
