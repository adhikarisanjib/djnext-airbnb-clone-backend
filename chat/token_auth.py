from django.contrib.auth.models import AnonymousUser

from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async

from rest_framework_simplejwt.tokens import AccessToken

from useraccount.models import CustomUser


@database_sync_to_async
def get_user(access_token):
    try:
        token = AccessToken(access_token)
        user_id = token.payload.get('user_id')
        return CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return AnonymousUser()
    except Exception as e:
        return AnonymousUser()
    

class TokenAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        self.inner = inner
    
    async def __call__(self, scope, receive, send):
        query = dict((x.split('=') for x in scope['query_string'].decode().split('&')))
        token_key = query.get('token')
        scope['user'] = await get_user(token_key)
        return await super().__call__(scope, receive, send)
