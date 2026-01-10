from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from .task import Task
from .form import TaskForm, CustomUserRegistrationForm

def home(request):
    """Главная страница"""
    if request.user.is_authenticated:
        return redirect('task_list')
    return render(request, 'tracker/home.html')

def register(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('task_list')
    else:
        form = CustomUserRegistrationForm()
    return render(request, 'tracker/register.html', {'form': form})

@login_required
def task_list(request):
    """Список задач пользователя"""
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'tracker/task_list.html', {'tasks': tasks})

@login_required
def task_create(request):
    """Создание новой задачи"""
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Задача успешно создана!')
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tracker/task_form.html', {'form': form})

@login_required
def task_update(request, pk):
    """Редактирование задачи"""
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Задача успешно обновлена!')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tracker/task_form.html', {'form': form})

@login_required
def task_delete(request, pk):
    """Удаление задачи"""
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Задача успешно удалена!')
        return redirect('task_list')
    return render(request, 'tracker/task_confirm_delete.html', {'task': task})

@login_required
def task_detail(request, pk):
    """Детали задачи"""
    task = get_object_or_404(Task, pk=pk, user=request.user)
    return render(request, 'tracker/task_detail.html', {'task': task})

@login_required
def task_mark_done(request, pk):
    """Отметить задачу как выполненную"""
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.status = 'closed'
    task.save()
    messages.success(request, 'Задача отмечена как выполненная!')
    return redirect('task_list')

# Функция проверки, является ли пользователь суперпользователем
def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser)
def admin_user_list(request):
    """Список пользователей для администратора"""
    users = User.objects.all().exclude(id=request.user.id)
    return render(request, 'tracker/admin_user_list.html', {'users': users})

@user_passes_test(is_superuser)
def admin_impersonate_user(request, user_id):
    """Вход от имени другого пользователя (только для админа)"""
    user = get_object_or_404(User, id=user_id)
    tasks = Task.objects.filter(user=user).order_by('-created_at')
    return render(request, 'tracker/task_list.html', {
        'tasks': tasks,
        'viewing_as_admin': True,
        'target_user': user
    })