from audio_validator.validator import AudioValidator
from django.contrib.auth import get_user_model
from django.core.validators import validate_image_file_extension
from django.db import models

from oauth.models import CustomUser
from sound.services.services import (get_album_cover_upload_path,
                                     get_playlist_cover_upload_path,
                                     get_title_upload_path,
                                     validate_size_image)

User = get_user_model()


class Genre(models.Model):
    """ Модель жанров."""
    name = models.CharField(max_length=256, unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Album(models.Model):
    """ Модель альбомов."""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='albums')
    name = models.CharField(max_length=256)
    description = models.TextField(max_length=1024)
    private = models.BooleanField(default=False)
    cover = models.ImageField(
        upload_to=get_album_cover_upload_path,
        blank=True, null=True,
        validators=[validate_image_file_extension, validate_size_image],
    )

    class Meta:
        verbose_name = 'Альбом'
        verbose_name_plural = 'Альбомы'

    def __str__(self):
        return self.name


class Title(models.Model):
    """ Модель аудио записей."""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='titles')
    name = models.CharField(max_length=256)
    genre = models.ManyToManyField(Genre, related_name='title_genres')
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, blank=True, null=True)
    file = models.FileField(
        upload_to=get_title_upload_path,
        validators=[AudioValidator('mp3')],
    )
    create_at = models.DateTimeField(auto_now_add=True)
    private = models.BooleanField(default=False)
    cover = models.ImageField(
        upload_to=get_playlist_cover_upload_path,
        blank=True, null=True,
        validators=[validate_image_file_extension, validate_size_image],
    )

    class Meta:
        verbose_name = 'Аудиозапись'
        verbose_name_plural = 'Аудиозаписи'

    def __str__(self):
        return f'{self.user} - {self.name}'


class Comment(models.Model):
    """ Модель комментариев."""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='title_comments')
    text = models.TextField(max_length=1024)
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Пользователь {self.user} оставил коментарий к {self.title}.'


class Playlist(models.Model):
    """ Модель плейлистов пользователя."""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='playlists')
    name = models.CharField(max_length=256)
    titles = models.ManyToManyField(Title, related_name='title_playlists')
    private = models.BooleanField(default=False)
    cover = models.ImageField(
        upload_to=get_playlist_cover_upload_path,
        blank=True, null=True,
        validators=[validate_image_file_extension, validate_size_image],
    )

    class Meta:
        verbose_name = 'Плейлист'
        verbose_name_plural = 'Плейлисты'

    def __str__(self):
        return self.name


class Follow(models.Model):
    """Модель подписок."""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='owner')
    subscriber = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='subscriber')
    subscription_date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'subscriber'], name='follow_unique'
            )
        ]

    def __str__(self):
        return f'{self.subscriber} подписан на {self.user}'
