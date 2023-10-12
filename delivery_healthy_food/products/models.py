from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from delivery_healthy_food.users.models import User


class Product(models.Model):
    """Модель для создания продукта."""
    name = models.CharField(
        max_length=150,
        verbose_name='Название',
        unique=True
    )
    weight = models.FloatField(
        verbose_name='Вес',
        validators=[
                MinValueValidator(1, 'Разрешены значения от 1 до 10000'),
                MaxValueValidator(10000, 'Разрешены значения от 1 до 10000')
        ]
    )
    description = models.CharField(
        max_length=200,
        verbose_name='Описание',
    )
    image = models.ImageField(
        verbose_name='Изображение',
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f'{self.name}, {self.weight}, {self.description}.'


class Favorite(models.Model):
    """Модель для избранных продуктов."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Добавил в избранное'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Избранный продукт'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'product'],
                name='unique_favorite'
            )
        ]


class ShoppingCart(models.Model):
    """Модель для создания корзины покупок."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_carts',
        verbose_name='Добавил в корзину'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='shopping_carts',
        verbose_name='Продукт в корзине'
    )
    count_of_product = models.IntegerField(
        verbose_name='Количество товара',
        validators = [
                MinValueValidator(1, 'Разрешены значения от 1 до 100'),
                MaxValueValidator(10000, 'Разрешены значения от 1 до 100')
        ]
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'product'],
                name='unique_shopping_cart'
            )
        ]

