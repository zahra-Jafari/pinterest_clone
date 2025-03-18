import os
import sys
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pinterest_clone.settings")

application = get_wsgi_application()


path = '/home/zahrajj/pinterest_clone'
if path not in sys.path:
    sys.path.append(path)




