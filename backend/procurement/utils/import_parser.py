import yaml
from django.db import transaction
from ..models import (
    Shop,
    Category,
    Product,
    ProductInfo,
    Parameter,
    ProductParameter
)

def parse_yaml_data(yaml_data, supplier_user):
    """
    Основной метод парсинга YAML-данных
    Пример входных данных: см. shop1.yaml
    """
    with transaction.atomic():  # Все операции в одной транзакции
        shop, _ = Shop.objects.get_or_create(
            name=yaml_data['shop'],
            user=supplier_user
        )
        
        # Обработка категорий
        for category_data in yaml_data.get('categories', []):
            category, _ = Category.objects.get_or_create(
                id=category_data['id'],
                defaults={'name': category_data['name']}
            )
            category.shops.add(shop)
        
        # Удаляем старые данные перед импортом
        ProductInfo.objects.filter(shop=shop).delete()
        
        # Обработка товаров
        for product_data in yaml_data.get('goods', []):
            product, _ = Product.objects.get_or_create(
                name=product_data['name'],
                category_id=product_data['category']
            )
            
            product_info = ProductInfo.objects.create(
                product=product,
                external_id=product_data['id'],
                model=product_data['model'],
                price=product_data['price'],
                price_rrc=product_data['price_rrc'],
                quantity=product_data['quantity'],
                shop=shop
            )
            
            # Обработка параметров товара
            for param_name, param_value in product_data.get('parameters', {}).items():
                parameter, _ = Parameter.objects.get_or_create(name=param_name)
                ProductParameter.objects.create(
                    product_info=product_info,
                    parameter=parameter,
                    value=str(param_value)
                )

def import_products_from_yaml(yaml_url, supplier_user):
    """
    Импорт товаров из YAML по URL
    """
    import requests
    from yaml import Loader
    
    try:
        response = requests.get(yaml_url, timeout=10)
        response.raise_for_status()
        data = yaml.load(response.content, Loader=Loader)
        parse_yaml_data(data, supplier_user)
        return True, "Импорт успешно завершен"
    except Exception as e:
        return False, f"Ошибка импорта: {str(e)}"
