from django.contrib import admin

from .models import Item, Tax, Discount, Order


class ItemAdmin(admin.ModelAdmin):
    model = Item
    list_display = ('name', 'description', 'currency', 'price')
    search_fields = ('name', 'currency')
    filter_horizontal = ('tax', 'discount')
    # list_filter = ('author', 'name', 'tags')


class TaxAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'value',
    )
    empty_value_display = '-пусто-'


class DiscountAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'value',
    )
    empty_value_display = '-пусто-'


class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = (
        'name',
    )
    filter_horizontal = ('items',)


admin.site.register(Order, OrderAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Tax, TaxAdmin)
admin.site.register(Discount, DiscountAdmin)
