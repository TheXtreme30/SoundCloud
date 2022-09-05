from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register('me', views.UserView, basename='me')
router.register('author', views.AuthorView, basename='author')

urlpatterns = [
    path('', include(router.urls)),

    path('google/', views.google_auth),
    path('', views.google_login),
]
