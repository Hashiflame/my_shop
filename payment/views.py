from decimal import Decimal
import stripe
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from orders.models import Order


stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


def payment_process(request):
    
    order_id = request.session.get('order_id', None)
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        success_url = request.build_absolute_uri(
            reverse('payment:complated'))
        cancel_url = request.build_absolute_uri(
            reverse('payment:canceled'))
        
        #session data of Stripe payment generation
        session_data = {
            'mode': 'payment',
            'client_reference_id': order.id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': []
        }
        #adding products to order in session payment
        for item in order.items.all():
            session_data['line_items'].append({
                'price_data':{
                    'unit_amount': int(item.price * Decimal('100')),
                    'currency':'inr',
                    'product_data': {
                        'name': item.product.name,
                    },
                },
                'quantity': item.quantity,
            })
        #Stripe coupon
        if order.coupon:
            stripe_coupon = stripe.Coupon.create(name=order.coupon.code,
                                                 percent_off=order.discount,
                                                 duration='once')
            session_data['discounts'] = [{
                'coupon': stripe_coupon.id
            }]
        
        #creating session for Stripe payment
        session = stripe.checkout.Session.create(**session_data)
        #redirect to Stripe payment form
        return redirect(session.url, code=303)
    else:
        return render(request, 'payment/process.html', locals())
    
def payment_complated(request):
    return render(request, 'payment/complated.html')

def payment_canceled(request):
    return render(request, 'payment/canceled.html')