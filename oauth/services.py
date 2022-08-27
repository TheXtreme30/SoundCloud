from django.core.exceptions import ValidationError

SIZE_LIMIT = 4


def get_avatar_upload_path(instance, file):
    """Построение пути к файлу: media/avatar/user_id/{file_name}"""
    return f'avatar/{instance.id}/{file}'


def validate_image_size(fiel_obj):
    """Проверка размера файла"""
    if fiel_obj.size > SIZE_LIMIT * 1024 * 1024:
        raise ValidationError(f'Максимальный размер файла {SIZE_LIMIT}Mb.')
