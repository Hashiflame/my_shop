from io import BytesIO
from celery import shared_task
import weasyprint

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Order


@shared_task
def payment_complated(order_id):

    """task to send an email 
    notification upon successful payment of an order"""
    
    order = Order.objects.get(id=order_id)

    #create invoice email
    subject = f'My Shop - Invoice no.{order.id}'
    message = 'Please, find attached the invoice for your recent purchase.'
    email = EmailMessage(subject, 
                         message, 
                         'admin@myshop.com', 
                         [order.email])
    #PDF generation
    html = render_to_string('orders/order/pdf.html', {'order': order})
    out = BytesIO
    stylesheets=[weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out, 
                                           stylesheets=stylesheets)
    #attach pdf file
    email.attach(f'order_{prder.id}.pdf', 
                 out.getvalue(),
                 'application/pdf')
    #sending email
    email.send()