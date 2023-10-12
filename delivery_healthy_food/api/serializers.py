from django.db import transaction
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from products.models import Product, ShoppingCart, Favorite
from users.models import User


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
        fields = ('name', 'image', 'weight')


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


class ProductMiniCartSerializer(serializers.ModelSerializer):
    """Сериалайзер для представления продукта."""
    product_name = serializers.SerializerMethodField()
    product_weight = serializers.SerializerMethodField()

    class Meta:
        model = ShoppingCart
        fields = ('product_name', 'count_of_product', 'product_weight')

    def get_product_name(self, obj):
        return obj.product.name

    def get_product_weight(self, obj):
        return obj.product.weight


class ShoppingCartSerializer(serializers.ModelSerializer):
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

    def validate_product(self, data):
        user = self.context['request'].user
        if ShoppingCart.objects.filter(product=data, user=user).exists():
            raise serializers.ValidationError('Продукт уже в корзине.')
        return data

    def validate_count_of_product(self, data):
        if data < 1:
            raise serializers.ValidationError(
                'Количество  товара в корзине должно быть не меньше 1!')
        return data


    # def update(self, instance, validated_data):
    #     count_of_product = validated_data.pop('count_of_product', 1)
    #     ShoppingCart.objects.create(
    #                 product=instance,
    #                 user=self.context['request'].user,
    #                 count_of_product=count_of_product
    #         )
    #     return super().update(instance, validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        product = validated_data.get('product')
        user = validated_data.get('user')
        count_of_product = validated_data.pop('count_of_product', 1)
        shopping_cart = ShoppingCart.objects.get(
            product=product,
            user=user,
            count_of_product=count_of_product
        )
        if validated_data:
            shopping_cart.save()

    # def to_representation(self, instance):
    #
    #     product = Product.objects.get(instance.product)
    #     print(product)
    #     return ProductMiniCartSerializer(product).data

    def to_representation(self, instance):

        return ProductMiniCartSerializer(instance, context=self.context).data
