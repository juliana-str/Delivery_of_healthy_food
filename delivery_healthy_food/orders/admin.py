from django.contrib import admin

from orders.models import ShoppingCart, Order


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity')
    list_editable = ('user', 'product', 'quantity')
    search_fields = ('user',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'goods',
                    'date', 'status', 'payment_method', 'is_paid',
                    'delivery_method', 'comment', 'discount', 'total_price')
    list_editable = ('status', 'payment_method',
                     'is_paid', 'comment', 'delivery_method')

