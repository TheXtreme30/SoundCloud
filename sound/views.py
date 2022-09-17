import os
from urllib import response

from django.http import Http404, HttpResponse, FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import parsers, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import models, serializers
from .pagination import Pagination
from .permissions import IsAuthorOrAdminOrReadOnly, IsOwnerOrAdminOrReadOnly
from .services.services import delete_old_file


class UserView(viewsets.ModelViewSet):
    """Просмотр и редактирование данных пользователя."""
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    pagination_class = Pagination
    parser_classes = (parsers.MultiPartParser,)
    permission_classes = (IsOwnerOrAdminOrReadOnly,)

    @action(detail=True, permission_classes=[IsAuthenticated])
    def subscribe(self, request, id=None):
        user = request.user
        subscriber = get_object_or_404(models.User, id=id)

        data = {
            'user': user.id,
            'subscriber': subscriber.id,
        }
        serializer = serializers.FollowSerializer(
            data=data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id=None):
        user = request.user
        subscriber = get_object_or_404(models.User, id=id)
        subscribe = get_object_or_404(
            models.Follow, user=user, subscriber=subscriber
        )
        subscribe.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        queryset = models.Follow.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = serializers.FollowerSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


class GenreView(viewsets.ReadOnlyModelViewSet):
    """Список жанров."""
    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenreSerializer


class AlbumView(viewsets.ModelViewSet):
    """CRUD альбомов автора."""
    parser_classes = (parsers.MultiPartParser,)
    serializer_class = serializers.AlbumSerializer
    permission_classes = (IsAuthorOrAdminOrReadOnly,)

    def get_queryset(self):
        user  = self.request.user
        author_id = self.kwargs.get('user_id')
        if user.id == author_id:
            return models.Album.objects.filter(user=user)
        return models.Album.objects.filter(user__id=author_id, private=False)


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        delete_old_file(instance.cover.path)
        instance.delete()


class TitleView(viewsets.ModelViewSet):
    """CRUD аудиозаписей."""
    parser_classes = (parsers.MultiPartParser,)
    permission_classes = (IsAuthorOrAdminOrReadOnly,)
    serializer_class = serializers.TitleSerializer

    def get_queryset(self):
        user  = self.request.user
        author_id = self.kwargs.get('user_id')
        if user.id == author_id:
            return models.Title.objects.filter(user=user)
        return models.Title.objects.filter(user__id=author_id, private=False)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        delete_old_file(instance.cover.path)
        delete_old_file(instance.file.path)
        instance.delete()

    @action(detail=True)
    def streaming_title(self, request, user_id, pk=None):
        user = request.user
        author_id = user_id
        if user.id == author_id:
            self.title = get_object_or_404(models.Title, id=pk)
        self.title = get_object_or_404(models.Title, id=pk, private=False)

        if os.path.exists(self.title.file.path):
            response = FileResponse(open(self.title.file.path, 'rb'), filename=self.title.file.name)
            # response = HttpResponse('', content_type="audio/mpeg", status=206)
            # response['X-Accel-Redirect'] = self.title.file.path
            return response
        else:
            return Http404

    @action(detail=True)
    def download_title(self, request, user_id, pk=None):
        user = request.user
        author_id = user_id
        if user.id == author_id:
            self.title = get_object_or_404(models.Title, id=pk)
        self.title = get_object_or_404(models.Title, id=pk, private=False)

        if os.path.exists(self.title.file.path):
            response = FileResponse(
                open(self.title.file.path, 'rb'), filename=self.title.file.name, as_attachment=True
            )
            # response = HttpResponse('', content_type="audio/mpeg", status=206)
            # response["Content-Disposition"] = f"attachment; filename={self.title.file.name.split('/')[-1]}"
            # response['X-Accel-Redirect'] = self.title.file.path
            return response
        else:
            return Http404


class PlaylistView(viewsets.ModelViewSet):
    """CRUD плейлистов пользователя."""
    serializer_class = serializers.PlaylistSerializer
    parser_classes = (parsers.MultiPartParser,)
    permission_classes = (IsAuthorOrAdminOrReadOnly,)

    def get_queryset(self):
        user  = self.request.user
        author_id = self.kwargs.get('user_id')
        if user.id == author_id:
            return models.Playlist.objects.filter(user=user)
        return models.Playlist.objects.filter(user__id=author_id, private=False)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        delete_old_file(instance.cover.path)
        instance.delete()


class CommentView(viewsets.ModelViewSet):
    """Комментарии к аудиозаписи."""
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        return models.Comment.objects.filter(title_id=self.kwargs.get('title_id'))
