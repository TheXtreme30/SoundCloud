from datetime import datetime, timedelta
from typing import Optional

import jwt
from django.conf import settings
from rest_framework import authentication, exceptions
from google.oauth2 import id_token
from google.auth.transport import requests

from ..models import AuthUser
from ..serializers import GoogleAuth


class AuthBackend(authentication.BaseAuthentication):
    authentication_header_prefix = 'Token'

    def authenticate(self, request, token=None, **kwargs) -> Optional[tuple]:
        auth_header = authentication.get_authorization_header(request).split()

        if not auth_header or auth_header[0].lower() != b'token':
            return None

        if len(auth_header) == 1:
            raise exceptions.AuthenticationFailed('Недопустимый заголовок токена. Учетные данные не предоставлены.')
        elif len(auth_header) > 2:
            raise exceptions.AuthenticationFailed(
                'Недопустимый заголовок токена. Строка токена не должна содержать пробелов.'
            )

        try:
            token = auth_header[1].decode('utf-8')
        except UnicodeError:
            raise exceptions.AuthenticationFailed(
                'Недопустимый заголовок токена. Строка токена не должна содержать недопустимых символов.'
            )

        return self.authenticate_credential(token)

    def authenticate_credential(self, token) -> tuple:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        except jwt.PyJWTError:
            raise exceptions.AuthenticationFailed('Неверная аутентификация. Не удалось расшифровать токен.')

        token_exp = datetime.fromtimestamp(payload['exp'])
        if token_exp < datetime.utcnow():
            raise exceptions.AuthenticationFailed('Срок действия токена истек.')

        try:
            user = AuthUser.objects.get(id=payload['user_id'])
        except AuthUser.DoesNotExist:
            raise exceptions.AuthenticationFailed('Пользователь, соответствующий этому токену, найден не был.')

        return user, None


def create_token(user_id: int) -> dict:
    """ Создание токена."""
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        'user_id': user_id,
        'access_token': create_access_token(
            data={'user_id': user_id}, expires_delta=access_token_expires
        ),
        'token_type': 'Token'
    }


def create_access_token(data: dict, expires_delta: timedelta = None):
    """ Создание access token."""
    to_encode = data.copy()
    if expires_delta is not None:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire, 'sub': 'access'})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def check_google_auth(google_user: GoogleAuth) -> dict:
    """Проверка токена."""
    try:
        id_token.verify_oauth2_token(
            google_user['token'], requests.Request(), settings.GOOGLE_CLIENT_ID
        )
    except ValueError:
        raise exceptions.AuthenticationFailed(code=403, detail='Неправильный токен Google')

    user, _ = AuthUser.objects.get_or_create(email=google_user['email'])
    return create_token(user.id)
