from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Order

@shared_task(bind=True, max_retries=3)
def send_order_confirmation_email(self, order_id):
    try:
        order = Order.objects.get(id=order_id)
        subject = f"Подтверждение заказа №{order.id}"
        html_message = render_to_string('emails/order_created.html', {'order': order})
        send_mail(
            subject=subject,
            message='',
            html_message=html_message,
            from_email='noreply@procurement.com',
            recipient_list=[order.user.email],
            fail_silently=False
        )
    except Exception as e:
        self.retry(exc=e, countdown=60)
