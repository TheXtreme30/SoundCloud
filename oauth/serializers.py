from rest_framework import serializers

from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AuthUser
        fields = ('avatar', 'country', 'city', 'bio', 'username')


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AuthUser
        fields = ('id', 'avatar', 'country', 'city', 'bio', 'username')


class GoogleAuth(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField()
