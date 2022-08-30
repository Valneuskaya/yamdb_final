from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, SignUpAPI, TitleViewSet, TokenAPI,
                    UserViewSet)

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(
    r'titles',
    TitleViewSet,
    basename='titles'
)
router.register(
    r'genres',
    GenreViewSet,
)
router.register(
    r'categories',
    CategoryViewSet,
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', SignUpAPI.as_view()),
    path('auth/token/', TokenAPI.as_view()),
]
