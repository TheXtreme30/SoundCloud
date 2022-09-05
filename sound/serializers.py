from rest_framework import serializers

from oauth.serializers import AuthorSerializer

from . import models
from .services.services import delete_old_file


class BaseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)


class GenreSerializer(BaseSerializer):
    class Meta:
        model = models.Genre
        fields = ('id', 'name')


class AlbumSerializer(BaseSerializer):
    class Meta:
        model = models.Album
        fields = ('id', 'name', 'description', 'cover', 'private')

    def update(self, instance, validated_data):
        delete_old_file(instance.cover.path)
        return super().update(instance, validated_data)


class CreateTitleSerializer(BaseSerializer):
    plays_count = serializers.IntegerField(read_only=True)
    download = serializers.IntegerField(read_only=True)
    user = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Title
        fields = ('id', 'name', 'genre', 'album', 'link_of_author', 'file', 'create_at',
                  'plays_count', 'download', 'private', 'cover', 'user')

    def update(self, instance, validated_data):
        delete_old_file(instance.file.path)
        delete_old_file(instance.cover.path)
        return super().update(instance, validated_data)


class TitleSerializer(CreateTitleSerializer):
    genre = GenreSerializer(many=True)
    album = AlbumSerializer()
    user = AuthorSerializer()


class CreatePlaylistSerializer(BaseSerializer):
    class Meta:
        model = models.Playlist
        fields = ('id', 'name', 'cover', 'titles')

    def update(self, instance, validated_data):
        delete_old_file(instance.cover.path)
        return super().update(instance, validated_data)


class PlaylistSerializer(CreatePlaylistSerializer):
    titles = TitleSerializer(many=True)


class CommentAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ('id', 'text', 'title')


class CommentSerializer(serializers.ModelSerializer):
    user = AuthorSerializer()

    class Meta:
        model = models.Comment
        fields = ('id', 'text', 'user', 'title', 'create_at')


class MixedSerializer:
    def get_serializer(self, *args, **kwargs):
        try:
            serializer_class = self.serializer_classes_by_action[self.action]
        except KeyError:
            serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)
