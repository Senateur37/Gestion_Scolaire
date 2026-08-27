import os
import datetime
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings

class Command(BaseCommand):
    help = 'Sauvegarde la base de données au format JSON'

    def handle(self, *args, **kwargs):
        # Création du dossier backups s'il n'existe pas
        backup_dir = os.path.join(settings.BASE_DIR, 'backups')
        os.makedirs(backup_dir, exist_ok=True)
        
        # Formatage du nom de fichier
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f"db_backup_{timestamp}.json"
        filepath = os.path.join(backup_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                call_command('dumpdata', stdout=f)
            self.stdout.write(self.style.SUCCESS(f'Sauvegarde réussie : {filepath}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erreur lors de la sauvegarde : {str(e)}'))
