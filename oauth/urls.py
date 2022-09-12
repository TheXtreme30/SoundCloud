from django.urls import path

from . import views

urlpatterns = [
    path('google_login', views.google_auth),
]