from django.contrib import admin

from . import models


@admin.register(models.AuthUser)
class AuthUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'join_date')
    list_display_links = ('email',)
