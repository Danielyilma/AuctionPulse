import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from .auth import JWTAuthMiddleware
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from AuctionManager.urls import websocket_urlpatterns as app1route
from notifications.urls import websocket_urlpatterns as app2route

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AuctionPulse.settings')

websocket_urlpatterns = app1route + app2route
application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AllowedHostsOriginValidator(
        JWTAuthMiddleware(
            URLRouter(websocket_urlpatterns)
        )
    )
})
