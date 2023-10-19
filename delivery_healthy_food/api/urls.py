from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CustomUserViewSet,
    CategoryViewSet,
    ProductViewSet,
    FavoriteViewSet,
)

app_name = 'api'

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='users')
router.register(r'products', ProductViewSet, basename='products')
router.register(r'favorites', FavoriteViewSet, basename='favorites')
router.register(r'categories', CategoryViewSet, basename='categories')


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
