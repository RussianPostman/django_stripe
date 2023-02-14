from .models import Item, Tax, Discount


def get_display_price(price):
    return "{0:.2f}".format(price / 100)


def get_item_prise(item: Item) -> int:
    item_prise = item.price
    one_percent_item_price = item_prise / 100
    discount_list: list[Discount] = item.discount.all()
    tax_list: list[Tax] = item.tax.all()

    tax_increase = 0
    full_discount = 0
    for i in tax_list:
        tax_increase += int(i.value * (item_prise / one_percent_item_price))

    for i in discount_list:
        full_discount += int(i.value * (item_prise / one_percent_item_price))

    return get_display_price(item_prise - full_discount + tax_increase)


def current_obj(id: int, django_model_obj):
    return django_model_obj.objects.get(pk=id)
