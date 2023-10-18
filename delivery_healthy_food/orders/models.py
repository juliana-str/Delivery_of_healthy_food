from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from users.models import User
from products.models import Product


STATUS = ['Оформлен', 'В обработке', 'Комплектуется', 'Собран',
          'Передан в доставку', 'Доставлен', 'Завершен']

PAYMENT_METHODS = ['Наличные', 'Картой на сайте', 'При получении']

DELIVERY_METHOD = ['Пункт выдачи', 'Курьером']


class ShoppingCart(models.Model):
    """Model for creating a shopping cart."""
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
    quantity = models.IntegerField(
        verbose_name='Количество товара',
        validators=[
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


class Order(models.Model):
    """Model for creating an order."""
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Покупатель'
    )
    goods = models.ForeignKey(
        ShoppingCart,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Покупки'
    )
    date = models.DateField(
        verbose_name='Дата оформления',
        auto_now_add=True
    )
    status = models.CharField(
        choices=STATUS,
        default='Оформлен'
        )
    payment_method = models.CharField(
        choices=PAYMENT_METHODS,
        default='Картой на сайте'
    )
    is_paid = models.BooleanField(default=False)
    comment = models.TextField(
        max_length=400,
        null=True
    )
    delivery_method = models.CharField(
        choices=DELIVERY_METHOD,
        default='Курьером'
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'