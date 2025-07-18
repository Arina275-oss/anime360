import os
import django
import traceback

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'anime360.settings')

try:
    django.setup()
    print("✅ Django успешно инициализирован!")
    from django.apps import apps
    print("Приложения:", [app.name for app in apps.get_app_configs()])
except Exception as e:
    print("❌ Ошибка инициализации:")
    traceback.print_exc()