import os

from django.core.exceptions import ValidationError

SIZE_LIMIT = 4


def get_avatar_upload_path(instance, filename):
    """Построение пути к файлу: media/avatar/username/{file}."""
    path = f'avatat/{instance.username}/'
    new_filename = f'{instance.username}.{filename.split(".")[-1]}'
    return os.path.join(path, new_filename)


def validate_image_size(fiel_obj):
    """Проверка размера файла."""
    if fiel_obj.size > SIZE_LIMIT * 1024 * 1024:
        raise ValidationError(f'Максимальный размер файла {SIZE_LIMIT}Mb.')
