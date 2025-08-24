import yaml
import requests
from django.db import transaction
from .models import Shop, Category, Product, ProductInfo, Parameter, ProductParameter

def parse_yaml_data(data, supplier_user):
    with transaction.atomic():
        shop, _ = Shop.objects.get_or_create(name=data['shop'], user=supplier_user)
        for cat in data.get('categories', []):
            category, _ = Category.objects.get_or_create(id=cat['id'], defaults={'name': cat['name']})
            category.shops.add(shop)
        ProductInfo.objects.filter(shop=shop).delete()
        for item in data.get('goods', []):
            product, _ = Product.objects.get_or_create(name=item['name'], category_id=item['category'])
            info = ProductInfo.objects.create(
                product=product, shop=shop, external_id=item['id'],
                model=item['model'], price=item['price'], price_rrc=item['price_rrc'],
                quantity=item['quantity']
            )
            for param_name, param_value in item.get('parameters', {}).items():
                param, _ = Parameter.objects.get_or_create(name=param_name)
                ProductParameter.objects.create(product_info=info, parameter=param, value=str(param_value))

def import_products_from_yaml(yaml_url, supplier_user):
    try:
        response = requests.get(yaml_url, timeout=10)
        response.raise_for_status()
        data = yaml.safe_load(response.content)
        parse_yaml_data(data, supplier_user)
        return True, "Импорт успешен"
    except Exception as e:
        return False, f"Ошибка: {str(e)}"
