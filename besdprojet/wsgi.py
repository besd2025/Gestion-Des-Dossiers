"""
WSGI config for besdprojet project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# 1. Définit les réglages Django avant toute chose
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'besdprojet.settings')
django.setup()

# 2. Importe tes routes WebSocket après le setup de Django
import besdapp.routing

application = ProtocolTypeRouter({
    # Gère le HTTP classique (API Rest, Admin)
    "http": get_asgi_application(),

    # Gère les WebSockets (Notifications en temps réel)
    "websocket": AuthMiddlewareStack(
        URLRouter(
            besdapp.routing.websocket_urlpatterns
        )
    ),
})