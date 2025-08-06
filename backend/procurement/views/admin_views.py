from django.contrib import admin
from django.http import JsonResponse
from .models import Order

@admin.action(description='Экспорт заказов в JSON')
def export_orders_json(modeladmin, request, queryset):
    """Действие в админке для экспорта заказов"""
    orders_data = []
    for order in queryset:
        orders_data.append({
            'id': order.id,
            'client': order.client.email,
            'total_amount': str(order.total_amount)
        })
    return JsonResponse(orders_data, safe=False)

class OrderAdmin(admin.ModelAdmin):
    actions = [export_orders_json]
