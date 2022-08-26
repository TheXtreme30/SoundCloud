from django.core.exceptions import ValidationError

def get_avatar_upload_path(instance, file):
    """Построение пути к файлу: media/avatar/user_id/{file_name}"""
    return f'avatar/{instance.id}/{file}'

def validate_image_size(fiel_obj):
    """Проверка размера файла"""
    size_limit = 4
    if fiel_obj > size_limit * 1024 * 1024:
        raise ValidationError(f'Максимальный размер файла {size_limit}Mb.')
