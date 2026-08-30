import sys
import os

# Ajouter le dossier G_Scolaire au path Python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'G_Scolaire'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'G_Scolaire.settings')

from mangum import Mangum
from G_Scolaire.wsgi import application

handler = Mangum(application, lifespan="off")
