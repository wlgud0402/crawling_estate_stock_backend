import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings.local")
application = get_wsgi_application()
