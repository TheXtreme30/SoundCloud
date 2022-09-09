from django.core.validators import validate_image_file_extension
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

from oauth.services.services import get_avatar_upload_path, validate_image_size


class CustomUserManager(BaseUserManager):
    def create_user(self, email, join_date, password=None):
        if not email:
            raise ValueError('Пользователи должны иметь адрес электронной почты')

        user = self.model(
            email=self.normalize_email(email),
            join_date=join_date,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, join_date, password=None):
        user = self.create_user(
            email,
            password=password,
            join_date=join_date,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    """Модель пользователя."""
    email = models.EmailField(max_length=256, unique=True)
    join_date = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=256, blank=True)
    city = models.CharField(max_length=256, blank=True)
    bio = models.TextField(max_length=1024, blank=True)
    username = models.CharField(max_length=256, blank=True)
    avatar = models.ImageField(
        upload_to=get_avatar_upload_path,
        blank=True, null=True,
        validators=[validate_image_file_extension, validate_image_size],
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['join_date']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
