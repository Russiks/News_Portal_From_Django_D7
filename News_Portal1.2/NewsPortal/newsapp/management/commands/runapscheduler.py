# import datetime
# import logging
#
# from apscheduler.schedulers.blocking import BlockingScheduler
# from apscheduler.triggers.cron import CronTrigger
# # from django.conf import settings
# from NewsPortal import settings
# from django.core.mail import EmailMultiAlternatives
# from django.core.management.base import BaseCommand
# from django.template.loader import render_to_string
# from django_apscheduler import util
# from django_apscheduler.jobstores import DjangoJobStore
# from django_apscheduler.models import DjangoJobExecution
# from newsapp.models import Post, Category
#
# logger = logging.getLogger(__name__)
#
#
# def my_job():
#     today = datetime.datetime.now()  # Определяем текущий день запуска триггера для фильтрации статей по дате создания
#     last_week = today - datetime.timedelta(days=7)  # Время начала отчета (неделя назад от сегодняшнего дня)
#     posts = Post.objects.filter(dateCreation__gte=last_week)  # Фильтруем категории по дате создания (gte - больше
#     # либо равно)
#     categories = set(posts.values_list('postCategory__name', flat=True))  # Получаем категории статей
#     subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))  #
#     # Получаем подписчиков на категории
#
#     html_content = render_to_string(
#         'daily_post.html',
#         {
#             'link': settings.SITE_URL,
#             'posts': posts
#         }
#     )
#
#     msg = EmailMultiAlternatives(
#         subject='Публикации за прошедшую неделю!',
#         body='',
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         to=subscribers
#     )
#
#     msg.attach_alternative(html_content, 'text/html')
#     msg.send()
#
#
# # Декоратор `close_old_connections` гарантирует, что соединения с базой данных, которые стали непригодными для
# # использования или устарели, закрываются до и после выполнения вашего задания. Вы должны использовать его для
# # обертывания всех запланированных вами заданий, которые каким-либо образом обращаются к базе данных Django.
# @util.close_old_connections
# def delete_old_job_executions(max_age=604_800):
#     """
#     Это задание удаляет записи о выполнении заданий APScheduler старше `max_age` из базы данных. Это помогает
#     предотвратить заполнение базы данных старыми историческими записями, которые больше не нужны.
#     :param max_age: Максимальный период времени, в течение которого следует хранить исторические
#                     записи о выполнении задания. По умолчанию 7 дней.
#     """
#     DjangoJobExecution.objects.delete_old_job_executions(max_age)
#
#
# class Command(BaseCommand):
#     help = "Runs APScheduler."
#
#     def handle(self, *args, **options):
#         scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
#         scheduler.add_jobstore(DjangoJobStore(), "default")
#
#         scheduler.add_job(  # Расписание задачи
#             my_job,
#             # trigger=CronTrigger(second="*/10"),  # Каждые 10 секунд
#             trigger=CronTrigger(day_of_week="fri", hour="18", minute="00"),  # Каждую пятницу в 18:00
#             id="my_job",  # Идентификатор, присвоенный каждому заданию, должен быть уникальным
#             max_instances=1,
#             replace_existing=True,
#         )
#         logger.info("Added job 'my_job'.")  # Добавление в работу
#
#         scheduler.add_job(
#             delete_old_job_executions,
#             trigger=CronTrigger(
#                 day_of_week="mon", hour="00", minute="00"
#             ),
#             id="delete_old_job_executions",  # Удаляем старые выполнения заданий
#             max_instances=1,
#             replace_existing=True,
#         )
#         logger.info("Added weekly job: 'delete_old_job_executions'.")  # Еженедельное выполнение задания
#
#         try:
#             logger.info("Starting scheduler...")  # Запуск планировщика
#             scheduler.start()
#         except KeyboardInterrupt:
#             logger.info("Stopping scheduler...")  # Остановка планировщика
#             scheduler.shutdown()
#             logger.info("Scheduler shut down successfully!")  # Успешное завершение работы планировщика
#
#
#
