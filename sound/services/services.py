import os

from django.core.exceptions import ValidationError

MEGABYTE_LIMIT = 4


def get_album_cover_upload_path(instance, filename):
    """Построение пути к файлу, format: (media)/album/username/{file}"""
    path = f'album/{instance.user.username}/'
    new_filename = f'{instance.name}.{filename.split(".")[-1]}'
    return os.path.join(path, new_filename)


def get_playlist_cover_upload_path(instance, filename):
    """Построение пути к файлу, format: (media)/playlist/username/{file}"""
    path = f'playlist/{instance.user.username}/'
    new_filename = f'{instance.name}.{filename.split(".")[-1]}'
    return os.path.join(path, new_filename)


def get_title_upload_path(instance, filename):
    """Построение пути к файлу, format: (media)/title/username/{file}"""
    path = f'title/{instance.user.username}/'
    new_filename = f'{instance.user.username}-{instance.name}.{filename.split(".")[-1]}'
    return os.path.join(path, new_filename)


def get_title_cover_upload_path(instance, filename):
    """Построение пути к файлу, format: (media)/title/username/cover/{file}"""
    path = f'title/{instance.user.username}/cover/'
    new_filename = f'{instance.user.username}-{instance.name}.{filename.split(".")[-1]}'
    return os.path.join(path, new_filename)


def validate_size_image(file_obj):
    """Проверка размера файла."""
    if file_obj.size > MEGABYTE_LIMIT * 1024 * 1024:
        raise ValidationError(f"Максимальный размер файла {MEGABYTE_LIMIT}MB")


def delete_old_file(path_file):
    """Удаление старого файла."""
    if os.path.exists(path_file):
        os.remove(path_file)
