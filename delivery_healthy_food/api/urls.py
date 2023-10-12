from django.urls import include, path
from rest_framework.routers import DefaultRouter

from delivery_healthy_food.users.views import CustomUserViewSet
from delivery_healthy_food.products.views import ProductViewSet

app_name = 'api'

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='users')
router.register(r'products', ProductViewSet, basename='products')


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
