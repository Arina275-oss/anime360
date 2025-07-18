import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'anime360.settings')
django.setup()

from django.apps import apps

print("Загруженные приложения:")
for app in apps.get_app_configs():
    print(f"- {app.name}")

print("\nКонфиг cart:", apps.get_app_config('cart'))