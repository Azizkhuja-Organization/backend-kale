from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from rest_framework_simplejwt.exceptions import TokenError


@database_sync_to_async
def get_user(headers):
    from django.contrib.auth.models import AnonymousUser

    if b'authorization' in headers:
        from rest_framework_simplejwt.tokens import AccessToken
        from django.contrib.auth import get_user_model
        User = get_user_model()

        token_name, token_key = headers[b'authorization'].decode().split()

        if token_name == 'Bearer':
            try:
                token = AccessToken(token=token_key)
            except TokenError:
                return AnonymousUser()
            user = User.objects.get(id=token.get('user_id'))
            return user
        return AnonymousUser()
    return AnonymousUser()


class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        headers = dict(scope['headers'])
        scope['user'] = await get_user(headers)
        return await self.inner(scope, receive, send)


class TokenAuthMiddlewareInstance:
    """
    Yeah, this is black magic:
    https://github.com/django/channels/issues/1399
    """

    def __init__(self, scope, middleware):
        self.middleware = middleware
        self.scope = dict(scope)
        self.inner = self.middleware.inner

    async def __call__(self, receive, send):
        headers = dict(self.scope['headers'])
        self.scope['user'] = await get_user(headers)
        inner = self.inner(self.scope)
        return await inner(receive, send)


def TokenAuthMiddlewareStack(inner):
    return TokenAuthMiddleware(AuthMiddlewareStack(inner))
