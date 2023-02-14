from django.urls import path

from .views import StripeIntentView, CustomPaymentView

urlpatterns = [
    path('buy/<int:item_id>/', StripeIntentView.as_view(), name='buy'),
    path('item/<int:item_id>/', CustomPaymentView.as_view(), name='item'),
]