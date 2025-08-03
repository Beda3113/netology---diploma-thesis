from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Order, User

@shared_task(bind=True, max_retries=3)
def send_order_confirmation_email(self, order_id):
    """
    Отправка email-подтверждения заказа клиенту
    """
    try:
        order = Order.objects.get(id=order_id)
        user = order.user
        
        subject = f"Подтверждение заказа №{order.id}"
        message = render_to_string('emails/order_confirmation.html', {
            'order': order,
            'user': user
        })
        
        send_mail(
            subject=subject,
            message='',  # Текстовая версия (пустая, т.к. используем html_message)
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=message,
            fail_silently=False
        )
        
    except Exception as e:
        self.retry(exc=e, countdown=60)  # Повтор через 60 сек при ошибке


@shared_task
def update_partner_products(supplier_id, yaml_url):
    """
    Фоновая задача для обновления товаров поставщика
    """
    from .utils.import_parser import import_products_from_yaml
    from .models import User
    
    try:
        supplier = User.objects.get(id=supplier_id, role='supplier')
        import_products_from_yaml(yaml_url, supplier)
    except Exception as e:
        logger.error(f"Ошибка импорта товаров: {str(e)}")


@shared_task
def notify_partner_about_order(order_id):
    """
    Уведомление поставщика о новом заказе
    """
    order = Order.objects.get(id=order_id)
    suppliers_emails = list(
        set(item.product.supplier.user.email for item in order.items.all())
    )
    
    for email in suppliers_emails:
        send_mail(
            subject=f"Новый заказ №{order.id}",
            message=f"В вашем магазине оформлен заказ на сумму {order.total_amount}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email]
        )
