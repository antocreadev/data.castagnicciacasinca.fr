import os
import shutil
from datetime import datetime
from database import DatabaseManager


class BackupManager:
    def __init__(self, db_path="tourisme_data.db"):
        self.db_path = db_path
        self.backup_dir = "backups"
        self.ensure_backup_dir()

    def ensure_backup_dir(self):
        """S'assure que le répertoire de sauvegarde existe"""
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

    def create_backup(self, backup_name=None):
        """Crée une sauvegarde de la base de données"""
        if not backup_name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"backup_{timestamp}.db"

        backup_path = os.path.join(self.backup_dir, backup_name)

        try:
            shutil.copy2(self.db_path, backup_path)
            return backup_path
        except Exception as e:
            print(f"Erreur lors de la création de la sauvegarde: {e}")
            return None

    def list_backups(self):
        """Liste toutes les sauvegardes disponibles"""
        if not os.path.exists(self.backup_dir):
            return []

        backups = []
        for file in os.listdir(self.backup_dir):
            if file.endswith(".db"):
                file_path = os.path.join(self.backup_dir, file)
                file_stats = os.stat(file_path)
                file_size = file_stats.st_size
                file_date = datetime.fromtimestamp(file_stats.st_mtime)

                backups.append(
                    {
                        "name": file,
                        "path": file_path,
                        "size": file_size,
                        "date": file_date,
                    }
                )

        return sorted(backups, key=lambda x: x["date"], reverse=True)

    def restore_backup(self, backup_path):
        """Restaure une sauvegarde"""
        try:
            shutil.copy2(backup_path, self.db_path)
            return True
        except Exception as e:
            print(f"Erreur lors de la restauration: {e}")
            return False

    def delete_backup(self, backup_path):
        """Supprime une sauvegarde"""
        try:
            os.remove(backup_path)
            return True
        except Exception as e:
            print(f"Erreur lors de la suppression de la sauvegarde: {e}")
            return False

    def auto_backup(self):
        """Crée une sauvegarde automatique avant les opérations de suppression"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"auto_backup_{timestamp}.db"
        return self.create_backup(backup_name)

    def cleanup_old_backups(self, keep_count=10):
        """Nettoie les anciennes sauvegardes, garde seulement les N plus récentes"""
        backups = self.list_backups()

        if len(backups) > keep_count:
            backups_to_delete = backups[keep_count:]
            deleted_count = 0

            for backup in backups_to_delete:
                if self.delete_backup(backup["path"]):
                    deleted_count += 1

            return deleted_count

        return 0
