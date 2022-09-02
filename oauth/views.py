from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import viewsets, parsers,permissions

from . import serializers
from services.auth_services import check_google_auth


class UserView(viewsets.ModelViewSet):
    """ Просмотр и редактирование данных пользователя
    """
    parser_classes = (parsers.MultiPartParser,)
    serializers_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user

    def get_object(self):
        return self.get_queryset()


def google_login(request):
    """ Страница входа через Google
    """
    return render(request, 'oauth/google_login.html')


@api_view(["POST"])
def google_auth(request):
    """ Подтверждение авторизации через Google
    """
    google_data = serializers.GoogleAuth(data=request.data)
    if google_data.is_valid():
        token = check_google_auth(google_data.data)
        return Response(token)
    else:
        return AuthenticationFailed(code=403, detail='Bad data Google')
