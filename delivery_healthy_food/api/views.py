from rest_framework import status, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from djoser.serializers import SetPasswordSerializer
from djoser.views import UserViewSet

from users.models import User
from products.models import (
    Product, ShoppingCart, Favorite)
from .serializers import (
    ProductSerializer,
    FavoriteSerializer,
    ShoppingCartSerializer,
    UserPostSerializer,
    UserGetSerializer
)


class CustomUserViewSet(UserViewSet):
    """Вьюсет для модели пользователей."""
    queryset = User.objects.all()
    serializer_class = UserPostSerializer
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return UserGetSerializer
        return UserPostSerializer

    @action(detail=False, methods=['post'],
            permission_classes=(IsAuthenticated,))
    def set_password(self, request):
        serializer = SetPasswordSerializer(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     GenericViewSet):
    """Вьюсет для модели продуктов."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)


class FavoriteViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      GenericViewSet):
    """Вьюсет для модели продуктов."""
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        """Метод добавления продукта в избранное."""
        product = get_object_or_404(Product, id=kwargs['id'])
        user = request.user
        serializer = FavoriteSerializer(
            data={'user': user.id, 'product': product.id})
        serializer.is_valid(raise_exception=True)
        Favorite.objects.create(user=user, product=product)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        product = get_object_or_404(Product, id=kwargs['id'])
        user = request.user
        favorite = Favorite.objects.filter(user=user.id, product=product.id)
        if not favorite:
            return Response({'errors': 'Этого продукта нет в избранном!'},
                            status=status.HTTP_400_BAD_REQUEST)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartViewSet(ModelViewSet):
    """Вьюсет для модели корзины продуктов."""
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ["get", "post", "patch", "delete"]

    def create(self, request, *args, **kwargs):
        """Метод для добавления продукта в корзину."""
        product = get_object_or_404(Product, id=kwargs['id'])
        user = request.user
        serializer = ShoppingCartSerializer(
            data={'user': user.id, 'product': product.id},
            context={"request": request})
        serializer.is_valid(raise_exception=True)
        ShoppingCart.objects.create(user=user, product=product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

    def destroy(self, request, *args, **kwargs):
        """Метод для удаления продукта из корзины."""
        product = get_object_or_404(Product, id=kwargs['id'])
        user = request.user
        shopping_cart = ShoppingCart.objects.filter(
            product=product.id, user=user.id)
        if not shopping_cart:
            return Response({'errors': 'Этого продукта нет в корзине!'},
                            status=status.HTTP_400_BAD_REQUEST)
        shopping_cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

