from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer

class CartViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

class CartItemViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer
    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)
