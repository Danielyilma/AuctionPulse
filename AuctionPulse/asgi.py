import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from AuctionManager.urls import websocket_urlpatterns as app1route

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AuctionPulse.settings')

websocket_urlpatterns = app1route
application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        )
    )
})
