from django_filters.rest_framework import filters, FilterSet
from products.models import Product, Category


class ProductFilter(FilterSet):
    """Фильтры продуктов."""
    name = filters.CharFilter(lookup_expr='istartswith')
    producer = filters.CharFilter(lookup_expr='istartswith')
    price = filters.RangeFilter()
    categories = filters.ModelMultipleChoiceFilter(
        field_name='category__slug',
        to_field_name='slug',
        queryset=Category.objects.all()
    )
    is_favorited = filters.BooleanFilter(method='get_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_is_in_shopping_cart')

    class Meta:
        model = Product
        fields = ('name', 'categories',
                  'is_favorited', 'is_in_shopping_cart',
                  'producer', 'price')

    def get_is_favorited(self, queryset, name, value):
        if self.request.user.is_authenticated:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if self.request.user.is_authenticated:
            return queryset.filter(shopping_carts__user=self.request.user)
        return queryset


class CategoryFilter(FilterSet):
    """Фильтры категорий."""
    name = filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Product
        fields = ('name', 'slug')
