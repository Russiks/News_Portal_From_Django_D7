"""
В данном файле прописывается логика приложения.
Суть представления (views) в Django - это запрос инициализации из модели в файле models и
передача ее в шаблон (templates).
После создания представлений, нужно указать адреса, по которым будут доступны представления.
Для настройки адресов используется файл "urls.py" но не тот, который лежит в проекте, а тот
что нужно создать в приложении и указать на него ссылкой из основного файла.
"""
from django.contrib.auth.decorators import login_required
from django.db.models import (
    Exists, OuterRef,
)
from django.shortcuts import render
from datetime import datetime

from django.views.decorators.csrf import csrf_protect
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin
)
from .models import (
    Post, Category, Subscription,
)
from .filters import PostFilter
from .forms import PostForm


# Класс-представление для отображения списка постов. Унаследован от базового представления"ListView"
class PostList(ListView):
    model = Post  # Указываем имя модели, которая будет использоваться для отображения и реализации логики
    template_name = 'flatpages/news.html'  # Указываем имя шаблона, то есть html файла, который будет использоваться
    # для визуализации
    context_object_name = 'news'  # Имя, которое будет использоваться для передачи переменных в шаблон
    queryset = Post.objects.order_by('-dateCreation')
    # ordering = ['-id']  # Задаем последовательность отображения по id
    paginate_by = 2  # Задаем кол-во отображаемых объектов на странице

    # -----------------------------------------------------------------------------------------------
    # Вот так мы можем использовать дженерик ListView для вывода списка постов:
    #
    # Создаем свой класс, который наследуется от ListView.
    # Указываем модель, из которой будем выводить данные.
    # Указываем поле сортировки данных модели (необязательно).
    # Записываем название шаблона.
    # Объявляем, как хотим назвать переменную в шаблоне.
    # -----------------------------------------------------------------------------------------------

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        queryset = super().get_queryset()  # Получаем обычный запрос
        self.filterset = PostFilter(self.request.GET, queryset)  # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict. Сохраняем нашу фильтрацию в объекте класса, чтобы потом
        # добавить в контекст и использовать в шаблоне.
        return self.filterset.qs  # Возвращаем из функции отфильтрованный список товаров

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # С помощью super() мы обращаемся к родительским классам и
        # вызываем у них метод get_context_data с теми же аргументами, что и были переданы нам. В ответе мы должны
        # получить словарь.
        context['time_now'] = datetime.utcnow()  # К словарю добавим текущую дату в ключ 'time_now'.
        # добавим ещё одну пустую переменную, чтобы на её примере посмотреть работу другого фильтра
        context['next_sale'] = 'Выберите статью по категории!'
        context['filterset'] = self.filterset  # Добавляем в контекст объект фильтрации
        return context


# Класс-представление для отображения деталей объекта (публикации)
class PostDetail(DetailView):
    model = Post
    template_name = 'flatpages/post.html'
    context_object_name = 'post'


# Класс-представление, созданное для поиска объектов по фильтрам
class PostSearch(PostList):
    model = Post
    template_name = 'flatpages/search.html'
    context_object_name = 'posts_search'
    filter_class = PostFilter
    ordering = ['dateCreation']

    # def get_filter(self):
    #     return PostFilter(self.request.GET, queryset=super().get_queryset())
    #
    # def get_queryset(self):
    #     return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):  # Метод get_context_data нужен нам для того, чтобы мы могли
        # передать переменные в шаблон. В возвращаемом словаре context будут храниться все переменные. Ключи этого
        # словаря и есть переменные, к которым мы сможем потом обратиться через шаблон
        context = super().get_context_data(*args, **kwargs)
        context['filter'] = PostFilter(
            self.request.GET, queryset=self.get_queryset())  # Вписываем фильтр в контекст
        return context


