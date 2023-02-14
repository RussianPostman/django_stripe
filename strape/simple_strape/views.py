import json
import stripe
from django.conf import settings
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.views import View

from .models import Item, Order
from .services import (current_obj, get_item_prise, multi_item_prise,
                       get_display_price, write_transaction)

stripe.api_key = settings.STRIPE_SECRET_KEY


class ItemIntentView(View):
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
                    'name': current_item.name,
                    'type': 'Item',
                    'item_id': current_item.pk
                }
            )
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return JsonResponse({'error': str(e)})


class ItemPaymentView(TemplateView):
    template_name = 'item_checkout.html'

    def get_context_data(self, **kwargs):
        current_item = current_obj(self.kwargs.get('item_id'), Item)
        price = get_display_price(get_item_prise(current_item))
        context = super(ItemPaymentView, self).get_context_data(**kwargs)
        context.update({
            'item': current_item,
            'price': price,
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
        })
        return context


class OrderIntentView(View):
    def post(self, request, *args, **kwargs):
        try:
            current_order = current_obj(self.kwargs.get('item_id'), Order)
            order_items = current_order.items.all()
            final_price = multi_item_prise(order_items)

            req_json = json.loads(request.body)
            customer = stripe.Customer.create(email=req_json['email'])
            intent = stripe.PaymentIntent.create(
                amount=final_price,
                currency=order_items[0].currency,  # костыль для выбора валюты
                customer=customer['id'],
                metadata={
                    'name': current_order.name,
                    'type': 'Order',
                    'item_id': current_order.pk
                }
            )
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return JsonResponse({'error': str(e)})


class OrderPaymentView(TemplateView):
    template_name = 'order_checkout.html'

    def get_context_data(self, **kwargs):
        current_order = current_obj(self.kwargs.get('item_id'), Order)
        order_items = current_order.items.all()
        final_price = get_display_price(multi_item_prise(order_items))
        context = super(OrderPaymentView, self).get_context_data(**kwargs)
        context.update({
            'currency': order_items[0].currency,
            'order': current_order,
            'order_items': order_items,
            'price': final_price,
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
        })
        return context


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)

    if event['type'] == 'payment_intent.succeeded':
        intent = event['data']['object']
        write_transaction(intent)

    return HttpResponse(status=200)
