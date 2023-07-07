
import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'notebookcopypro.settings')
import collabrate1.routing
application = ProtocolTypeRouter({
    'http' : get_asgi_application(),
    'websocket':URLRouter(
        collabrate1.routing.websocket_urlpatterns
    )
})