# CreateView представление для создания товаров.
class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    # raise_exception = True
    form_class = PostForm  # Указываем нашу разработанную форму,
    model = Post  # модель публикации
    template_name = 'flatpages/post_create.html'  # и новый шаблон, в котором используется форма.
    permission_required = 'newsapp.add_post'  # Даем разрешения на создание публикации

    def form_valid(self, form):  # Этот метод вызывается, когда действительные данные формы получены в POSTed. Он
        # должен возвращать HttpResponse.
        post = form.save(commit=False)  # Этот метод save() принимает необязательный аргумент ключевого слова commit,
        # который принимает значение True или False. Если вы вызовете метод save() с commit=False, то он вернет
        # объект, который еще не был сохранен в базе данных. В этом случае вы сами должны вызвать save() для
        # полученного экземпляра модели. Это полезно, если вы хотите выполнить пользовательскую обработку объекта
        # перед его сохранением, или если вы хотите использовать один из специализированных вариантов сохранения
        # модели. По умолчанию commit имеет значение True.
        post.categoryType = 'AR'  # Тип созданной категории

        return super().form_valid(form)


# CreateView представление для создания публикации.
class NewsCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm  # Указываем нашу разработанную форму,
    model = Post  # модель публикации
    template_name = 'flatpages/news_create.html'  # и новый шаблон, в котором используется форма.
    permission_required = 'newsapp.add_post'  # Даем разрешения на создание публикации

    def form_valid(self, form):  # Этот метод вызывается, когда действительные данные формы получены в POSTed. Он
        # должен возвращать HttpResponse.
        post = form.save(commit=False)
        post.categoryType = 'NW'

        return super().form_valid(form)


# UpdateView представление для редактирования публикации.
class PostUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm  # form_class нужен, чтобы получать доступ к форме через метод POST
    template_name = 'flatpages/post_edit.html'
    model = Post
    permission_required = 'newsapp.change_post'  # Даем разрешения на создание публикации

    def get_object(self, **kwargs):  # метод get_object мы используем вместо queryset, чтобы получить информацию об
        # объекте, который мы собираемся редактировать
        id = self.kwargs.get('pk')  # Запрашиваем первичный ключ
        return Post.objects.get(pk=id)  # Возвращаем объект по запрошенному id


# UpdateView представление для редактирования публикации.
class NewsUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm  # form_class нужен, чтобы получать доступ к форме через метод POST
    template_name = 'flatpages/news_edit.html'
    model = Post
    permission_required = 'newsapp.change_post'  # Даем разрешения на создание публикации

    def get_object(self, **kwargs):  # метод get_object мы используем вместо queryset, чтобы получить информацию об
        # объекте, который мы собираемся редактировать
        id = self.kwargs.get('pk')  # Запрашиваем первичный ключ
        return Post.objects.get(pk=id)  # Возвращаем объект по запрошенному id


# DeleteView представление для удаления публикации.
class PostDelete(PermissionRequiredMixin, DeleteView):
    template_name = 'flatpages/post_delete.html'
    # queryset = Post.objects.all()
    success_url = '/post/'
    permission_required = 'newsapp.delete_post'  # Даем разрешения на создание публикации

    def get_object(self, **kwargs):  # метод get_object мы используем вместо queryset, чтобы получить информацию об
        # объекте, который мы собираемся редактировать
        id = self.kwargs.get('pk')  # Запрашиваем первичный ключ
        return Post.objects.get(pk=id)  # Возвращаем объект по запрошенному id


# DeleteView представление для удаления публикации.
class NewsDelete(PermissionRequiredMixin, DeleteView):
    template_name = 'flatpages/news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    permission_required = 'newsapp.delete_post'  # Даем разрешения на создание публикации


@login_required  # Декоратор login_required дает возможность подписаться только зарегистрированным пользователям
@csrf_protect  # Декоратор csrf_protect автоматически проверяет CSRF-токен в получаемых формах
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )
#–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
# В представлении мы можем принять как GET, так и POST-запросы:
#
# GET — будут выполняться, когда пользователь просто открывает страницу подписок;
# POST — когда пользователь нажмёт
# кнопку подписки или отписки от категории
# Далее по коду мы делаем непростой запрос в базу данных. Мы соберём все категории товаров с сортировкой по алфавиту и
# добавим специальное поле, которое покажет, подписан сейчас пользователь на данную категорию или нет
# –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

# Create your views here.