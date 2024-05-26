from django.contrib import admin
from .models import Card
from django.contrib.admin import SimpleListFilter


class CardCodeFilter(SimpleListFilter):
    title = 'Cтатус проверки'
    parameter_name = 'status_check'

    def lookups(self, request, model_admin):
        return (
            ('check', 'Проверено'),
            ('not check', 'Не проверено'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'check':
            return queryset.filter(answer__contains='Проверено')
        elif self.value() == 'not check':
            return queryset.exclude(answer__contains='Не проверено')


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):

    list_display = ('id', 'question', 'category', 'views', 'check_status', 'upload_date')

    list_display_links = ('id',)

    list_filter = ('category', 'upload_date', CardCodeFilter)

    list_editable = ('views', 'question', 'check_status')

    list_per_page = 10

    actions = ['make_checked', 'make_unchecked']

    @admin.action(description='Отметить выбранные карточки как проверенные')
    def make_checked(self, request, queryset):
        updated_count = queryset.update(check_status=True)
        self.message_user(request, f"{updated_count} записей было помечено как проверенное")

    @admin.action(description='Отметить выбранные карточки как непроверенные')
    def make_unchecked(self, request, queryset):
        updated_count = queryset.update(check_status=False)
        self.message_user(request, f"{updated_count} записей было помечено как непроверенные")