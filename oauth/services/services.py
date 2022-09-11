import os
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


SIZE_LIMIT = 4


@deconstructible
class PathAndRename(object):

    def __init__(self, path, name):
        self.path = path
        self.name = name

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = f'{self.name}.{ext}'
        return os.path.join(self.sub_path, filename)


def get_avatar_upload_path(instance, filename):
    """Построение пути к файлу: media/avatar/username/{file}."""
    path = f'avatar/{instance.username}/'
    name = f'{instance.username}'
    return PathAndRename(path, name)


def validate_image_size(fiel_obj):
    """Проверка размера файла."""
    if fiel_obj.size > SIZE_LIMIT * 1024 * 1024:
        raise ValidationError(f'Максимальный размер файла {SIZE_LIMIT}Mb.')
