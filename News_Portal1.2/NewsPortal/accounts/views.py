from django.shortcuts import render
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
# from .forms import SignUpForm


class SignUp(CreateView):
    model = User  # Модель формы, которую реализует данный generic
    # form_class = SignUpForm  # Форма, которая будет заполняться пользователем
    success_url = '/accounts/login'  # URL, на который нужно направить пользователя после успешного ввода данных в форму

    template_name = 'registration/signup.html'
# Create your views here.
