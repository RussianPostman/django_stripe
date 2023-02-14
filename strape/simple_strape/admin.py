from django.contrib import admin

from .models import Item, Tax, Discount, Order, Transaction


class ItemAdmin(admin.ModelAdmin):
    model = Item
    list_display = ('name', 'description', 'currency', 'price')
    search_fields = ('name', 'currency')
    filter_horizontal = ('tax', 'discount')


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


class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'view_obj',
        'customer',
        'created'
    )

    def view_obj(self, obj: Transaction):
        return obj


admin.site.register(Order, OrderAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Tax, TaxAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(Transaction, TransactionAdmin)
