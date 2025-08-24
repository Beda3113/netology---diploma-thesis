from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from procurement.utils.import_parser import import_products_from_yaml
import os

User = get_user_model()


class Command(BaseCommand):
    help = "Импорт товаров из YAML файла для указанного поставщика"

    def add_arguments(self, parser):
        parser.add_argument(
            "--supplier-id", type=int, required=True, help="ID пользователя-поставщика"
        )
        parser.add_argument("--file", type=str, help="Путь к локальному YAML файлу")
        parser.add_argument("--url", type=str, help="URL YAML файла")

    def handle(self, *args, **options):
        supplier_id = options["supplier_id"]
        file_path = options.get("file")
        yaml_url = options.get("url")

        try:
            supplier = User.objects.get(id=supplier_id, role="supplier")
        except User.DoesNotExist:
            self.stderr.write(
                self.style.ERROR(
                    f"Пользователь с ID {supplier_id} не найден или не является поставщиком"
                )
            )
            return

        # Проверка источника данных
        if not (file_path or yaml_url):
            self.stderr.write(self.style.ERROR("Необходимо указать --file или --url"))
            return

        if file_path and yaml_url:
            self.stderr.write(
                self.style.ERROR(
                    "Укажите только один источник данных (--file ИЛИ --url)"
                )
            )
            return

        try:
            if file_path:
                # Обработка локального файла
                if not os.path.exists(file_path):
                    raise FileNotFoundError(f"Файл {file_path} не существует")

                with open(file_path, "r", encoding="utf-8") as f:
                    import yaml

                    data = yaml.safe_load(f)
                    from procurement.utils.import_parser import parse_yaml_data

                    parse_yaml_data(data, supplier)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"Успешно импортировано из файла {file_path}"
                        )
                    )
            else:
                # Обработка URL
                success, message = import_products_from_yaml(yaml_url, supplier)
                if success:
                    self.stdout.write(self.style.SUCCESS(message))
                else:
                    self.stderr.write(self.style.ERROR(message))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Ошибка импорта: {str(e)}"))
