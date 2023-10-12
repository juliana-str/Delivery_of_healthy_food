from rest_framework import serializers

from .models import Product, ShoppingCart, Favorite


class ProductSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели продуктов."""
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Product

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Favorite.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(user=user, recipe=obj).exists()


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели избранных продуктов."""

    class Meta:
        fields = '__all__'
        model = Favorite



class ShoppingCartSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = ShoppingCart
