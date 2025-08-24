from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer
from .tasks import send_order_confirmation_email


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def create(self, request):
        cart = request.user.cart
        order = Order.objects.create(
            user=request.user, state="new", contact=request.data["contact"]
        )
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order, product_info=item.product_info, quantity=item.quantity
            )
        cart.items.all().delete()
        send_order_confirmation_email.delay(order.id)
        return Response({"status": "Заказ создан", "order_id": order.id}, status=201)
