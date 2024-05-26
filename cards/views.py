from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import SearchVector
from django.core.cache import cache
from django.db.models import Q, F
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from .models import Card, Tag
from .forms import CardForm, SearchForm
from django.views.generic import TemplateView, ListView, DetailView, CreateView

info = {
    "menu": [
        {"title": "Главная",
         "url": "/",
         "url_name": "index"},
        {"title": "О проекте",
         "url": "/about/",
         "url_name": "about"},
        {"title": "Каталог",
         "url": "/cards/catalog/",
         "url_name": "catalog"},
    ]}


class MenuMixin:

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(info)
        context['cards_count'] = self.get_cards_count()
        return context

    @staticmethod
    def get_cards_count():
        cards_count = cache.get('cards_count')
        if not cards_count:
            cards_count = Card.objects.count()
            cache.set('cards_count', cards_count)

        return cards_count


class IndexView(MenuMixin, TemplateView):
    """
    Класс для главной страницы
    """
    template_name = 'main.html'


class AboutView(MenuMixin, TemplateView):
    """
    Класс страницы "О проекте"
    """
    template_name = 'about.html'


class CatalogView(MenuMixin, ListView):
    """
    Класс для каталога карточек
    """
    model = Card  # Указываем модель, данные которой мы хотим отобразить
    template_name = 'cards/catalog.html'  # Путь к шаблону, который будет использоваться для отображения страницы
    context_object_name = 'cards'  # Имя переменной контекста, которую будем использовать в шаблоне
    paginate_by = 30  # Количество объектов на странице

    # Метод для модификации начального запроса к БД
    def get_queryset(self):
        # Получение параметров сортировки из GET-запроса
        sort = self.request.GET.get('sort', 'upload_date')
        order = self.request.GET.get('order', 'desc')
        search_query = self.request.GET.get('search_query', '')

        # Определение направления сортировки
        if order == 'asc':
            order_by = sort
        else:
            order_by = f'-{sort}'

        # Фильтрация карточек по поисковому запросу и сортировка
        if search_query:
            queryset = Card.objects.filter(
                Q(question__icontains=search_query) |
                Q(answer__icontains=search_query) |
                Q(tags__name__icontains=search_query)
            ).distinct().order_by(order_by)
        else:
            queryset = Card.objects.all().order_by(order_by)
        return queryset

    # Метод для добавления дополнительного контекста
    def get_context_data(self, **kwargs):
        # Получение существующего контекста из базового класса
        context = super().get_context_data(**kwargs)
        # Добавление дополнительных данных в контекст
        context['sort'] = self.request.GET.get('sort', 'upload_date')
        context['order'] = self.request.GET.get('order', 'desc')
        context['search_query'] = self.request.GET.get('search_query', '')
        context['cards_count'] = self.get_cards_count()
        return context

    @staticmethod
    def get_cards_count():
        cards_count = cache.get('cards_count')
        if not cards_count:
            cards_count = Card.objects.count()
            cache.set('cards_count', cards_count)

        return cards_count


class CardDetailView(MenuMixin, DetailView):
    """
    Класс для детального отображения карточек
    """
    model = Card  # Указываем, что моделью для этого представления является Card
    template_name = 'cards/card_detail.html'  # Указываем путь к шаблону для детального отображения карточки
    context_object_name = 'card'  # Переопределяем имя переменной в контексте шаблона на 'card'

    # Метод для добавления дополнительных данных в контекст шаблона
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # Получаем исходный контекст от базового класса
        context['menu'] = info['menu']  # Добавляем в контекст информацию о меню
        context['title'] = f'Карточка: {context["card"].question}'  # Добавляем заголовок страницы
        return context

    # Метод для обновления счетчика просмотров при каждом отображении детальной страницы карточки
    def get_object(self, queryset=None):
        # Получаем объект с учетом переданных в URL параметров (в данном случае, pk или id карточки)
        obj = super().get_object(queryset=queryset)
        # Увеличиваем счетчик просмотров на 1 с помощью F-выражения для избежания гонки условий
        Card.objects.filter(pk=obj.pk).update(views=F('views') + 1)
        return obj


def get_cards_by_tag(request, tag_id):
    """
    Возвращает карточки по тегу для представления в каталоге
    """
    # Добываем карточки из БД по тегу
    cards = Card.objects.filter(tags__id=tag_id)

    # Подготавливаем контекст и отображаем шаблон
    context = {
        'cards': cards,
        'menu': info['menu'],
    }

    return render(request, 'cards/catalog.html', context)


class AddCardCreateView(MenuMixin, LoginRequiredMixin, CreateView):
    """
    Класс для добавления карточек
    """
    model = Card  # Указываем модель, с которой работает представление
    form_class = CardForm  # Указываем класс формы для создания карточки
    template_name = 'cards/add_card.html'  # Указываем шаблон, который будет использоваться для отображения формы
    success_url = reverse_lazy('catalog')  # URL для перенаправления после успешного создания карточки
    login_url = '/users/login/'
    redirect_field_name = 'next'

    def form_valid(self, form):
        # Метод вызывается, если форма валидна
        # Здесь можно добавить дополнительную логику обработки данных формы перед сохранением объекта
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # Метод для добавления дополнительных данных в контекст шаблона
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст информацию о меню, предполагая, что 'info' доступен в контексте
        context['menu'] = info['menu']
        return context


def add_card(request):
    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            card = form.save()
            return redirect(card.get_absolute_url())
    else:
        form = CardForm()

    return render(request, 'cards/add_card.html', {'form': form})
