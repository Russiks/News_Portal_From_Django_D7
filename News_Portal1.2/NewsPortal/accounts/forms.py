from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm  # Базовая форма, позволяющая создать пользователя (в ней реализованы
# все валидации и проверки)
from django.contrib.auth.models import Group
from django.core.mail import (
    send_mail, EmailMultiAlternatives, mail_admins,
)


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)  # Вызываем метод класса-родителя, чтобы были выполнены необходимые проверки и
        # сохранение в модель User
        normal_users = Group.objects.get(name='normal users')  # Получаем объект модели группы normal users
        # normal_users.user_set.add(user)  # через атрибут user_set, возвращающий список всех пользователей этой группы
        # и добавляем нового пользователя в эту группу
        user.groups.add(normal_users)  # Добавляем нового пользователя в эту группу

        # send_mail(
        #     subject='Добро пожаловать в наш интернет-портал!',  # Голова сообщения
        #     message=f'{user.username}, вы успешно зарегистрировались!',  # Тело сообщения
        #     from_email=None,  # будет использовано значение DEFAULT_FROM_EMAIL
        #     recipient_list=[user.email],  # Список получателей
        # )

        subject = 'Добро пожаловать в наш интернет-портал!'  # Голова сообщения
        text = f'{user.username}, вы успешно зарегистрировались на сайте!'  # Тело сообщения
        html = (  # html-тело сообщения
            f'<b>{user.username}</b>, вы успешно зарегистрировались на '
            f'<a href="http://127.0.0.1:8000/about">сайте</a>!'
        )
        msg = EmailMultiAlternatives(  # В инициализатор класса EmailMultiAlternatives мы передаём текстовую версию
            subject=subject, body=text, from_email=None, to=[user.email]
        )
        # --------------------------------------------------------------------------------------------------------------
        # Если писать длинные сообщения с большим количеством разметки, то лучше вынести код в HTML-файл и с помощью
        # функции render_to_string создать переменную с HTML-кодом. И уже эту переменную передать в
        # attach_alternative. То есть, по сути, разработать шаблон не для выдачи в браузере, а для составления письма.
        # --------------------------------------------------------------------------------------------------------------
        msg.attach_alternative(html, "text/html")  # html прикрепляем как альтернативный вариант письма
        msg.send()  # Отправляем письмо

        mail_admins(
            subject=' Новый пользователь!',
            message=f'Пользователь {user.username} зарегистрировался на сайте.'
        )

        return user  # Обязательным требованием метода save() является возвращение объекта модели User по итогу
        # выполнения функции


# class SignUpForm(UserCreationForm):
#     # Стандартные поля формы Module 5
#     email = forms.EmailField(label="Email")
#     first_name = forms.CharField(label="Имя")
#     last_name = forms.CharField(label="Фамилия")
#
#     # Расширение стандартных форм
#     class Meta:
#         model = User
#         fields = (
#             "username",
#             "first_name",
#             "last_name",
#             "email",
#             "password1",
#             "password2",
#         )