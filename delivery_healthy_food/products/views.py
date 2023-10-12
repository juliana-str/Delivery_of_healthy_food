from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Product, ShoppingCart, Favorite
from .serializers import (
    ProductSerializer,
    FavoriteSerializer,
    ShoppingCartSerializer
)


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

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, **kwargs):
        """Метод добавления продукта в избранное."""
        product = get_object_or_404(Product, id=kwargs['pk'])
        user = request.user
        if request.method == 'POST':
            serializer = FavoriteSerializer(
                data={'user': user.id, 'product': product.id})
            serializer.is_valid(raise_exception=True)
            Favorite.objects.create(user=user, product=product)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)

        favorite = Favorite.objects.filter(user=user.id, product=product.id)
        if not favorite:
            return Response({'errors': 'Этого продукта нет в избранном!'},
                            status=status.HTTP_400_BAD_REQUEST)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartViewSet(mixins.ListModelMixin,
                          mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          GenericViewSet):
    """Вьюсет для модели корзины продуктов."""
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, **kwargs):
        """Метод для создания, удаления списка продуктов."""
        product = get_object_or_404(Product, id=kwargs['pk'])
        user = request.user
        if request.method == 'POST':
            serializer = ShoppingCartSerializer(
                data={'user': user.id, 'product': product.id},
                context={"request": request})
            serializer.is_valid(raise_exception=True)
            ShoppingCart.objects.create(user=user, product=product)
            return Response(serializer.data, status=status.HTTP_200_OK)

        shopping_cart = ShoppingCart.objects.filter(
            product=product.id, user=user.id)
        if not shopping_cart:
            return Response({'errors': 'Этого продукта нет в списке покупок!'},
                            status=status.HTTP_400_BAD_REQUEST)
        shopping_cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
