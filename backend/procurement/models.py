from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

# Выбор статусов заказа и типов пользователей
STATE_CHOICES = (
    ("basket", "Статус корзины"),
    ("new", "Новый"),
    ("confirmed", "Подтвержден"),
    ("assembled", "Собран"),
    ("sent", "Отправлен"),
    ("delivered", "Доставлен"),
    ("canceled", "Отменен"),
)

USER_TYPE_CHOICES = (
    ("shop", "Магазин"),
    ("buyer", "Покупатель"),
)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"
    objects = UserManager()

    email = models.EmailField("email address", unique=True)
    company = models.CharField("Компания", max_length=40, blank=True)
    position = models.CharField("Должность", max_length=40, blank=True)
    type = models.CharField(
        "Тип пользователя", choices=USER_TYPE_CHOICES, max_length=5, default="buyer"
    )
    is_active = models.BooleanField("active", default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Shop(models.Model):
    name = models.CharField("Название", max_length=50)
    url = models.URLField("Ссылка", null=True, blank=True)
    user = models.OneToOneField(
        User,
        verbose_name="Пользователь",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    state = models.BooleanField("статус получения заказов", default=True)

    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "Список магазинов"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField("Название", max_length=40)
    shops = models.ManyToManyField(
        Shop, verbose_name="Магазины", related_name="categories", blank=True
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Список категорий"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField("Название", max_length=80)
    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        related_name="products",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Список продуктов"

    def __str__(self):
        return self.name


class ProductInfo(models.Model):
    model = models.CharField("Модель", max_length=80, blank=True)
    external_id = models.PositiveIntegerField("Внешний ИД")
    product = models.ForeignKey(
        Product,
        verbose_name="Продукт",
        related_name="product_infos",
        on_delete=models.CASCADE,
    )
    shop = models.ForeignKey(
        Shop,
        verbose_name="Магазин",
        related_name="product_infos",
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField("Количество")
    price = models.PositiveIntegerField("Цена")
    price_rrc = models.PositiveIntegerField("Рекомендуемая розничная цена")

    class Meta:
        verbose_name = "Информация о продукте"
        constraints = [
            models.UniqueConstraint(
                fields=["product", "shop", "external_id"], name="unique_product_info"
            ),
        ]


class Parameter(models.Model):
    name = models.CharField("Название", max_length=40)

    class Meta:
        verbose_name = "Имя параметра"

    def __str__(self):
        return self.name


class ProductParameter(models.Model):
    product_info = models.ForeignKey(
        ProductInfo,
        verbose_name="Информация о продукте",
        related_name="product_parameters",
        on_delete=models.CASCADE,
    )
    parameter = models.ForeignKey(
        Parameter,
        verbose_name="Параметр",
        related_name="product_parameters",
        on_delete=models.CASCADE,
    )
    value = models.CharField("Значение", max_length=100)

    class Meta:
        verbose_name = "Параметр"
        constraints = [
            models.UniqueConstraint(
                fields=["product_info", "parameter"], name="unique_product_parameter"
            ),
        ]


class Contact(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        related_name="contacts",
        on_delete=models.CASCADE,
    )
    city = models.CharField("Город", max_length=50)
    street = models.CharField("Улица", max_length=100)
    house = models.CharField("Дом", max_length=15, blank=True)
    phone = models.CharField("Телефон", max_length=20)

    class Meta:
        verbose_name = "Контакт"

    def __str__(self):
        return f"{self.city} {self.street} {self.house}"


class Order(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        related_name="orders",
        on_delete=models.CASCADE,
    )
    dt = models.DateTimeField(auto_now_add=True)
    state = models.CharField("Статус", choices=STATE_CHOICES, max_length=15)
    contact = models.ForeignKey(
        Contact, verbose_name="Контакт", blank=True, null=True, on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Заказ"
        ordering = ("-dt",)

    def __str__(self):
        return str(self.dt)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        verbose_name="Заказ",
        related_name="ordered_items",
        on_delete=models.CASCADE,
    )
    product_info = models.ForeignKey(
        ProductInfo,
        verbose_name="Информация о продукте",
        related_name="ordered_items",
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField("Количество")

    class Meta:
        verbose_name = "Заказанная позиция"
        constraints = [
            models.UniqueConstraint(
                fields=["order_id", "product_info"], name="unique_order_item"
            ),
        ]


class Cart(models.Model):
    user = models.OneToOneField(
        User, verbose_name="Пользователь", related_name="cart", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return sum(item.price for item in self.items.all())

    @property
    def total_items(self):
        return self.items.count()


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, verbose_name="Корзина", related_name="items", on_delete=models.CASCADE
    )
    product_info = models.ForeignKey(
        ProductInfo,
        verbose_name="Информация о продукте",
        related_name="cart_items",
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField("Количество", default=1)

    @property
    def price(self):
        return self.product_info.price * self.quantity
