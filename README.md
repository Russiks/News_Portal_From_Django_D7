# News_Portal_From_Django_D7
 SkillFactoryStudy


Запуск приложения осуществлеестя через python3 manage.py runserver
Предварительно надо надо войти в виртуальное окружения через source venv/bin/activate, а затем пройти в папку проекта через cd
В веб-приложение можно создавать публикации, осуществялть регистрацию через сторонние сервисы и напрямую, подписываться на на категории публикаций
Рассылки подписчикам осуществляются черз таски 
Для запуска рассылок нужно выполнить сл команды 

redis-cli ping 

celery -A NewsPortal worker -l INFO 

celery -A NewsPortal beat -l INFO