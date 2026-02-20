from django.db import models

from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    """
    Модель задачи для TODO-листа
    """
    # Связь с пользователем (ForeignKey — многие задачи к одному пользователю)
    user = models.ForeignKey( User, on_delete=models.CASCADE, related_name='tasks', verbose_name='Пользователь')
    
    # Название задачи (строка до 200 символов)
    title = models.CharField(max_length=200, verbose_name='Название')
    
    # Описание задачи (текстовое поле, может быть пустым)
    description = models.TextField( blank=True, verbose_name='Описание')
    
    # Статус выполнения (True - выполнено, False - не выполнено)
    completed = models.BooleanField(
        default=False,
        verbose_name='Выполнено'
    )
    
    # Дата создания (заполняется автоматически при создании)
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    
    # Дата обновления (обновляется автоматически при изменении)
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    
    class Meta:
        # Сортировка по умолчанию (сначала новые)
        ordering = ['-created_at']
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
    
    def __str__(self):
        # Что показывать при печати объекта
        return f"{self.title} ({'✅' if self.completed else '⏳'})"