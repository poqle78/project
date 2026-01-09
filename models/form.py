from django import forms # Импортируем модуль forms из Django для создания форм
from .task import Task # Импортируем модель Task из текущего пакета для привязки к форме

class TaskForm(forms.ModelForm):
    """
    Форма для создания и редактирования задач
    
    Наследуется от ModelForm Django, что позволяет автоматически
    генерировать поля формы на основе модели Task
    
    Атрибуты:
        Meta: Вложенный класс для конфигурации формы
    
    Методы:
        clean_title(): Валидация поля названия задачи
    """

    class Meta:
        """
        Класс конфигурации для формы TaskForm
        
        Определяет связь с моделью, отображаемые поля, виджеты и метки для полей формы
        
        Атрибуты:
            model (Model): Модель, связанная с формой
            fields (list): Список полей модели, отображаемых в форме
            widgets (dict): Настройки HTML-виджетов для каждого поля
            labels (dict): Человекочитаемые названия для полей формы
        """

        model = Task # Указываем, с какой моделью связана форма
        fields = ['title', 'description', 'priority', 'due_date', 'status'] # Определяем, какие поля модели будут отображаться в форме
         # Настраиваем виджеты для каждого поля
        widgets = {
            # Поле названия задачи -- текстовый ввод с CSS-классом и placeholder
            'title': forms.TextInput(attrs={
                'class': 'form-control', # Bootstrap CSS класс
                'placeholder': 'Введите название задачи', # Подсказка в поле
                'required': True # HTML5 атрибут обязательности
            }),
            # Поле описания -- текстовое поле с несколькими строками
            'description': forms.Textarea(attrs={
                'class': 'form-control', # Bootstrap CSS класс
                'rows': 4, # Количество строк текстового поля
                'placeholder': 'Введите описание задачи' # Подсказка в поле
            }),
            'priority': forms.Select(attrs={'class': 'form-control'}), # Поле приоритета - выпадающий список
            # Поле даты выполнения -- ввод даты с HTML5 типом date
            'due_date': forms.DateInput(attrs={
                'type': 'date', # HTML5 атрибут type="date" для отображения нативного виджета выбора даты в браузере
                'class': 'form-control' # Bootstrap CSS класс
            }),
            'status': forms.Select(attrs={'class': 'form-control'}), # Поле статуса -- выпадающий список
        }
        # Настраиваем названия полей
        labels = {
            'title': 'Название задачи',
            'description': 'Описание',
            'priority': 'Приоритет',
            'due_date': 'Дата выполнения',
            'status': 'Статус',
        }
    
    def clean_title(self):
        """
        Валидация поля названия задачи
        
        Проверяет, что название задачи не пустое и не состоит только из пробелов
        Удаляет начальные и конечные пробелы из значения
        
        Возвращает:
            str: Очищенное значение названия задачи
            
        Исключения:
            forms.ValidationError: Если название задачи пустое
        """

        title = self.cleaned_data.get('title') # Получаем очищенные данные поля title
        if not title or len(title.strip()) == 0: # Проверяем, что title не пустой и не состоит только из пробелов
            raise forms.ValidationError("Название задачи обязательно для заполнения") # Генерируем ошибку валидации
        return title.strip() # Возвращаем очищенное значение (без начальных и конечных пробелов)