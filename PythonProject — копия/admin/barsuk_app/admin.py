from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from rangefilter.filters import DateRangeFilter
import json
from django.utils.timesince import timesince
from django.utils.safestring import mark_safe

from .models import TelegramUser, Event, Request, ContentCategory, ContentItem


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_role')
    list_filter = UserAdmin.list_filter + ('groups',)

    def get_role(self, obj):
        if obj.is_superuser:
            return 'Администратор'
        elif obj.groups.filter(name='Manager').exists():
            return 'Менеджер'
        elif obj.groups.filter(name='Marketer').exists():
            return 'Маркетолог'
        elif obj.groups.filter(name='Viewer').exists():
            return 'Наблюдатель'
        return 'Пользователь'

    get_role.short_description = 'Роль'


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(TelegramUser)
class TelegramUserAdmin(ImportExportModelAdmin):
    list_display = ('id', 'telegram_id', 'username', 'full_name', 'phone', 'get_status_colored',
                    'is_18_confirmed', 'points', 'created_at')
    list_display_links = ('id', 'telegram_id', 'username')
    list_filter = ('status', 'is_18_confirmed', 'city', 'level',
                   ('created_at', DateRangeFilter),
                   ('last_activity', DateRangeFilter))
    search_fields = ('telegram_id', 'username', 'first_name', 'last_name', 'phone')
    readonly_fields = ('created_at', 'updated_at', 'last_activity')
    list_per_page = 50

    fieldsets = (
        ('Основная информация', {
            'fields': ('telegram_id', 'username', 'first_name', 'last_name', 'phone', 'language_code')
        }),
        ('Статусы и подтверждения', {
            'fields': ('status', 'is_18_confirmed', 'consent_accepted',
                       'consent_version', 'consent_accepted_at')
        }),
        ('Дополнительная информация', {
            'fields': ('birth_date', 'city', 'source')
        }),
        ('Лояльность', {
            'fields': ('points', 'level')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at', 'last_activity')
        }),
    )

    def get_status_colored(self, obj):
        colors = {
            'NEW': 'gray',
            'AGE_PENDING': 'orange',
            'ACTIVE': 'green',
            'BLOCKED_UNDERAGE': 'red',
            'BLOCKED_ADMIN': 'darkred',
            'DELETED': 'lightgray',
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )

    get_status_colored.short_description = 'Статус'

    def full_name(self, obj):
        return obj.full_name

    full_name.short_description = 'Имя'


@admin.register(Event)
class EventAdmin(ImportExportModelAdmin):
    list_display = ('id', 'user', 'event_type', 'created_at')
    list_filter = ('event_type', ('created_at', DateRangeFilter))
    search_fields = ('user__telegram_id', 'user__username', 'user__first_name')
    readonly_fields = ('created_at',)
    list_per_page = 100


@admin.register(Request)
class RequestAdmin(ImportExportModelAdmin):
    list_display = ('id', 'user', 'request_type', 'status', 'created_at', 'assigned_to')
    list_filter = ('request_type', 'status', 'assigned_to',
                   ('created_at', DateRangeFilter),
                   ('updated_at', DateRangeFilter))
    search_fields = ('user__telegram_id', 'user__username', 'user__phone', 'manager_notes')
    list_per_page = 50
    list_editable = ('status', 'assigned_to')

    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'request_type', 'status', 'assigned_to')
        }),
        ('Данные заявки', {
            'fields': ('data',)
        }),
        ('Заметки менеджера', {
            'fields': ('manager_notes',)
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(ContentCategory)
class ContentCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'item_count', 'is_active', 'created_at')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')

    def item_count(self, obj):
        return obj.items.count()

    item_count.short_description = 'Кол-во позиций'


@admin.register(ContentItem)
class ContentItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price_display', 'order', 'is_active', 'created_at')
    list_editable = ('order', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description')
    list_per_page = 50

    def price_display(self, obj):
        return obj.price_display

    price_display.short_description = 'Цена'


admin.site.site_header = "Панель управления БарсукЪ"
admin.site.site_title = "Админ-панель БарсукЪ"
admin.site.index_title = "Добро пожаловать в панель управления"