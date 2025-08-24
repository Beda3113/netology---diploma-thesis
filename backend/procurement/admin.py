from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http import JsonResponse
from procurement.models import (
    User,
    Shop,
    Category,
    Product,
    ProductInfo,
    Parameter,
    ProductParameter,
    Order,
    OrderItem,
    Contact,
    ConfirmEmailToken,
)


@admin.action(description="Экспорт выбранных товаров в JSON")
def export_products_json(modeladmin, request, queryset):
    """
    Экспорт товаров (ProductInfo) в формате JSON.
    Включает название товара, категорию, магазин, цену, количество и параметры.
    """
    data = []
    for product_info in queryset:
        # Собираем параметры как словарь "параметр: значение"
        parameters = {
            pp.parameter.name: pp.value for pp in product_info.product_parameters.all()
        }
        data.append(
            {
                "product": product_info.product.name,
                "category": product_info.product.category.name,
                "shop": product_info.shop.name,
                "price": product_info.price,
                "quantity": product_info.quantity,
                "parameters": parameters,
            }
        )
    return JsonResponse(
        data, safe=False, json_dumps_params={"ensure_ascii": False, "indent": 2}
    )


@admin.register(ProductInfo)
class ProductInfoAdmin(admin.ModelAdmin):
    """
    Админ-панель для информации о товарах.
    Поддерживает экспорт в JSON через действие.
    """

    list_display = ("product", "shop", "price", "quantity", "external_id")
    list_filter = ("shop", "product__category")
    search_fields = ("product__name", "model", "external_id")
    actions = [export_products_json]


# === Остальные модели ===


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Кастомная админ-панель для пользователя.
    Использует email как основной идентификатор.
    """

    model = User
    fieldsets = (
        (None, {"fields": ("email", "password", "type")}),
        (
            "Personal info",
            {"fields": ("first_name", "last_name", "company", "position")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "type"),
            },
        ),
    )
    list_display = ("email", "first_name", "last_name", "type", "is_staff", "is_active")
    list_filter = ("type", "is_staff", "is_superuser", "is_active")
    search_fields = ("email", "first_name", "last_name", "company")
    ordering = ("email",)


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "state")
    list_filter = ("state",)
    search_fields = ("name",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category")
    list_filter = ("category",)
    search_fields = ("name",)


@admin.register(Parameter)
class ParameterAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(ProductParameter)
class ProductParameterAdmin(admin.ModelAdmin):
    list_display = ("product_info", "parameter", "value")
    list_filter = ("parameter",)
    search_fields = ("value",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "dt", "state")
    list_filter = ("state", "dt")
    search_fields = ("user__email", "id")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product_info", "quantity")
    list_filter = ("order",)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("user", "city", "phone")
    search_fields = ("user__email", "city", "phone")


@admin.register(ConfirmEmailToken)
class ConfirmEmailTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "key", "created_at")
    readonly_fields = ("key", "created_at")
