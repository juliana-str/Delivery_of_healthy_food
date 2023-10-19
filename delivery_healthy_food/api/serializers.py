from django.db import transaction
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from products.models import Product, Favorite, Category
from users.models import User

from orders.models import Order, ShoppingCart


class UserGetSerializer(UserCreateSerializer):
    """Сериалайзер для модели пользователей, просмотр."""

    class Meta:
        fields = ('id',
                  'email',
                  'username',
                  'first_name',
                  'last_name',
                  'phone_number',
                  'address'
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
            'password',
            'phone_number',
            'address'
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
        fields = ('product_name',
                  'product_amount', 'product_price')

    def get_product_name(self, obj):
        return obj.product.name

    def get_product_amount(self, obj):
        return obj.product.amount

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


class OrderListSerializer(serializers.ModelSerializer):
    """Serializer for list orders."""
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('user', 'goods', 'date', 'status',
                  'is_paid','total_price')

    def get_total_price(self,obj):
        return sum(obj.goods.price)


class OrderPostDeleteSerializer(serializers.ModelSerializer):
    """Serializer for create/delete orders."""

    goods = ShoppingCartListSerializer()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('user', 'goods',
                  'date', 'status', 'payment_method', 'is_paid',
                  'delivery_method', 'comment', 'total_price')

    def get_goods(self, obj):
        print(obj)
        return ShoppingCart.filter(
            shopping_carts__user=self.context['request'].user)

    def get_total_price(self, obj):
        total = obj.goods.price
        if obj.discount:
            return (total * obj.discount)/100
        return total

    # @transaction.atomic
    # def create(self, validated_data):
    #     user = self.context['request'].user
    #     payment_method = validated_data.pop('payment_method')
    #     status = validated_data.pop('status')
    #     is_paid = validated_data.pop('is_paid ')
    #     comment = validated_data.pop('comment')
    #     total_price = validated_data.pop('total_price')
    #     delivery_method = validated_data.pop('delivery_method')
    #     goods = validated_data.pop('good')
    #     order = Order.objects.create(
    #         user=user,
    #         goods=goods,
    #         payment_method=payment_method,
    #         status=status,
    #         is_paid=is_paid,
    #         comment=comment,
    #         delivery_method=delivery_method,
    #         total_price=total_price
    #     )
    #     return order

    # @transaction.atomic
    # def update(self, instance, validated_data):
    #     ingredient = validated_data.get('ingredient')
    #     amount = validated_data.get('amount')
    #     recipe = validated_data.get('recipe')
    #     ingredient_in_recipe = IngredientInRecipe.objects.get(
    #         ingredient=ingredient,
    #         amount=amount,
    #         recipe=recipe
    #     )
    #     if validated_data:
    #         ingredient_in_recipe.save()