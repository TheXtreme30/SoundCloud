from django.db import models
from django.core.validators import validate_image_file_extension

from oauth.services import get_avatar_upload_path, validate_image_size


class AuthUser(models.Model):
    """Модель пользователя"""
    email = models.EmailField(max_length=255, unique=True)
    join_date = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(max_length=1024, blank=True, null=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.ImageField(
        upload_to=get_avatar_upload_path,
        blanc=True, null=True,
        validators=[validate_image_file_extension, validate_image_size],
    )

    @property
    def is_authenticated(self):
        return True

    def __str__(self):
        return self.email
        
        
class Follower(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='owner')
    subscriber = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='subscriber')
    
    def __str__(self):
        return f'{self.subscriber} подписан на {self.user}'
