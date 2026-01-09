from django.shortcuts import render, redirect, get_object_or_404 # Функции Django для работы с представлениями
from django.contrib.auth.decorators import login_required # Декоратор ограничения доступа по авторизации
from .task import Task # Модель Task из текущего приложения
from .form import TaskForm # Форма TaskForm из текущего приложения


@login_required # Декоратор требует авторизации пользователя для доступа к функции
def task_list(request):
    '''
    Список задач пользователя
    '''
    
    tasks = Task.objects.filter(user=request.user).order_by('-created_at') # Получаем все задачи текущего пользователя, отсортированные по дате создания (новые сверху)
    return render(request, 'task_list.html', {'tasks': tasks}) # Рендерим шаблон task_list.html с передачей списка задач в контекст

@login_required
def task_create(request):
    '''
    Создание новой задачи
    '''
    if request.method == 'POST': # Если форма отправлена методом POST
        form = TaskForm(request.POST) # Создаем экземпляр формы с данными из POST-запроса
        if form.is_valid(): # Проверяем валидность данных формы
            task = form.save(commit=False) # Сохраняем форму с commit=False, чтобы не сохранять в БД сразу
            task.user = request.user # Привязываем задачу к текущему пользователю
            task.save() # Теперь сохраняем задачу в БД
            return redirect('task_list') # Перенаправляем пользователя на список задач
    else: # Если запрос GET (первый вход на страницу)
        form = TaskForm() # Создаем пустую форму
    return render(request, 'task_form.html', {'form': form}) # Рендерим шаблон формы создания/редактирования задачи

@login_required
def task_update(request, pk):
    '''
    Редактирование задачи
    '''
    task = get_object_or_404(Task, pk=pk, user=request.user) # Получаем задачу по ID с проверкой принадлежности текущему пользователю или возвращаем 404 ошибку
    
    if request.method == 'POST': # Если форма отправлена
        form = TaskForm(request.POST, instance=task) # Создаем форму с данными из POST-запроса и привязываем к существующей задаче
        if form.is_valid(): # Проверяем валидность данных
            form.save() # Сохраняем изменения в БД
            return redirect('task_list') # Перенаправляем на список задач
    else: # Если запрос GET (загрузка формы для редактирования)
        form = TaskForm(instance=task) # Создаем форму с предзаполненными данными из существующей задачи
    return render(request, 'task_form.html', {'form': form}) # Рендерим шаблон формы с переданной формой

@login_required
def task_delete(request, pk):
    '''
    Удаление задачи
    '''
    task = get_object_or_404(Task, pk=pk, user=request.user) # Получаем задачу по первичному ключу, проверяя принадлежность пользователю
    
    if request.method == 'POST': # Подтверждение удаления (POST-запрос)
        task.delete() # Удаляем задачу из БД
        return redirect('task_list') # Перенаправляем на список задач
    return render(request, 'task_confirm_delete.html', {'task': task}) # Отображаем шаблон подтверждения удаления задачи с передачей объекта задачи в контекст

@login_required
def task_detail(request, pk):
    '''
    Детали задачи
    '''
    task = get_object_or_404(Task, pk=pk, user=request.user) # Получаем задачу по первичному ключу, проверяя принадлежность пользователю
    return render(request, 'task_detail.html', {'task': task}) # Рендерим шаблон с детальной информацией о задаче

@login_required
def task_mark_done(request, pk):
    '''
    Отметка задачи как выполненной
    '''
    task = get_object_or_404(Task, pk=pk, user=request.user) # Получаем задачу по первичному ключу, проверяя принадлежность пользователю
    task.status = 'closed' # Устанавливаем статус 'закрытая' (closed)
    task.save() # Сохраняем изменения в БД
    return redirect('task_list') # Перенаправляем на список задач