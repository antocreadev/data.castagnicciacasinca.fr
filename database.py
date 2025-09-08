import sqlite3
from datetime import datetime
import os


class DatabaseManager:
    def __init__(self, db_path="tourisme_data.db"):
        self.db_path = db_path
        self.init_database()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_database(self):
        """Initialise la base de données avec les tables nécessaires"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Table pour les vues totales du site
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS vues_totales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE DEFAULT CURRENT_DATE,
                nombre_vues INTEGER DEFAULT 0
            )
        """
        )

        # Table pour les vues par page
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS vues_pages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom_page TEXT NOT NULL,
                categorie TEXT NOT NULL,
                nombre_vues INTEGER DEFAULT 1,
                date_derniere_vue DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # Table pour les visiteurs (valeurs libres, sans contraintes CHECK)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS visiteurs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type_visiteur TEXT NOT NULL,
                temps_sejour TEXT NOT NULL,
                tranche_age TEXT NOT NULL,
                type_personna TEXT NOT NULL,
                date_visite DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        # Migration: si d'anciennes contraintes CHECK existent, recréer la table sans contraintes
        try:
            cursor.execute("PRAGMA table_info(visiteurs)")
            cols = cursor.fetchall()
            col_defs = {c[1]: c[2] for c in cols}  # name -> type
            # Vérification basique: si la définition contient CHECK, on migre
            cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='visiteurs'")
            table_sql_row = cursor.fetchone()
            if table_sql_row and table_sql_row[0] and "CHECK" in table_sql_row[0].upper():
                cursor.execute("BEGIN")
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS visiteurs__new (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        type_visiteur TEXT NOT NULL,
                        temps_sejour TEXT NOT NULL,
                        tranche_age TEXT NOT NULL,
                        type_personna TEXT NOT NULL,
                        date_visite DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                    """
                )
                cursor.execute(
                    "INSERT INTO visiteurs__new (id, type_visiteur, temps_sejour, tranche_age, type_personna, date_visite) "
                    "SELECT id, type_visiteur, temps_sejour, tranche_age, type_personna, date_visite FROM visiteurs"
                )
                cursor.execute("DROP TABLE visiteurs")
                cursor.execute("ALTER TABLE visiteurs__new RENAME TO visiteurs")
                conn.commit()
        except Exception:
            # Si la migration échoue, on ignore pour ne pas bloquer le démarrage
            pass

        # Insérer une donnée initiale pour les vues totales si elle n'existe pas
        cursor.execute("SELECT COUNT(*) FROM vues_totales")
        if cursor.fetchone()[0] == 0:
            cursor.execute("INSERT INTO vues_totales (nombre_vues) VALUES (0)")

        conn.commit()
        conn.close()

    def increment_vues_totales(self):
        """Incrémente le nombre de vues totales du site"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE vues_totales SET nombre_vues = nombre_vues + 1, date = CURRENT_DATE WHERE id = 1"
        )
        conn.commit()
        conn.close()

    def get_vues_totales(self):
        """Récupère le nombre total de vues du site"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT nombre_vues FROM vues_totales WHERE id = 1")
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 0

    def add_vue_page(self, nom_page, categorie):
        """Ajoute ou met à jour une vue de page"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Vérifier si la page existe déjà
        cursor.execute(
            "SELECT id FROM vues_pages WHERE nom_page = ? AND categorie = ?",
            (nom_page, categorie),
        )
        existing = cursor.fetchone()

        if existing:
            cursor.execute(
                """
                UPDATE vues_pages 
                SET nombre_vues = nombre_vues + 1, date_derniere_vue = CURRENT_TIMESTAMP 
                WHERE nom_page = ? AND categorie = ?
            """,
                (nom_page, categorie),
            )
        else:
            cursor.execute(
                """
                INSERT INTO vues_pages (nom_page, categorie, nombre_vues) 
                VALUES (?, ?, 1)
            """,
                (nom_page, categorie),
            )

        conn.commit()
        conn.close()

    def get_vues_pages(self):
        """Récupère toutes les vues par page"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT nom_page, categorie, nombre_vues, date_derniere_vue FROM vues_pages ORDER BY nombre_vues DESC"
        )
        result = cursor.fetchall()
        conn.close()
        return result

    def add_visiteur(self, type_visiteur, temps_sejour, tranche_age, type_personna):
        """Ajoute un nouveau visiteur"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO visiteurs (type_visiteur, temps_sejour, tranche_age, type_personna) 
            VALUES (?, ?, ?, ?)
        """,
            (type_visiteur, temps_sejour, tranche_age, type_personna),
        )
        conn.commit()
        conn.close()

    def get_visiteurs(self):
        """Récupère tous les visiteurs"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM visiteurs ORDER BY date_visite DESC")
        result = cursor.fetchall()
        conn.close()
        return result

    def get_stats_visiteurs(self):
        """Récupère les statistiques des visiteurs"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Statistiques par type de visiteur
        cursor.execute(
            "SELECT type_visiteur, COUNT(*) FROM visiteurs GROUP BY type_visiteur"
        )
        stats_type = cursor.fetchall()

        # Statistiques par temps de séjour
        cursor.execute(
            "SELECT temps_sejour, COUNT(*) FROM visiteurs GROUP BY temps_sejour"
        )
        stats_sejour = cursor.fetchall()

        # Statistiques par tranche d'âge
        cursor.execute(
            "SELECT tranche_age, COUNT(*) FROM visiteurs GROUP BY tranche_age"
        )
        stats_age = cursor.fetchall()

        # Statistiques par type de persona
        cursor.execute(
            "SELECT type_personna, COUNT(*) FROM visiteurs GROUP BY type_personna"
        )
        stats_personna = cursor.fetchall()

        conn.close()
        return {
            "type_visiteur": stats_type,
            "temps_sejour": stats_sejour,
            "tranche_age": stats_age,
            "type_personna": stats_personna,
        }

    def delete_visiteur(self, visiteur_id):
        """Supprime un visiteur par son ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM visiteurs WHERE id = ?", (visiteur_id,))
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        return rows_affected > 0

    def update_visiteur(
        self, visiteur_id, type_visiteur, temps_sejour, tranche_age, type_personna
    ):
        """Met à jour un visiteur"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE visiteurs 
            SET type_visiteur = ?, temps_sejour = ?, tranche_age = ?, type_personna = ?
            WHERE id = ?
        """,
            (type_visiteur, temps_sejour, tranche_age, type_personna, visiteur_id),
        )
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        return rows_affected > 0

    def get_visiteur_by_id(self, visiteur_id):
        """Récupère un visiteur par son ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM visiteurs WHERE id = ?", (visiteur_id,))
        result = cursor.fetchone()
        conn.close()
        return result

    def delete_page(self, page_id):
        """Supprime une page par son ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM vues_pages WHERE id = ?", (page_id,))
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        return rows_affected > 0

    def update_page(self, page_id, nom_page, categorie):
        """Met à jour une page"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE vues_pages 
            SET nom_page = ?, categorie = ?
            WHERE id = ?
        """,
            (nom_page, categorie, page_id),
        )
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        return rows_affected > 0

    def get_page_by_id(self, page_id):
        """Récupère une page par son ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vues_pages WHERE id = ?", (page_id,))
        result = cursor.fetchone()
        conn.close()
        return result

    def get_vues_pages_with_id(self):
        """Récupère toutes les vues par page avec les IDs"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, nom_page, categorie, nombre_vues, date_derniere_vue FROM vues_pages ORDER BY nombre_vues DESC"
        )
        result = cursor.fetchall()
        conn.close()
        return result

    def delete_visiteurs_by_criteria(
        self,
        type_visiteur=None,
        temps_sejour=None,
        tranche_age=None,
        type_personna=None,
    ):
        """Supprime les visiteurs selon des critères spécifiques"""
        conn = self.get_connection()
        cursor = conn.cursor()

        conditions = []
        params = []

        if type_visiteur and type_visiteur != "Tous":
            conditions.append("type_visiteur = ?")
            params.append(type_visiteur)

        if temps_sejour and temps_sejour != "Tous":
            conditions.append("temps_sejour = ?")
            params.append(temps_sejour)

        if tranche_age and tranche_age != "Tous":
            conditions.append("tranche_age = ?")
            params.append(tranche_age)

        if type_personna and type_personna != "Tous":
            conditions.append("type_personna = ?")
            params.append(type_personna)

        if conditions:
            query = f"DELETE FROM visiteurs WHERE {' AND '.join(conditions)}"
            cursor.execute(query, params)
        else:
            cursor.execute("DELETE FROM visiteurs")

        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        return rows_affected

    def delete_pages_by_categories(self, categories):
        """Supprime les pages selon les catégories spécifiées"""
        if not categories:
            return 0

        conn = self.get_connection()
        cursor = conn.cursor()

        placeholders = ",".join(["?" for _ in categories])
        query = f"DELETE FROM vues_pages WHERE categorie IN ({placeholders})"
        cursor.execute(query, categories)

        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        return rows_affected

    def reset_all_data(self):
        """Remet à zéro toutes les données"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM visiteurs")
        cursor.execute("DELETE FROM vues_pages")
        cursor.execute("UPDATE vues_totales SET nombre_vues = 0, date = CURRENT_DATE")

        conn.commit()
        conn.close()
        return True
