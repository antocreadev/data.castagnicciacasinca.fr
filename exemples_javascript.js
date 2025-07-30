// ===================================================================
// EXEMPLES D'UTILISATION DE L'API - BUREAU D'ÉTUDE OFFICE DE TOURISME
// ===================================================================

// Configuration de base
const API_BASE_URL = "http://localhost:8000";

// ===================================================================
// 1. INCRÉMENTER LES VUES TOTALES (à chaque visite de page)
// ===================================================================

/**
 * À appeler sur chaque page de votre site pour compter les visites
 */
async function incrementerVuesTotales() {
  try {
    const response = await fetch(`${API_BASE_URL}/vue-totale`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });

    const result = await response.json();

    if (result.success) {
      console.log(`✅ Vue totale incrémentée. Total: ${result.vues_totales}`);
    }
  } catch (error) {
    console.error(
      "❌ Erreur lors de l'incrémentation des vues totales:",
      error
    );
  }
}

// Appel automatique à chaque chargement de page
document.addEventListener("DOMContentLoaded", incrementerVuesTotales);

// ===================================================================
// 2. ENREGISTRER UNE VUE DE PAGE SPÉCIFIQUE
// ===================================================================

/**
 * Enregistre la visite d'une page spécifique avec sa catégorie
 * @param {string} nomPage - Nom de la page visitée
 * @param {string} categorie - Catégorie de la page
 */
async function enregistrerVuePage(nomPage, categorie) {
  try {
    const response = await fetch(`${API_BASE_URL}/page-vue`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        nom_page: nomPage,
        categorie: categorie,
      }),
    });

    const result = await response.json();

    if (result.success) {
      console.log(`✅ Vue de page enregistrée: ${nomPage} (${categorie})`);
    }
  } catch (error) {
    console.error(
      "❌ Erreur lors de l'enregistrement de la vue de page:",
      error
    );
  }
}

// Exemples d'utilisation automatique selon la page
function detecterEtEnregistrerPage() {
  const path = window.location.pathname;
  const title = document.title;

  // Exemples de mapping page -> catégorie
  if (path.includes("/activites") || path.includes("/randonnees")) {
    enregistrerVuePage(title || "Activités", "Activités");
  } else if (path.includes("/hebergement") || path.includes("/hotels")) {
    enregistrerVuePage(title || "Hébergement", "Hébergement");
  } else if (path.includes("/restaurants") || path.includes("/gastronomie")) {
    enregistrerVuePage(title || "Restauration", "Restauration");
  } else if (path.includes("/culture") || path.includes("/patrimoine")) {
    enregistrerVuePage(title || "Culture", "Culture");
  } else if (path.includes("/nature") || path.includes("/plages")) {
    enregistrerVuePage(title || "Nature", "Nature");
  } else if (path.includes("/evenements") || path.includes("/agenda")) {
    enregistrerVuePage(title || "Événements", "Événements");
  } else if (path === "/" || path === "/accueil") {
    enregistrerVuePage("Accueil", "Accueil");
  } else {
    enregistrerVuePage(title || "Page générale", "Pratique");
  }
}

// Appel automatique
document.addEventListener("DOMContentLoaded", detecterEtEnregistrerPage);

// ===================================================================
// 3. FORMULAIRE DE PROFIL VISITEUR
// ===================================================================

/**
 * Envoie les données d'un visiteur depuis un formulaire
 * @param {Object} donneesVisiteur - Données du visiteur
 */
async function ajouterVisiteur(donneesVisiteur) {
  try {
    const response = await fetch(`${API_BASE_URL}/visiteur`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(donneesVisiteur),
    });

    const result = await response.json();

    if (result.success) {
      console.log("✅ Visiteur ajouté avec succès");
      return true;
    } else {
      console.error("❌ Erreur côté serveur:", result.message);
      return false;
    }
  } catch (error) {
    console.error("❌ Erreur lors de l'ajout du visiteur:", error);
    return false;
  }
}

// Exemple de formulaire HTML à intégrer sur votre site
function creerFormulaireVisiteur() {
  return `
    <div id="formulaire-visiteur">
        <h3>Dites-nous en plus sur votre visite !</h3>
        <form id="form-visiteur">
            <div>
                <label>Vous visitez :</label>
                <select name="type_visiteur" required>
                    <option value="">Sélectionnez...</option>
                    <option value="Couple">En couple</option>
                    <option value="Famille">En famille</option>
                    <option value="Solitaire">Seul(e)</option>
                </select>
            </div>
            
            <div>
                <label>Durée de votre séjour :</label>
                <select name="temps_sejour" required>
                    <option value="">Sélectionnez...</option>
                    <option value="Moins d'une semaine">Moins d'une semaine</option>
                    <option value="1-2 semaines">1-2 semaines</option>
                    <option value="Plus d'un mois">Plus d'un mois</option>
                    <option value="Plus de 3 mois">Plus de 3 mois</option>
                </select>
            </div>
            
            <div>
                <label>Votre tranche d'âge :</label>
                <select name="tranche_age" required>
                    <option value="">Sélectionnez...</option>
                    <option value="18-25 ans">18-25 ans</option>
                    <option value="26-35 ans">26-35 ans</option>
                    <option value="36-45 ans">36-45 ans</option>
                    <option value="46-55 ans">46-55 ans</option>
                    <option value="56-65 ans">56-65 ans</option>
                    <option value="Plus de 65 ans">Plus de 65 ans</option>
                </select>
            </div>
            
            <div>
                <label>Ce qui vous intéresse le plus :</label>
                <select name="type_personna" required>
                    <option value="">Sélectionnez...</option>
                    <option value="Culture/Patrimoine">Culture & Patrimoine</option>
                    <option value="Randonnée">Randonnée</option>
                    <option value="Plage">Plage</option>
                    <option value="Gastronomie">Gastronomie</option>
                    <option value="Sport">Sport</option>
                    <option value="Détente">Détente</option>
                </select>
            </div>
            
            <button type="submit">Envoyer</button>
        </form>
        <div id="message-succes" style="display:none; color:green;">
            Merci pour vos informations ! 🎉
        </div>
    </div>
    `;
}

