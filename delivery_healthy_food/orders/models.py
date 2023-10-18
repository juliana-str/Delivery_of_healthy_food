from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from users.models import User
from products.models import Product


STATUS = [(1, 'Оформлен'), (2, 'В обработке'), (3, 'Комплектуется'),
          (4, 'Собран'),(5, 'Передан в доставку'),
          (6, 'Доставлен'), (7, 'Завершен')]

PAYMENT_METHODS = [(1, 'Наличные'), (2, 'Картой на сайте'),
                   (3,'При получении')]

DELIVERY_METHOD = [(1, 'Пункт выдачи'), (2, 'Курьером')]


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
    # customer = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE,
    #     related_name='orders',
    #     verbose_name='Покупатель'
    # )
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
        max_length=50,
        choices=STATUS,
        default=1
        )
    payment_method = models.CharField(
        max_length=50,
        choices=PAYMENT_METHODS,
        default=2
    )
    is_paid = models.BooleanField(default=False)
    comment = models.TextField(
        max_length=400,
        blank=True
    )
    delivery_method = models.CharField(
        max_length=50,
        choices=DELIVERY_METHOD,
        default=2
    )
    discount = models.IntegerField(
        default=0
    )
    total_price = models.IntegerField(
        default=0
    )

    class Meta:
        ordering = ['-date']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'