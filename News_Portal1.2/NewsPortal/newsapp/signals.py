from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
from NewsPortal import settings
# from django.conf import settings
from .models import Post, PostCategory
from .tasks import send_notifications


# def send_notifications(preview, pk, title, subscribers):
#     html_content = render_to_string(
#         'post_created_email.html',
#         {
#             'text': preview,
#             'link': f'{settings.SITE_URL}/news/{pk}'
#         }
#     )
#
#     msg = EmailMultiAlternatives(
#         subject=title,
#         body='',
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         to=subscribers
#     )
#
#     msg.attach_alternative(html_content, 'text/html')
#     msg.send()


# Используем m2m_changed, т.к. PostCategory имеет связь m2m, из-за этого список не сформируется и будет пустым,
# потому что объекты для связи m2m создаются позже чем объект основной модели, так устроен алгоритм создания и
# сохранения объектов в БД
@receiver(m2m_changed, sender=PostCategory)
def notify_post_created(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.postCategory.all()
        subscribers = []

        for category in categories:
            subscribers += category.subscribers.all()
            subscribers = [s.email for s in subscribers]

        send_notifications.delay(
            instance.preview(), instance.pk, instance.title, subscribers,
        )


# @receiver(post_save, sender=Post)
# def post_created(instance, created, **kwargs):
#     if not created:
#         return
#
#     emails = User.objects.filter(
#         subscriptions__category=instance.category
#     ).values_list('email', flat=True)
#
#     subject = f'Новая статья в категории {instance.category}'
#
#     text_content = (
#         f'Новая публикация: {instance.title}\n'
#         f'Краткое содержание: {instance.text}\n\n'
#         f'Ссылка на статью: http://127.0.0.1{instance.get_absolute_url()}'
#     )
#     html_content = (
#         f'Новая публикация: {instance.title}<br>'
#         f'Краткое содержание: {instance.text}<br><br>'
#         f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
#         f'Ссылка на статью</a>'
#     )
#     for email in emails:
#         msg = EmailMultiAlternatives(subject, text_content, None, [email])
#         msg.attach_alternative(html_content, "text/html")
#         msg.send()


# @receiver(post_save, sender=Post)
# def post_created(instance, **kwargs):
#     print('Пост создан', instance)