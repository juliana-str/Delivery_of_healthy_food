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


class ShoppingCartGetSerializer(serializers.ModelSerializer):
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


class ShoppingCartPostSerializer(serializers.ModelSerializer):
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

    # def update(self, instance, validated_data):
    #     count_of_product = validated_data.pop('count_of_product', 1)
    #     ShoppingCart.objects.create(
    #                 product=instance,
    #                 user=self.context['request'].user,
    #                 count_of_product=count_of_product
    #         )
    #     return super().update(instance, validated_data)

    # def create(self, request, *args, **kwargs):
    #     """Метод для добавления продукта в корзину."""
    #     product = request.data
    #     user = request.user
    #     print(product, user)
    #     serializer = ShoppingCartSerializer(
    #         data={'user': user.id, 'product': product['product']},
    #         context={"request": request.data})
    #     serializer.is_valid(raise_exception=True)
    #     ShoppingCart.objects.create(product=product, user=user, count)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    #
    # @transaction.atomic
    # def create(self, validated_data):
    #     user = self.context['request'].user
    #     product = validated_data.pop('product')
    #     count_of_product = validated_data.pop('count_of_product')
    #     cart = ShoppingCart.objects.create(**validated_data,
    #                                    )
    #     ShoppingCart.objects.bulk_create(
    #         ShoppingCart(
    #             product=product,
    #             count_of_product=count_of_product,
    #             user=user
    #     ))
    #     return cart
    #
    #
    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(
    #         instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #
    # def destroy(self, request, *args, **kwargs):
    #     """Метод для удаления продукта из корзины."""
    #     product = get_object_or_404(Product, id=kwargs['id'])
    #     user = request.user
    #     shopping_cart = ShoppingCart.objects.filter(
    #         product=product.id, user=user.id)
    #     if not shopping_cart:
    #         return Response({'errors': 'Этого продукта нет в корзине!'},
    #                         status=status.HTTP_400_BAD_REQUEST)
    #     shopping_cart.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

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


