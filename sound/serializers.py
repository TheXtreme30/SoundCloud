from rest_framework import serializers

from . import models
from .services.services import delete_old_file


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = models.User
        fields = ('id', 'email', 'username', 'country', 'city', 'bio', 'avatar', 'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return models.Follow.objects.filter(user=request.user, subscriber=obj.id).exists()


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Genre
        fields = ('id', 'name')


class AlbumSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Album
        fields = ('id', 'name', 'description', 'cover', 'private', 'user')

    def update(self, instance, validated_data):
        delete_old_file(instance.cover.path)
        return super().update(instance, validated_data)


class TitleSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    genres = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = models.Title
        fields = ('id', 'name', 'genres', 'album', 'file',
                  'create_at', 'private', 'cover', 'user')

    def update(self, instance, validated_data):
        delete_old_file(instance.file.path)
        delete_old_file(instance.cover.path)
        return super().update(instance, validated_data)


class PlaylistSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    titles = TitleSerializer(many=True)

    class Meta:
        model = models.Playlist
        fields = ('id', 'name', 'cover', 'titles', 'private', 'user')

    def update(self, instance, validated_data):
        delete_old_file(instance.cover.path)
        return super().update(instance, validated_data)


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = models.Comment
        fields = ('id', 'text', 'user', 'title', 'create_at')


class FollowerSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='subscriber.id')
    username = serializers.ReadOnlyField(source='subscriber.username')
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = models.User
        fields = ('id', 'username', 'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return models.Follow.objects.filter(
            user=obj.user, subscriber=obj.subscriber
        ).exists()


class FollowSerializer(serializers.ModelSerializer):
    queryset = models.User.objects.all()
    user = serializers.PrimaryKeyRelatedField(queryset=queryset)
    subscriber = serializers.PrimaryKeyRelatedField(queryset=queryset)

    class Meta:
        model = models.Follow
        fields = ('user', 'subscriber')

    def validate(self, data):
        request = self.context.get('request')
        subscriber_id = data['subscriber'].id
        follow_exists = models.Follow.objects.filter(
            user=request.user,
            subscriber__id=subscriber_id
        ).exists()

        if request.method == 'GET':
            if request.user.id == subscriber_id:
                raise serializers.ValidationError(
                    'Нельзя подписаться на себя.'
                )
            if follow_exists:
                raise serializers.ValidationError(
                    'Вы уже подписаны на этого пользователя.'
                )

        return data
