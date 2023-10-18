from django.contrib import admin

from orders.models import ShoppingCart, Order


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'count_of_product')
    list_editable = ('user', 'product', 'count_of_product')
    search_fields = ('user',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'goods', 'date', 'status',
                    'payment_method', 'is_paid', 'comment', 'delivery_method')
    list_editable = ('date', 'status', 'payment_method',
                     'is_paid', 'comment', 'delivery_method')
    readonly_fields = ('customer', 'goods')
