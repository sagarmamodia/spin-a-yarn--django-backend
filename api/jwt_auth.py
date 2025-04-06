import jwt
import datetime
from django.conf import settings
from django.http import JsonResponse
from channels.middleware import BaseMiddleware

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = 'HS256'

def generate_jwt(payload_data):
    payload = {
        'guest_id': payload_data['guest_id'],
        'room_id': payload_data['room_id'],
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1),
        'iat': datetime.datetime.now(datetime.timezone.utc),
    }

    token = jwt.encode(payload, SECRET_KEY, ALGORITHM)
    return token

def decode_jwt(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def jwt_required(view_func):
    def _wrapper(request, *args, **kwargs):
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            payload = decode_jwt(token)
            if payload:
                request.guest_id = payload['guest_id']
                request.room_id = payload['room_id']
                return view_func(request, *args, **kwargs)
        
        return JsonResponse({"error": "Unauthorized"}, status=401)
    
    return _wrapper

# class SyncJWTAuthMiddleware(BaseMiddleware):
#     def __init__(self, inner):
#         self.inner = inner

#     def __call__(self, scope):
#         pass