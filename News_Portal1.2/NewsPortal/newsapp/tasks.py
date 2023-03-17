import datetime

from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
from NewsPortal import settings
from .models import PostCategory, Post, Category


@shared_task()
def send_notifications(preview, pk, title, subscribers):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task()
def my_job():
    today = datetime.datetime.now()  # Определяем текущий день запуска триггера для фильтрации статей по дате создания
    last_week = today - datetime.timedelta(days=7)  # Время начала отчета (неделя назад от сегодняшнего дня)
    posts = Post.objects.filter(dateCreation__gte=last_week)  # Фильтруем категории по дате создания (gte - больше
    # либо равно)
    categories = set(posts.values_list('postCategory__name', flat=True))  # Получаем категории статей
    subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))  #
    # Получаем подписчиков на категории

    html_content = render_to_string(
        'daily_post.html',
        {
            'link': settings.SITE_URL,
            'posts': posts
        }
    )

    msg = EmailMultiAlternatives(
        subject='Публикации за прошедшую неделю!',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()