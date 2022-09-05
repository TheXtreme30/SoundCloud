from django.core.exceptions import ValidationError


def get_album_cover_upload_path(instance, file):
    """Построение пути к файлу, format: (media)/album/user_id/photo.jpg."""
    return f'album/user_{instance.user.id}/{file}'


def get_playlist_cover_upload_path(instance, file):
    """Построение пути к файлу, format: (media)/playlist/user_id/photo.jpg."""
    return f'playlist/user_{instance.user.id}/{file}'


def get_title_upload_path(instance, file):
    """Построение пути к файлу, format: (media)/track/user_id/audio.pm3."""
    return f'track/user_{instance.user.id}/{file}'


def get_title_cover_upload_path(instance, file):
    """Построение пути к файлу, format: (media)/track/cover/user_id/photo.jpg."""
    return f'track/cover/user_{instance.user.id}/{file}'


def validate_size_image(file_obj):
    """Проверка размера файла."""
    megabyte_limit = 4
    if file_obj.size > megabyte_limit * 1024 * 1024:
        raise ValidationError(f"Максимальный размер файла {megabyte_limit}MB")