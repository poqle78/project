from django.contrib import admin
from django.contrib.auth.models import User
from .task import Task


class TaskInline(admin.TabularInline):
    """
    Встраиваемый (inline) редактор задач на странице пользователя в админке.

    Атрибуты:
        model (Model): Модель, связанная с этим inline-блоком.
        extra (int): Количество пустых форм для новых записей (0 = не показывать).
        fields (tuple): Поля, отображаемые в таблице задач.
        readonly_fields (tuple): Поля, доступные только для чтения.
        ordering (tuple): Порядок сортировки задач (новые сверху).
    """
    model = Task  # Указывает, что этот inline работает с моделью Task
    extra = 0  # Не отображать пустые формы для новых задач по умолчанию
    fields = ('title', 'status', 'priority', 'due_date', 'created_at')  # Какие поля показывать в таблице
    readonly_fields = ('created_at',)  # Поле 'created_at' нельзя редактировать
    ordering = ('-created_at',)  # Сортировка: сначала новые задачи


class CustomUserAdmin(admin.ModelAdmin):
    """
    Кастомный админ-класс для модели User.

    Атрибуты:
        inlines (list): Список inline-классов, подключаемых к этой модели.
        list_display (tuple): Поля, отображаемые в списке пользователей.
        search_fields (tuple): Поля, по которым выполняется поиск.
    """
    inlines = [TaskInline]  # Подключает блок задач к странице пользователя
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')  # Колонки в списке пользователей
    search_fields = ('username', 'email')  # Поля, по которым можно искать пользователей


class TaskAdmin(admin.ModelAdmin):
    """
    Кастомный админ-класс для модели Task.

    Атрибуты:
        list_display (tuple): Поля, отображаемые в списке задач.
        list_filter (tuple): Поля, по которым доступна боковая фильтрация.
        search_fields (tuple): Поля, участвующие в поиске.
        ordering (tuple): Сортировка по умолчанию.
    """
    list_display = ('title', 'user', 'priority', 'status', 'due_date', 'created_at')  # Основные колонки в списке задач
    list_filter = ('status', 'priority', 'user', 'due_date')  # Фильтры в правой панели админки
    search_fields = ('title', 'description', 'user__username')  # Поиск по заголовку, описанию и имени пользователя
    ordering = ('-created_at',)  # Сортировка: новые задачи первыми


# регистрация моделей в админ панели
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Task, TaskAdmin)