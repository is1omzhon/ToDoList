from django.contrib import admin
from .models import Task  # импортируем нашу модель

@admin.register(Task)  # декоратор для регистрации
class TaskAdmin(admin.ModelAdmin):
    # Какие поля показывать в списке задач
    list_display = ('title', 'user', 'completed', 'created_at')
    
    # По каким полям можно фильтровать (правая панель)
    list_filter = ('completed', 'created_at', 'user')
    
    # Поля для поиска
    search_fields = ('title', 'description')
    
    # Сортировка по умолчанию в админке
    ordering = ('-created_at',)
