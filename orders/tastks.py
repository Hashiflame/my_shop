from celery import shared_task
from django.core.mail import send_mail
from .models import Order


@shared_task
def order_created(order_id):
    """
    Set up sending email notifications when an order 
    is successfully placed.
    """
    order = Order.objects.get(id=order_id)
    subject = f'Order no. {order_id}'
    message = f'Dear {order.first_name}, \n\n' \
                f'You have successfully placed an order.' \
                f'Your order ID is {order_id}'
    mail_sent = send_mail(subject,
                          message,
                          'admin@myshop.com',
                          [order.email])
    return mail_sent