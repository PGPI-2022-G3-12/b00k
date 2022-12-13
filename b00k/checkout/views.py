from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from django.conf import settings
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from store.models import Cart

import json
import os
import stripe

def home(request,cart_id):
    
    cart_string_id = str(cart_id)
    url = '/checkout/'+ cart_string_id +'/create-checkout-session/'
    context = {'url':url}
    return render(request,'checkout.html', context=context)

def success(request,cart_id):
    return render(request,'success.html')

def cancel(request,cart_id):
    return render(request,'cancel.html')


stripe.api_key = settings.STRIPE_SECRET_KEY
YOUR_DOMAIN = 'http://127.0.0.1:8000'

@csrf_exempt
def create_checkout_session(request,cart_id):
    print("Ve al checkout")

    cart = Cart.objects.get(id=cart_id)
    total_price = cart.totalPrice

    session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=[{
        'price_data': {
            'currency': 'eur',
            'product_data': {
                'name': 'Total a pagar',
             },
             'unit_amount': total_price,
         },
         'quantity': 1,
     }],
     mode='payment',
     success_url=YOUR_DOMAIN + '/checkout/success.html',
     cancel_url=YOUR_DOMAIN + '/checkout/cancel.html',
    )
    return JsonResponse({'id': session.id})
