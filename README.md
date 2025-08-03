<h1 id="readme-top">Название проекта</h1>

# Дипломный проект: Backend для автоматизации закупок (Python/Django)

## Основные характеристики проекта
- **Цель**: Разработка backend-сервиса для автоматизации закупок в розничных сетях
- **Технологии**: Django REST Framework, Celery, Docker, PostgreSQL
- **Тип проекта**: Курсовая работа для профессии "Python-разработчик"

## Ключевые требования
**Обязательная часть**:
- Реализация REST API для клиентов и поставщиков
- Система управления товарами с характеристиками
- Импорт товаров из YAML-файлов
- Email-уведомления (подтверждение заказов)
- Документация API

**Дополнительно (по желанию)**:
- Админ-панель для управления заказами
- Асинхронная обработка через Celery
- Docker-контейнеризация
- Экспорт товаров

## Этапы разработки
1. **Базовая реализация**:
   - Настройка Django-проекта
   - Проектирование моделей данных
   - Импорт товаров
   - Реализация API endpoints

2. **Продвинутые функции**:
   - Админка склада
   - Асинхронные задачи
   - Docker-развертывание

## Технические требования
- Python 3.10+
- Django 4.2+
- DRF 3.14+
- Поддержка Linux/MacOS (не рекомендуется Windows)

## Критерии оценки
- Работоспособность всех обязательных функций
- Наличие документации
- Использование Git с регулярными коммитами
- Чистота и комментированность кода

**Срок сдачи**: Согласно графику курса  
**Формат сдачи**: GitHub-репозиторий с полной историей разработки

<p align="right">(<a href="#readme-top">Вернуться к началу</a>)</p>

# ПО

    Python 3.13
    Git
    Docker + Docker Compose
    IDE: VS Code
    AI-инструмент: Codeium




# Этап 1: Создание и настройка проекта
## Цель
  Создать рабочее окружение и инициализировать Django-проект.
### 1. Fork репозитория

Структура впроекта "the path of least resistance"
```
reference/
├── backend/
│   ├── __init__.py
│   ├── admin.py            
│   ├── apps.py
│   ├── models.py           
│   ├── serializers.py      
│   ├── views.py            
│   ├── urls.py             
│   ├── signals.py          
│   └── tests.py            
│
├── migrations/
│   ├── 0001_initial.py
│   ├── __init__.py
│   └── __pycache__/
│       ├── 0001_initial.cpython-310.pyc
│       └── __init__.cpython-310.pyc
│
│
│
├── manage.py               
├── netology_pd_diplom/    
│   ├── settings.py         
│   ├── urls.py             
│   └── wsgi.py
│   
│
├── requirements.txt       
└── .gitignore
```
            
### 2. Клонируйть репозиторий
```
git clone https://github.com/ВАШ_ЛОГИН/netology_pd_diplom.git
cd netology_pd_diplom
```
### 3. Создайть виртуальное окружение
```
python -m venv env
source env/bin/activate
```
### 4. Установить зависимости
```
pip install Django djangorestframework PyYAML requests python-decouple drf-yasg celery redis
```
### 5. Создайте Django-проект и приложение
```
django-admin startproject procurement_backend .
python manage.py startapp procurement
```

### 6. Запуск
```
python manage.py runserver
```
http://127.0.0.1:8000/admin


# Этап 2: Проработка моделей данных
## Создать модели: пользователи, товары, заказы, поставщики.
На втором этапе "Проработка моделей данных" была выполнена следующая работа: 

  Были созданы и настроены все основные модели Django, соответствующие бизнес-логике системы автоматизации закупок. Основные действия включали: 

  1. Создание моделей: 
  2. Настройка связей и ограничений: 
  3. Добавление дополнительных методов и мета-настроек: 
         
  Итог: На втором этапе была полностью реализована объектно-реляционная модель данных, которая позволяет системе работать с товарами от нескольких поставщиков, хранить настраиваемые характеристики товаров и управлять заказами пользователей. 

Обновлены файлы 
    procurement/models.py
    procurement_backend/settings.py (регистрация приложения) 
    
# Этап 3: Реализация импорта товаров
## Цель
  Импорт товаров из YAML-файла по URL.

### 1. Создан парсер
    procurement/utils/import_parser.py
### 2. Создайте view 
    procurement/views/suppliers.py
### 3. Подключен URL
    procurement/urls.py
### 4. Включн в основной urls.py

# Этап 4: Реализация API Views
## Цель
  Реализовать все API-эндпоинты.
### 1. Авторизация 
    procurement/views/auth.py
### 2. Корзина 
    procurement/views/cart.py
### 3. Заказы
    procurement/views/orders.py
### 4. Подключен в urls.py

# Этап 5: Полностью готовый backend
  - сценарий: регистрация → вход → корзина → заказ → email.
### Действия
  - Запустите сервер: 
```
    python manage.py runserver
```
### Через Postman:
    - Зарегистрировоться
    - Войти
    - Добавить товар в корзину
    - Оформить заказ
    - Проверьть email
### Проверить что все работает.  

# Этап 6: Админка заказов 
# Этап 7: Асинхронные задачи
# Этап 8: Docker-развёртывание

<p align="right">(<a href="#readme-top">Вернуться к началу</a>)</p>

Итоговая структура после выполнения 8 этапов "the path of least resistance"
```
backend/
├── __init__.py
├── admin.py
├── apps.py
├── models.py
├── serializers.py
├── views/
│   ├── __init__.py
│   ├── auth.py            # Регистрация и авторизация
│   ├── cart.py            # Работа с корзиной
│   ├── orders.py          # Управление заказами
│   ├── suppliers.py       # API для поставщиков
│   └── admin_views.py     # Админские функции
├── urls.py
├── tasks.py               # Celery-задачи
├── utils/
│   ├── __init__.py
│   ├── import_parser.py   # Парсер YAML
│   └── notifications.py   # Отправка уведомлений
├── migrations/
│   ├── __init__.py
│   └── 0001_initial.py
│   
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_views.py
│   └── test_utils.py
├── signals.py             # Сигналы Django
├── templates/
│   └── emails/
│       ├── order_created.html
│       └── status_changed.html
└── management/
    ├── __init__.py
    └── commands/
        ├── __init__.py
        └── import_products.py  # Кастомная команда
                       
```

<p align="right">(<a href="#readme-top">Вернуться к началу</a>)</p>
