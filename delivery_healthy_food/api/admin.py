from django.contrib import admin

from products.models import Favorite, ShoppingCart, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'weight', 'description', 'image')
    list_filter = ('name', )
    search_fields = ('^name', )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product')
    list_editable = ('user', 'product')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product')
    list_editable = ('user', 'product')

