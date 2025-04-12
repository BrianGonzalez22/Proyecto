"""
ASGI config for mi_proyecto project.

It exposes the ASGI callable as a module-level variable named ``application``.
For more information on this file, see
https://channels.readthedocs.io/en/stable/deploying.html
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

# Configuración de las variables de entorno
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Para manejar las solicitudes HTTP estándar
    "websocket": AuthMiddlewareStack(  # Para manejar las conexiones WebSocket
        URLRouter([
            # Aquí irían las rutas específicas de WebSocket que definirás más adelante
        ])
    ),
})
