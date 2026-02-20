from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Task

class TaskModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        self.task = Task.objects.create(
            user = self.user,
            title ='Тестовая задача',
            description = 'Описание тестовой задачи'
        )
    
    def task_creation(self):
        self.assertEqual(self.task.title, 'Тестовая задача')
        self.assertEqual(self.task.description, 'Описание тестовой задачи')
        self.assertEqual(self.task.user, self.user)
        self.assertFalse(self.task.completed)
        self.assertIsNotNone(self.task.created_at)

    def test_task_str_method(self):
        
        self.assertEqual(str(self.task), 'Тестовая задача (⏳)')
        
        # Отмечаем как выполненную
        self.task.completed = True
        self.task.save()
        self.assertEqual(str(self.task), 'Тестовая задача (✅)')
    
    def test_task_default_completed(self):
        
        self.assertFalse(self.task.completed)
        
    
"""Тестирование регистрации"""
class RegistrationTest(TestCase):
    
    def test_registration_page_status_code(self):
        """Страница регистрации открывается (200 OK)"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
    
    def test_registration_form_valid(self):
        """Можно зарегистрировать нового пользователя"""
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'securepass123',
            'password2': 'securepass123',
        })
        # После успешной регистрации должно перенаправить (302)
        self.assertEqual(response.status_code, 302)
        # Проверяем, что пользователь создался
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_registration_passwords_dont_match(self):
        """Если пароли не совпадают, показываем ошибку"""
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'pass123',
            'password2': 'pass456',
        })
        # Должна остаться на той же странице (200)
        self.assertEqual(response.status_code, 200)
        # Пользователь не должен создаться
        self.assertFalse(User.objects.filter(username='newuser').exists())
    
    def test_registration_duplicate_username(self):
        """Нельзя зарегистрироваться с существующим именем"""
        # Сначала создаём пользователя
        User.objects.create_user(username='existing', password='pass123')
        
        # Пытаемся зарегистрироваться с тем же именем
        response = self.client.post(reverse('register'), {
            'username': 'existing',
            'password1': 'newpass123',
            'password2': 'newpass123',
        })
        # Должна остаться на странице регистрации
        self.assertEqual(response.status_code, 200)
        # Второй пользователь не создаётся
        self.assertEqual(User.objects.filter(username='existing').count(), 1)
        
    
    
class LoginLogoutTest(TestCase):
    """Тестирование входа и выхода"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_login_page_status_code(self):
        """Страница входа открывается"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
    
    def test_login_valid_credentials(self):
        """Вход с правильными данными работает"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123',
        })
        self.assertEqual(response.status_code, 302)  # Редирект
        self.assertRedirects(response, reverse('dashboard'))
    
    def test_login_invalid_credentials(self):
        """Вход с неправильным паролем не работает"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpass',
        })
        self.assertEqual(response.status_code, 200)  # Остался на странице
    
    def test_logout(self):
        """Выход из системы работает"""
        # Сначала логинимся
        self.client.login(username='testuser', password='testpass123')
        # Потом выходим
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Редирект
        self.assertRedirects(response, reverse('index'))




class DashboardTest(TestCase):
    """Тестирование dashboard и безопасности"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_dashboard_requires_login(self):
        """Без логина на dashboard не попасть"""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)  # Редирект на логин
    
    def test_dashboard_with_login(self):
        """С логином dashboard открывается"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)



class TaskCRUDTest(TestCase):
    """Тестирование создания/редактирования/удаления задач"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        self.task = Task.objects.create(
            user=self.user,
            title='Тестовая задача',
            description='Описание'
        )
    
    def test_create_task(self):
        """Создание задачи работает"""
        response = self.client.post(reverse('task_create'), {
            'title': 'Новая задача',
            'description': 'Описание новой задачи',
        })
        self.assertEqual(response.status_code, 302)  # Редирект
        self.assertTrue(Task.objects.filter(title='Новая задача').exists())
    
    def test_edit_task(self):
        """Редактирование задачи работает"""
        response = self.client.post(
            reverse('task_edit', args=[self.task.id]),
            {
                'title': 'Обновлённый заголовок',
                'description': 'Обновлённое описание',
            }
        )
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Обновлённый заголовок')
    
    def test_delete_task(self):
        """Удаление задачи работает"""
        response = self.client.post(reverse('task_delete', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())
    
    def test_toggle_task(self):
        """Переключение статуса работает"""
        self.assertFalse(self.task.completed)
        response = self.client.get(reverse('task_toggle', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertTrue(self.task.completed)



class SecurityTest(TestCase):
    """Тестирование безопасности (нельзя трогать чужие задачи)"""
    
    def setUp(self):
        # Создаём двух пользователей
        self.user1 = User.objects.create_user(
            username='user1',
            password='pass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='pass123'
        )
        
        # Задача первого пользователя
        self.task = Task.objects.create(
            user=self.user1,
            title='Задача пользователя 1',
            description='Описание'
        )
        
        # Логинимся под вторым пользователем
        self.client.login(username='user2', password='pass123')
    
    def test_cant_edit_others_task(self):
        """Нельзя редактировать чужую задачу"""
        response = self.client.post(
            reverse('task_edit', args=[self.task.id]),
            {'title': 'Попытка взлома', 'description': 'Хак'}
        )
        # Должна быть ошибка 404 (не нашли задачу)
        self.assertEqual(response.status_code, 404)
    
    def test_cant_delete_others_task(self):
        """Нельзя удалять чужую задачу"""
        response = self.client.post(reverse('task_delete', args=[self.task.id]))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(Task.objects.filter(id=self.task.id).exists())
    
    def test_cant_toggle_others_task(self):
        """Нельзя менять статус чужой задачи"""
        response = self.client.get(reverse('task_toggle', args=[self.task.id]))
        self.assertEqual(response.status_code, 404)



    