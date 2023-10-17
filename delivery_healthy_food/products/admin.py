from django.contrib import admin

from .models import Favorite, ShoppingCart, Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measure_unit', 'description',
                    'image', 'producer', 'category', 'amount')
    list_filter = ('name', )
    search_fields = ('^name', )

    def category(self, obj):
        return ', '.join([str(category) for category in obj.category.all()])


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product')
    list_editable = ('user', 'product')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'count_of_product')
    list_editable = ('user', 'product', 'count_of_product')


admin.site.register(Category)
