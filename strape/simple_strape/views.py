import json
from django.views.generic import TemplateView
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views import View

from .models import Item  # Tax, Discount, Order
from .services import current_obj, get_item_prise

stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeIntentView(View):
    def post(self, request, *args, **kwargs):
        try:
            current_item = current_obj(self.kwargs.get('item_id'), Item)
            price = get_item_prise(current_item)

            req_json = json.loads(request.body)
            customer = stripe.Customer.create(email=req_json['email'])
            intent = stripe.PaymentIntent.create(
                amount=price,
                currency=current_item.currency,
                customer=customer['id'],
                metadata={
                    "item_id": current_item.pk
                }
            )
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return JsonResponse({'error': str(e)})


class CustomPaymentView(TemplateView):
    template_name = 'checkout.html'

    def get_context_data(self, **kwargs):
        current_item = current_obj(self.kwargs.get('item_id'), Item)
        price = get_item_prise(current_item)
        context = super(CustomPaymentView, self).get_context_data(**kwargs)
        context.update({
            'item': current_item,
            'price': price,
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
        })
        return context
