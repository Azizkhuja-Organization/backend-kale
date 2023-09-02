import os
import sys
from pathlib import Path

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

import config.routing
from config.customauth import TokenAuthMiddlewareStack
from config.settings.base import DEBUG

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(BASE_DIR / "kale"))
if DEBUG:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
django_application = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_application,
        "websocket": AllowedHostsOriginValidator(
            # TokenAuthMiddlewareStack(URLRouter(config.routing.websocket_urlpatterns))
            AuthMiddlewareStack(URLRouter(config.routing.websocket_urlpatterns))
        ),
    }
)
