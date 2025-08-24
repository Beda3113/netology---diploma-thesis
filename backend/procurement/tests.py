from django.test import TestCase
from procurement.models import User, Cart, CartItem


class CartModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@example.com", password="test")
        self.cart = Cart.objects.create(user=self.user)

    def test_cart_total_price(self):
        item = CartItem.objects.create(
            cart=self.cart, product_info__price=100, quantity=2
        )
        self.assertEqual(self.cart.total_price, 200)
