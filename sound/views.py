import os

from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, parsers, views, viewsets

from . import models, serializers
from .pagination import Pagination
from .permissions import IsAuthor
from .services.services import delete_old_file


class GenreView(generics.ListAPIView):
    """Список жанров."""
    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenreSerializer


class AlbumView(viewsets.ModelViewSet):
    """CRUD альбомов автора."""
    parser_classes = (parsers.MultiPartParser,)
    serializer_class = serializers.AlbumSerializer
    permission_classes = [IsAuthor]

    def get_queryset(self):
        return models.Album.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        delete_old_file(instance.cover.path)
        instance.delete()


class PublicAlbumView(generics.ListAPIView):
    """Список публичных альбомов автора."""
    serializer_class = serializers.AlbumSerializer

    def get_queryset(self):
        return models.Album.objects.filter(user__id=self.kwargs.get('pk'), private=False)


class TitleView(serializers.MixedSerializer, viewsets.ModelViewSet):
    """CRUD аудиозаписей."""
    parser_classes = (parsers.MultiPartParser,)
    permission_classes = [IsAuthor]
    serializer_class = serializers.CreateTitleSerializer
    serializer_classes_by_action = {
        'list': serializers.TitleSerializer
    }

    def get_queryset(self):
        return models.Title.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        delete_old_file(instance.cover.path)
        delete_old_file(instance.file.path)
        instance.delete()


class PlaylistView(serializers.MixedSerializer, viewsets.ModelViewSet):
    """CRUD плейлистов пользователя."""
    parser_classes = (parsers.MultiPartParser,)
    permission_classes = [IsAuthor]
    serializer_class = serializers.CreatePlaylistSerializer
    serializer_classes_by_action = {
        'list': serializers.PlaylistSerializer
    }

    def get_queryset(self):
        return models.Playlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        delete_old_file(instance.cover.path)
        instance.delete()


class TitleListView(generics.ListAPIView):
    """Список всех аудиозаписей."""
    queryset = models.Title.objects.filter(album__private=False, private=False)
    serializer_class = serializers.TitleSerializer
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'user__username', 'album__name', 'genre__name']


class AuthorTitleListView(generics.ListAPIView):
    """Список всех аудиозаписей автора."""
    serializer_class = serializers.TitleSerializer
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'album__name', 'genre__name']

    def get_queryset(self):
        return models.Title.objects.filter(
            user__id=self.kwargs.get('pk'), album__private=False, private=False
        )


class CommentAuthorView(viewsets.ModelViewSet):
    """CRUD комментариев автора."""
    serializer_class = serializers.CommentAuthorSerializer
    permission_classes = [IsAuthor]

    def get_queryset(self):
        return models.Comment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentView(viewsets.ModelViewSet):
    """Комментарии к аудиозаписи."""
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        return models.Comment.objects.filter(title_id=self.kwargs.get('pk'))


class StreamingFileView(views.APIView):
    """Воспроизведение аудиозаписи."""
    def set_play(self):
        self.title.plays_count += 1
        self.title.save()

    def get(self, request, pk):
        self.title = get_object_or_404(models.Title, id=pk, private=False)
        if os.path.exists(self.title.file.path):
            self.set_play()
            response = HttpResponse('', content_type="audio/mpeg", status=206)
            response['X-Accel-Redirect'] = f"/mp3/{self.title.file.name}"
            return response
        else:
            return Http404


class DownloadTitleView(views.APIView):
    """Скачивание аудиозаписи."""
    def set_download(self):
        self.title.download += 1
        self.title.save()

    def get(self, request, pk):
        self.title = get_object_or_404(models.Title, id=pk, private=False)
        if os.path.exists(self.title.file.path):
            self.set_download()
            response = HttpResponse('', content_type="audio/mpeg", status=206)
            response["Content-Disposition"] = f"attachment; filename={self.title.file.name}"
            response['X-Accel-Redirect'] = f"/media/{self.title.file.name}"
            return response
        else:
            return Http404


class StreamingFileAuthorView(views.APIView):
    """Воспроизведение аудиозаписи."""
    permission_classes = [IsAuthor]

    def get(self, request, pk):
        self.title = get_object_or_404(models.Title, id=pk, user=request.user)
        if os.path.exists(self.title.file.path):
            response = HttpResponse('', content_type="audio/mpeg", status=206)
            response['X-Accel-Redirect'] = f"/mp3/{self.title.file.name}"
            return response
        else:
            return Http404
