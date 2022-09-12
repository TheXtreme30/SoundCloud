from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()

router.register(r'genres', views.GenreView, basename='genres_api_v1')
router.register(r'users', views.UserView, basename='users_api_v1')
router.register(r'users/(?P<user_id>\d+)/albums', views.AlbumView, basename='albums_api_v1')
router.register(r'users/(?P<user_id>\d+)/playlist', views.PlaylistView, basename='playlist_api_v1')
router.register(r'users/(?P<user_id>\d+)/titles', views.TitleView, basename='titles_api_v1')
router.register(r'users/(?P<user_id>\d+)/titles/(?P<title_id>\d+)/comments',
                views.CommentView, basename='comments_api_v1')


urlpatterns = [
    path('', include(router.urls)),
]
