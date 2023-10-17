# Generated by Django 3.2 on 2023-10-17 07:22

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Категория товара')),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name': 'Категория товара',
                'verbose_name_plural': 'Категории товара',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Избранное',
                'verbose_name_plural': 'Избранное',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Название')),
                ('measure_unit', models.CharField(max_length=200, verbose_name='Единица измерения')),
                ('amount', models.FloatField(validators=[django.core.validators.MinValueValidator(1, 'Разрешены значения от 1 до 1000'), django.core.validators.MaxValueValidator(1000, 'Разрешены значения от 1 до 1000')], verbose_name='Количество')),
                ('description', models.CharField(max_length=200, verbose_name='Описание')),
                ('image', models.ImageField(upload_to='products/media', verbose_name='Изображение')),
                ('producer', models.CharField(max_length=100, verbose_name='Производитель')),
                ('price', models.FloatField(validators=[django.core.validators.MinValueValidator(1, 'Разрешены значения от 1 до 10000'), django.core.validators.MaxValueValidator(10000, 'Разрешены значения от 1 до 10000')], verbose_name='Цена')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукты',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count_of_product', models.IntegerField(validators=[django.core.validators.MinValueValidator(1, 'Разрешены значения от 1 до 100'), django.core.validators.MaxValueValidator(10000, 'Разрешены значения от 1 до 100')], verbose_name='Количество товара')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopping_carts', to='products.product', verbose_name='Продукт в корзине')),
            ],
            options={
                'verbose_name': 'Корзина',
                'verbose_name_plural': 'Корзина',
            },
        ),
    ]