// Gestionnaire de soumission du formulaire
function initialiserFormulaireVisiteur() {
  document
    .getElementById("form-visiteur")
    .addEventListener("submit", async (e) => {
      e.preventDefault();

      const formData = new FormData(e.target);
      const donneesVisiteur = {
        type_visiteur: formData.get("type_visiteur"),
        temps_sejour: formData.get("temps_sejour"),
        tranche_age: formData.get("tranche_age"),
        type_personna: formData.get("type_personna"),
      };

      const succes = await ajouterVisiteur(donneesVisiteur);

      if (succes) {
        document.getElementById("form-visiteur").style.display = "none";
        document.getElementById("message-succes").style.display = "block";
      } else {
        alert("Erreur lors de l'envoi. Veuillez réessayer.");
      }
    });
}

// ===================================================================
// 4. TRACKING AVANCÉ EN LOT
// ===================================================================

/**
 * Envoie plusieurs données en une seule requête (plus efficace)
 * @param {Object} donneesLot - Objet contenant visiteurs, pages, vues_totales
 */
async function envoyerDonneesEnLot(donneesLot) {
  try {
    const response = await fetch(`${API_BASE_URL}/tracking/bulk`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(donneesLot),
    });

    const result = await response.json();

    if (result.success) {
      console.log("✅ Données en lot envoyées:", result);
    }
  } catch (error) {
    console.error("❌ Erreur lors de l'envoi en lot:", error);
  }
}

// Exemple d'utilisation pour envoyer plusieurs événements
async function exempleEnvoiLot() {
  const donneesLot = {
    visiteurs: [
      {
        type_visiteur: "Couple",
        temps_sejour: "1-2 semaines",
        tranche_age: "26-35 ans",
        type_personna: "Culture/Patrimoine",
      },
    ],
    pages: [
      {
        nom_page: "Accueil du site",
        categorie: "Accueil",
      },
      {
        nom_page: "Liste des randonnées",
        categorie: "Activités",
      },
    ],
    vues_totales: 2,
  };

  await envoyerDonneesEnLot(donneesLot);
}

// ===================================================================
// 5. RÉCUPÉRATION DES STATISTIQUES
// ===================================================================

/**
 * Récupère les statistiques générales pour affichage sur le site
 */
async function obtenirStatistiques() {
  try {
    const response = await fetch(`${API_BASE_URL}/stats`);
    const stats = await response.json();

    console.log("📊 Statistiques:", stats);

    // Exemple d'affichage sur le site
    if (document.getElementById("stats-compteur")) {
      document.getElementById("stats-compteur").innerHTML = `
                <p>🏖️ ${stats.vues_totales} visiteurs ont exploré notre région</p>
                <p>👥 ${stats.nombre_visiteurs} profils de voyageurs collectés</p>
            `;
    }

    return stats;
  } catch (error) {
    console.error("❌ Erreur lors de la récupération des stats:", error);
  }
}

// ===================================================================
// 6. VÉRIFICATION DE L'ÉTAT DE L'API
// ===================================================================

/**
 * Vérifie que l'API est disponible
 */
async function verifierAPI() {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    const health = await response.json();

    if (health.status === "healthy") {
      console.log("✅ API opérationnelle");
      return true;
    }
  } catch (error) {
    console.warn("⚠️ API non disponible, mode hors ligne activé");
    return false;
  }
}

// ===================================================================
// 7. INTÉGRATION COMPLÈTE POUR UN SITE WEB
// ===================================================================

/**
 * Initialisation complète à inclure dans votre site
 */
async function initialiserTrackingOfficeTourisme() {
  // Vérifier que l'API est disponible
  const apiDisponible = await verifierAPI();

  if (!apiDisponible) {
    console.warn("Mode hors ligne - tracking désactivé");
    return;
  }

  // Incrémenter les vues totales
  await incrementerVuesTotales();

  // Détecter et enregistrer la page courante
  detecterEtEnregistrerPage();

  // Afficher les statistiques si un élément est prévu
  await obtenirStatistiques();

  // Initialiser le formulaire visiteur s'il existe
  if (document.getElementById("form-visiteur")) {
    initialiserFormulaireVisiteur();
  }

  console.log("🏖️ Tracking Office de Tourisme initialisé");
}

// Auto-initialisation
document.addEventListener(
  "DOMContentLoaded",
  initialiserTrackingOfficeTourisme
);

// ===================================================================
// EXPORT POUR UTILISATION EN MODULE
// ===================================================================

// Si vous utilisez des modules ES6
export {
  incrementerVuesTotales,
  enregistrerVuePage,
  ajouterVisiteur,
  envoyerDonneesEnLot,
  obtenirStatistiques,
  verifierAPI,
  initialiserTrackingOfficeTourisme,
};
