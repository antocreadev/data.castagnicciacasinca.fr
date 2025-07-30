from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import json
from database import DatabaseManager
from backup_manager import BackupManager

# Initialisation de l'API
app = FastAPI(
    title="API Bureau d'Étude - Office de Tourisme",
    description="API REST pour collecter les données de fréquentation et profils visiteurs",
    version="1.0.0",
)

# Configuration CORS pour permettre les appels depuis un site web
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifiez les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialisation des gestionnaires
db = DatabaseManager()
backup_manager = BackupManager()


# Modèles Pydantic pour la validation des données
class VisiteurCreate(BaseModel):
    type_visiteur: str = Field(
        ..., description="Type de visiteur", pattern="^(Couple|Famille|Solitaire)$"
    )
    temps_sejour: str = Field(
        ...,
        description="Temps de séjour",
        pattern="^(Moins d'une semaine|1-2 semaines|Plus d'un mois|Plus de 3 mois)$",
    )
    tranche_age: str = Field(
        ...,
        description="Tranche d'âge",
        pattern="^(18-25 ans|26-35 ans|36-45 ans|46-55 ans|56-65 ans|Plus de 65 ans)$",
    )
    type_personna: str = Field(
        ...,
        description="Centres d'intérêt",
        pattern="^(Culture/Patrimoine|Randonnée|Plage|Gastronomie|Sport|Détente)$",
    )

    class Config:
        json_schema_extra = {
            "example": {
                "type_visiteur": "Couple",
                "temps_sejour": "1-2 semaines",
                "tranche_age": "26-35 ans",
                "type_personna": "Culture/Patrimoine",
            }
        }


class PageVue(BaseModel):
    nom_page: str = Field(
        ..., description="Nom de la page visitée", min_length=1, max_length=255
    )
    categorie: str = Field(
        ...,
        description="Catégorie de la page",
        pattern="^(Accueil|Activités|Hébergement|Restauration|Culture|Nature|Événements|Pratique)$",
    )

    class Config:
        json_schema_extra = {
            "example": {"nom_page": "Randonnées GR20", "categorie": "Activités"}
        }


class VisiteurResponse(BaseModel):
    id: int
    type_visiteur: str
    temps_sejour: str
    tranche_age: str
    type_personna: str
    date_visite: str


class PageResponse(BaseModel):
    id: int
    nom_page: str
    categorie: str
    nombre_vues: int
    date_derniere_vue: str


class StatsResponse(BaseModel):
    vues_totales: int
    nombre_visiteurs: int
    nombre_pages: int
    derniere_activite: Optional[str]


# Routes API


@app.get("/", tags=["Info"])
async def root():
    """Point d'entrée de l'API"""
    return {
        "message": "API Bureau d'Étude - Office de Tourisme",
        "version": "1.0.0",
        "endpoints": {
            "POST /visiteur": "Ajouter un visiteur",
            "POST /page-vue": "Enregistrer une vue de page",
            "POST /vue-totale": "Incrémenter les vues totales",
            "GET /stats": "Obtenir les statistiques",
            "GET /visiteurs": "Lister tous les visiteurs",
            "GET /pages": "Lister toutes les pages",
        },
    }


@app.post("/visiteur", response_model=dict, tags=["Visiteurs"])
async def ajouter_visiteur(visiteur: VisiteurCreate):
    """
    Ajouter un nouveau visiteur

    Envoie les données d'un visiteur pour analyse statistique.
    Toutes les valeurs doivent correspondre aux options prédéfinies.
    """
    try:
        db.add_visiteur(
            visiteur.type_visiteur,
            visiteur.temps_sejour,
            visiteur.tranche_age,
            visiteur.type_personna,
        )
        return {
            "success": True,
            "message": "Visiteur ajouté avec succès",
            "data": visiteur.dict(),
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erreur lors de l'ajout du visiteur: {str(e)}"
        )


@app.post("/page-vue", response_model=dict, tags=["Pages"])
async def enregistrer_vue_page(page: PageVue):
    """
    Enregistrer une vue de page

    Comptabilise la visite d'une page du site web.
    Si la page existe déjà, incrémente son compteur.
    """
    try:
        db.add_vue_page(page.nom_page, page.categorie)
        return {
            "success": True,
            "message": "Vue de page enregistrée avec succès",
            "data": page.dict(),
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'enregistrement de la vue: {str(e)}",
        )


@app.post("/vue-totale", response_model=dict, tags=["Statistiques"])
async def incrementer_vues_totales():
    """
    Incrémenter le compteur de vues totales du site

    À appeler à chaque visite sur le site principal.
    """
    try:
        db.increment_vues_totales()
        vues_totales = db.get_vues_totales()
        return {
            "success": True,
            "message": "Vue totale incrémentée",
            "vues_totales": vues_totales,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erreur lors de l'incrémentation: {str(e)}"
        )


