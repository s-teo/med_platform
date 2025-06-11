import os
import sys
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "apps"))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()  # ← Важно вызвать ДО импорта consumers и routing

from apps.chat.middleware import JWTAuthMiddleware  # ← путь к JWTAuthMiddleware
from apps.chat.routing import websocket_urlpatterns  # ← Импорт роутов WebSocket

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": JWTAuthMiddleware(
        URLRouter(websocket_urlpatterns)
    ),
})

