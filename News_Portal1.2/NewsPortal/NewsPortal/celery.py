import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal.settings')  # Связываем настройки Django с настройками
# Celery через переменную окружения

app = Celery('NewsPortal')  # Создаем экземпляр приложения Celery и устанавливаем для него файл конфигурации
app.config_from_object('django.conf:settings', namespace='CELERY')  # Указываем пространство имен, чтобы Celery сам
# находил все необходимые настройки в файле settings.py. Он их будет искать по шаблону: "CELERY_***"

app.autodiscover_tasks()  # Указываем Celery автоматически искать задания в файлах "tasks.py" каждого приложения проекта

app.conf.beat_schedule = {
    'weekly_subscribe': {
        'task': 'newsapp.tasks.my_job',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}