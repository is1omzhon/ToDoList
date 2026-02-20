from django import forms 
from . models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название задачи'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите описание (необязательно)', 'rows': 3}),
        }
        labels = {
            'title': 'Название',
            'description': 'Описание',
        }