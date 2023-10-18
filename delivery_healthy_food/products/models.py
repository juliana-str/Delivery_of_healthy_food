from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from users.models import User

MEASURE_UNIT = ('гр', 'мл', 'шт', 'кг')


class Category(models.Model):
    """Модель для создания категории."""
    name = models.CharField(
        max_length=150,
        verbose_name='Категория товара',
        unique=True
    )
    slug = models.SlugField(
        max_length=50,
        unique=True
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категории товара'

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    """Модель для создания продукта."""
    name = models.CharField(
        max_length=150,
        verbose_name='Название',
        unique=True
    )
    measure_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения'
    )
    amount = models.FloatField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(1, 'Разрешены значения от 1 до 1000'),
            MaxValueValidator(1000, 'Разрешены значения от 1 до 1000')
    ]
    )
    description = models.CharField(
        max_length=200,
        verbose_name='Описание',
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='products/media'
    )
    producer = models.CharField(
        max_length=100,
        verbose_name='Производитель',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория'
    )
    price = models.FloatField(
        verbose_name='Цена',
        validators=[
            MinValueValidator(1, 'Разрешены значения от 1 до 10000'),
            MaxValueValidator(10000, 'Разрешены значения от 1 до 10000')
    ]
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return (f'{self.name}, ' 
                f'{self.price} '
                f'{self.measure_unit}, ' 
                f'{self.description}, '
                f'{self.category}, ' 
                f'{self.producer}.')


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


class ProductCategory(models.Model):
    """Модель связи моделей категорий и продуктов."""
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
