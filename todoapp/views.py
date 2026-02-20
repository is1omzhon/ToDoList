from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . models import Task
from .forms import TaskForm
from django.shortcuts import get_object_or_404


def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Пользователь с таким именем уже существует')
                return render(request, 'register.html')
            else:
                user = User.objects.create_user(username=username, password=password1)
                
                login(request, user)
                messages.success(request, 'Регистрация прошла успешно!')
                return redirect('dashboard')
        else:
            messages.error(request, 'Пароли не совпадает')
            return render(request, 'register.html')
    else:
        return render(request, 'register.html')
    
@login_required
def dashboard(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'tasks':tasks})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Вы успешно зашлииииии!!!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Неверное имя или пароль')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')
    
def logout_view(request):
    logout(request)
    messages.success(request, 'Вы вышли из системы')
    return redirect('index')

@login_required
def task_create(request):
    form = TaskForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        task = form.save(commit=False)
        task.user = request.user
        task.save()
        messages.success(request, 'Задача создана!')
        return redirect('dashboard')
    
    return render(request, 'task_form.html', {'form': form})


@login_required
def task_edit(request, pk):
    # Находим задачу, но только если она принадлежит текущему пользователю
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Задача успешно обновлена!')
            return redirect('dashboard')
    else:
        form = TaskForm(instance=task)
    
    return render(request, 'task_form.html', {'form': form, 'title': 'Редактирование задачи'})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Задача удалена!')
        return redirect('dashboard')
    
    return render(request, 'task_confirm_delete.html', {'task':task})

@login_required
def task_toggle(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    task.completed = not task.completed
    task.save()
    
    if task.completed:
        messages.success(request, f'Задача "{task.title}" отмена как выполненная!')
    else:
        messages.info(request, f'Задача "{task.title}" снова в работе.')
        
    
    return redirect('dashboard')