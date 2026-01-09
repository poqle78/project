from django.db import models # Импорт необходимых модулей Django
from django.contrib.auth.models import User # Стандартная модель пользователя Django
from django.utils import timezone # Утилиты для работы с временем

class Task(models.Model):
    '''
    Модель, представляющая задачу в системе управления задачами
    
    Атрибуты:
        STATUS_CHOICES (list): Доступные варианты статусов задачи
        PRIORITY_CHOICES (list): Доступные варианты приоритетов задачи
        title (CharField): Заголовок задачи
        description (TextField): Подробное описание задачи
        priority (CharField): Приоритет выполнения задачи
        due_date (DateField): Срок выполнения задачи
        status (CharField): Текущий статус задачи
        created_at (DateTimeField): Дата и время создания задачи
        updated_at (DateTimeField): Дата и время последнего обновления задачи
        user (ForeignKey): Пользователь, которому принадлежит задача
        
    Методы:
        __str__(): Возвращает строковое представление задачи
    '''
    # Варианты статусов задачи в виде списка кортежей
    STATUS_CHOICES = [
        ('open', 'Открытая'), # Статус: открытая задача
        ('in_progress', 'В процессе'), # Статус: задача в работе
        ('closed', 'Закрытая'), # Статус: завершенная задача
    ]
    
    # Варианты приоритетов задачи
    PRIORITY_CHOICES = [
        ('low', 'Низкий'), # Низкий приоритет
        ('medium', 'Средний'), # Средний приоритет (по умолчанию)
        ('high', 'Высокий'), # Высокий приоритет
    ]
    
    title = models.CharField(max_length=200, verbose_name='Название') # Поле: заголовок задачи
    description = models.TextField(blank=True, verbose_name='Описание') # Поле: подробное описание задачи (может быть пустым)
    # Поле: приоритет задачи с выбором из предопределенных вариантов
    priority = models.CharField(
        max_length=10, # Максимальная длина строки в БД (самое длинное значение 'medium' - 6 символов)
        choices=PRIORITY_CHOICES, # Ограничение ввода только указанными значениями
        default='medium', # Значение по умолчанию -- средний приоритет
        verbose_name='Приоритет' # Название поля для отображения в админ-панели и формах
    )
    # Поле: срок выполнения задачи
    due_date = models.DateField(
        default=timezone.now, # По умолчанию -- текущая дата
        verbose_name='Дата выполнения' # Название поля для отображения в админ-панели и формах
    )
    # Поле: текущий статус задачи
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, # Ограничение ввода только указанными статусами
        default='open', # По умолчанию -- открытая задача
        verbose_name='Статус'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания') # Поле: дата создания (автоматически устанавливается при создании записи)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления') # Поле: дата последнего обновления (автоматически обновляется при каждом сохранении)
    # Связь с моделью User: каждая задача принадлежит одному пользователю
    user = models.ForeignKey(
        User, # Ссылка на стандартную модель пользователя Django
        on_delete=models.CASCADE, # При удалении пользователя удаляются все его задачи
        related_name='tasks', # Обратная связь: user.tasks.all()
        verbose_name='Пользователь' # Название поля для отображения в админ-панели и формах
    )
    
    def __str__(self):
        '''
        Возвращает строковое представление задачи
        
        Возвращает:
            str: Строка в формате 'Название задачи (Статус)'
        '''
        return f'{self.title} ({self.get_status_display()})' # get_status_display() возвращает читаемое имя статуса
    
    class Meta:
        '''
        Метаданные модели Task
        
        Атрибуты:
            ordering (list): Порядок сортировки по умолчанию
            verbose_name (str): Человекочитаемое имя в единственном числе
            verbose_name_plural (str): Человекочитаемое имя во множественном числе
        '''
        ordering = ['-created_at'] # Сортировка по умолчанию: сначала новые задачи
        verbose_name = 'Задача' # Единственное имя для отображения
        verbose_name_plural = 'Задачи' # Множественное имя для отображения