from django import forms
from .models import Categories, Card, Tag
from django.core.exceptions import ValidationError
import re


class CardForm(forms.ModelForm):
    # Теперь мы можем определить только те поля, которые нам нужно кастомизировать
    category = forms.ModelChoiceField(queryset=Categories.objects.all(), empty_label="Категория не выбрана",
                                      label='Категория', widget=forms.Select(attrs={'class': 'form-control'}))
    tags = forms.CharField(label='Теги', required=False, help_text='Перечислите теги через запятую',
                           widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Card  # Указываем модель, с которой работает форма
        # Указываем, какие поля должны присутствовать в форме и в каком порядке
        fields = ['question', 'answer', 'category', 'tags']
        # Указываем виджеты для полей
        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control'}),
            'answer': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 40}),
        }
        # Указываем метки для полей
        labels = {
            'question': 'Вопрос',
            'answer': 'Ответ',
            'category': 'Категория',
            'tags': 'Теги'
        }

    def clean_tags(self):
        # Валидация и преобразование строки тегов в список тегов
        tags_str = self.cleaned_data['tags']
        tag_list = [tag.strip() for tag in tags_str.split(',') if tag.strip()]
        return tag_list

    def save(self, *args, **kwargs):
        # Сохранение карточки вместе с тегами
        instance = super().save(commit=False)
        instance.save()  # Сначала сохраняем карточку, чтобы получить ее id

        # Обрабатываем теги
        for tag_name in self.cleaned_data['tags']:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            instance.tags.add(tag)

        return instance


class SearchForm(forms.Form):
    query = forms.CharField()
