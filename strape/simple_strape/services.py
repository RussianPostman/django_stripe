import stripe
from .models import Item, Tax, Discount, Transaction, Order


def get_display_price(price):
    return '{0:.2f}'.format(price / 100)


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

    return item_prise - full_discount + tax_increase


def current_obj(id: int, django_model_obj):
    return django_model_obj.objects.get(pk=id)


def multi_item_prise(obj_list) -> str:
    final_price = 0
    for item in obj_list:
        # тут должна быть ф-ция конфертации валют если они разные
        final_price += get_item_prise(item)
    return final_price


def write_transaction(intent: dict) -> None:
    transaction_type = intent['metadata']['type']
    stripe_customer_id = intent['customer']
    stripe_customer = stripe.Customer.retrieve(stripe_customer_id)
    item = Item.objects.get(pk=intent['metadata']['item_id'])

    transaction = Transaction(
        transaction=transaction_type,
        price=intent['amount'],
        customer=stripe_customer['email']
    )
    transaction.save()

    if transaction_type == 'Item':
        item = Item.objects.get(pk=intent['metadata']['item_id'])
        transaction.product.add(item)

    elif transaction_type == 'Order':
        items = Order.objects.get(pk=intent['metadata']['item_id']).items.all()
        for item in items:
            transaction.product.add(item)