@app.get("/stats", response_model=StatsResponse, tags=["Statistiques"])
async def obtenir_statistiques():
    """
    Obtenir les statistiques générales du site

    Retourne un résumé des métriques principales.
    """
    try:
        vues_totales = db.get_vues_totales()
        visiteurs = db.get_visiteurs()
        pages = db.get_vues_pages()

        derniere_activite = None
        if visiteurs:
            derniere_activite = visiteurs[0][5]  # Date du visiteur le plus récent

        return StatsResponse(
            vues_totales=vues_totales,
            nombre_visiteurs=len(visiteurs),
            nombre_pages=len(pages),
            derniere_activite=derniere_activite,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la récupération des stats: {str(e)}",
        )


@app.get("/visiteurs", response_model=List[VisiteurResponse], tags=["Visiteurs"])
async def lister_visiteurs(limit: int = 100):
    """
    Lister tous les visiteurs

    Retourne la liste des visiteurs enregistrés (limité à 100 par défaut).
    """
    try:
        visiteurs = db.get_visiteurs()
        visiteurs_limited = visiteurs[:limit]

        return [
            VisiteurResponse(
                id=v[0],
                type_visiteur=v[1],
                temps_sejour=v[2],
                tranche_age=v[3],
                type_personna=v[4],
                date_visite=v[5],
            )
            for v in visiteurs_limited
        ]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la récupération des visiteurs: {str(e)}",
        )


@app.get("/pages", response_model=List[PageResponse], tags=["Pages"])
async def lister_pages():
    """
    Lister toutes les pages avec leurs statistiques

    Retourne la liste des pages visitées avec le nombre de vues.
    """
    try:
        pages = db.get_vues_pages_with_id()

        return [
            PageResponse(
                id=p[0],
                nom_page=p[1],
                categorie=p[2],
                nombre_vues=p[3],
                date_derniere_vue=p[4],
            )
            for p in pages
        ]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la récupération des pages: {str(e)}",
        )


# Routes pour le tracking avancé
@app.post("/tracking/bulk", response_model=dict, tags=["Tracking Avancé"])
async def tracking_bulk(request: Request):
    """
    Envoie de données en lot (bulk)

    Permet d'envoyer plusieurs événements en une seule requête.
    Format JSON: {"visiteurs": [...], "pages": [...], "vues_totales": number}
    """
    try:
        data = await request.json()

        added_visiteurs = 0
        added_pages = 0

        # Traiter les visiteurs
        if "visiteurs" in data and isinstance(data["visiteurs"], list):
            for visiteur_data in data["visiteurs"]:
                try:
                    visiteur = VisiteurCreate(**visiteur_data)
                    db.add_visiteur(
                        visiteur.type_visiteur,
                        visiteur.temps_sejour,
                        visiteur.tranche_age,
                        visiteur.type_personna,
                    )
                    added_visiteurs += 1
                except Exception as e:
                    print(f"Erreur visiteur: {e}")

        # Traiter les vues de pages
        if "pages" in data and isinstance(data["pages"], list):
            for page_data in data["pages"]:
                try:
                    page = PageVue(**page_data)
                    db.add_vue_page(page.nom_page, page.categorie)
                    added_pages += 1
                except Exception as e:
                    print(f"Erreur page: {e}")

        # Traiter les vues totales
        if "vues_totales" in data and isinstance(data["vues_totales"], int):
            for _ in range(data["vues_totales"]):
                db.increment_vues_totales()

        return {
            "success": True,
            "message": "Données en lot traitées",
            "visiteurs_ajoutes": added_visiteurs,
            "pages_ajoutees": added_pages,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erreur lors du traitement en lot: {str(e)}"
        )


@app.get("/health", tags=["System"])
async def health_check():
    """
    Vérification de l'état de l'API

    Endpoint pour vérifier que l'API fonctionne correctement.
    """
    try:
        # Test simple de la base de données
        vues_totales = db.get_vues_totales()
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "database": "connected",
            "vues_totales": vues_totales,
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service indisponible: {str(e)}")


# Route pour obtenir la documentation des valeurs valides
@app.get("/valeurs-valides", tags=["Documentation"])
async def valeurs_valides():
    """
    Obtenir les valeurs valides pour chaque champ

    Retourne les listes des valeurs acceptées pour créer des formulaires dynamiques.
    """
    return {
        "type_visiteur": ["Couple", "Famille", "Solitaire"],
        "temps_sejour": [
            "Moins d'une semaine",
            "1-2 semaines",
            "Plus d'un mois",
            "Plus de 3 mois",
        ],
        "tranche_age": [
            "18-25 ans",
            "26-35 ans",
            "36-45 ans",
            "46-55 ans",
            "56-65 ans",
            "Plus de 65 ans",
        ],
        "type_personna": [
            "Culture/Patrimoine",
            "Randonnée",
            "Plage",
            "Gastronomie",
            "Sport",
            "Détente",
        ],
        "categories_pages": [
            "Accueil",
            "Activités",
            "Hébergement",
            "Restauration",
            "Culture",
            "Nature",
            "Événements",
            "Pratique",
        ],
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
