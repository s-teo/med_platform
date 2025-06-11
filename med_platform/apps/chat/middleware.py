from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from rest_framework_simplejwt.tokens import UntypedToken
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
import jwt
from django.conf import settings
import logging
logger = logging.getLogger("django")


@database_sync_to_async
def get_user(user_id):
    try:
        return get_user_model().objects.get(id=user_id)
    except get_user_model().DoesNotExist:
        return AnonymousUser()

class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = scope.get('query_string', b'').decode()
        query_params = parse_qs(query_string)
        token_list = query_params.get('token')

        if token_list:
            token = token_list[0]
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                user = await get_user(payload['user_id'])
                scope['user'] = user
                logger.info(f"✅ JWTAuthMiddleware: Authenticated user: {user}")

            except (jwt.InvalidTokenError, KeyError) as e:
                scope['user'] = AnonymousUser()
                logger.warning(f"❌ JWTAuthMiddleware: Token decode error: {e}")

        else:
            scope['user'] = AnonymousUser()
            logger.warning("❌ JWTAuthMiddleware: No token provided in query")


        return await super().__call__(scope, receive, send)
