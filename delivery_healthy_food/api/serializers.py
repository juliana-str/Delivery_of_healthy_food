from django.db import transaction
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from products.models import Product, ShoppingCart, Favorite, Category
from users.models import User

from delivery_healthy_food.orders.models import Order


class UserGetSerializer(UserCreateSerializer):
    """Сериалайзер для модели пользователей, просмотр."""

    class Meta:
        fields = ('id',
                  'email',
                  'username',
                  'first_name',
                  'last_name',
                  )
        model = User


class UserPostSerializer(UserCreateSerializer):
    """Сериалайзер для модели пользователей, создание, изменение, удаление."""

    class Meta:
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )
        model = User


class CategorySerializer(serializers.ModelSerializer):
    """Сериалайзер для модели категорий продуктов."""

    class Meta:
        fields = '__all__'
        model = Category


class ProductSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели продуктов."""
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    category = serializers.ReadOnlyField(source='category.name')

    class Meta:
        fields = '__all__'
        model = Product

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Favorite.objects.filter(user=user, product=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(user=user, product=obj).exists()


class ProductMinifiedSerializer(serializers.ModelSerializer):
    """Сериалайзер для представления продукта."""

    class Meta:
        model = Product
        fields = ('name', 'image', 'price')


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели избранных продуктов."""

    class Meta:
        fields = '__all__'
        model = Favorite
        validators = (
            serializers.UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=('user', 'product'),
                message='Вы уже добавили этот продукт в избранное!'
            ),
        )

    def to_representation(self, instance):
        instance = instance.product
        return ProductMinifiedSerializer(instance, context=self.context).data


class ShoppingCartListSerializer(serializers.ModelSerializer):
    """Сериалайзер для представления продукта."""
    product_name = serializers.SerializerMethodField()
    product_amount = serializers.SerializerMethodField()
    product_price = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingCart
        fields = ('product_name', 'count_of_product',
                  'product_amount', 'product_price')

    def get_product_name(self, obj):
        return obj.product.name

    def get_product_amont(self, obj):
        return obj.product.weight

    def get_product_price(self, obj):
        return obj.product.price


class ShoppingCartPostUpdateSerializer(serializers.ModelSerializer):
    count_of_product = serializers.IntegerField(default=1)

    class Meta:
        fields = '__all__'
        model = ShoppingCart
        validators = (
            serializers.UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=('user', 'product'),
                message='Вы уже добавили этот продукт в корзину!'
            ),
        )

    def validate_count_of_product(self, data):
        if data < 1:
            raise serializers.ValidationError(
                'Количество  товара в корзине должно быть не меньше 1!')
        return data

    # @transaction.atomic
    # def update(self, instance, validated_data):
    #     product = validated_data.get('product')
    #     user = validated_data.get('user')
    #     count_of_product = validated_data.pop('count_of_product', 1)
    #     shopping_cart = ShoppingCart.objects.get(
    #         product=product,
    #         user=user,
    #         count_of_product=count_of_product
    #     )
    #     if validated_data:
    #         shopping_cart.save()
    #         return shopping_cart

class OrderSerializer(serializers.ModelSerializer):
    """Serializer for create/update/delete orders."""
    customer_data = serializers.SerializerMethodField()
    shopping_cart_products = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('customer_data', 'shopping_cart_products',
                  'date', 'status', 'is_paid')

    def get_customer_data(self, obj):
        name = obj.user.name
        surname = obj.user.surname
        address = obj.user.address
        phone_number = obj.user.phone_number
        return name, surname, address, phone_number

    def get_shopping_cart_products(self, obj):
        return ShoppingCart.filter(
            shopping_carts__user=self.context['request'].user)
