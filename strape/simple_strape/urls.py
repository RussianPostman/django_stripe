from django.urls import path

from .views import (
    ItemIntentView,
    ItemPaymentView,
    OrderIntentView,
    OrderPaymentView,
    stripe_webhook
    )

urlpatterns = [
    path(
        'item/buy/<int:item_id>/',
        ItemIntentView.as_view(),
        name='item_buy'
    ),
    path(
        'item/view/<int:item_id>/',
        ItemPaymentView.as_view(),
        name='item'
    ),
    path(
        'order/buy/<int:item_id>/',
        OrderIntentView.as_view(),
        name='order_buy'
    ),
    path(
        'order/view/<int:item_id>/',
        OrderPaymentView.as_view(),
        name='order'
    ),
    path(
        'webhooks/stripe/',
        stripe_webhook,
        name='stripe-webhook'
    ),
]
