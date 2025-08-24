from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from celery import shared_task


def send_supplier_notification(shop_name, product_count):
    """
    Уведомление администратора о новом импорте товаров
    """
    subject = f"Обновление ассортимента в {shop_name}"
    message = f"Добавлено {product_count} новых товаров"

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.ADMIN_EMAIL],
    )


@shared_task
def async_send_order_status_update(order_id, new_status):
    """
    Асинхронная отправка уведомления об изменении статуса заказа
    """
    from ..models import Order

    order = Order.objects.get(id=order_id)
    subject = f"Статус заказа №{order.id} изменен"
    html_message = render_to_string(
        "emails/order_status_update.html", {"order": order, "new_status": new_status}
    )

    send_mail(
        subject=subject,
        message="",
        html_message=html_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[order.user.email],
        fail_silently=False,
    )
