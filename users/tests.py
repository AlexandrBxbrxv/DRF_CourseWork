from django.db import connection
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from habits.models import Habit
from users.models import User


class PermissionAPITestCase(APITestCase):

    def reset_sequence(self):
        with connection.cursor() as cursor:
            cursor.execute("ALTER SEQUENCE users_user_id_seq RESTART WITH 1;")
            cursor.execute("ALTER SEQUENCE habits_habit_id_seq RESTART WITH 1;")

    def setUp(self) -> None:

        self.reset_sequence()

        self.user = User.objects.create(
            email='user@test.com',
            password='test'
        )

        self.associated_habit = Habit.objects.create(
            user=self.user,
            place='test',
            time='12:02:00',
            action='test',
            is_nice_habit=True,
            associated_habit=None,
            periodicity='1',
            reward=None,
            time_for_execution=60,
            is_public=False,
            next_reminder='2024-11-20'
        )

        self.habit = Habit.objects.create(
            user=self.user,
            place='test',
            time='12:00:00',
            action='test',
            is_nice_habit=False,
            associated_habit=self.associated_habit,
            periodicity='1',
            reward=None,
            time_for_execution=120,
            is_public=False,
            next_reminder='2024-11-20'
        )

        self.other_user = User.objects.create(
            email='other_user@test.com',
            password='test'
        )

        self.other_associated_habit = Habit.objects.create(
            user=self.other_user,
            place='test',
            time='12:02:00',
            action='test',
            is_nice_habit=True,
            associated_habit=None,
            periodicity='1',
            reward=None,
            time_for_execution=60,
            is_public=False,
            next_reminder='2024-11-20'
        )

        self.other_habit = Habit.objects.create(
            user=self.other_user,
            place='test',
            time='12:00:00',
            action='test',
            is_nice_habit=False,
            associated_habit=self.other_associated_habit,
            periodicity='1',
            reward=None,
            time_for_execution=120,
            is_public=False,
            next_reminder='2024-11-20'
        )

        self.client = APIClient()

    def test_unauthorized_create_habit(self):
        """Создание привычки без авторизации."""

        data = {
            "place": "test",
            "time": "12:00:00",
            "action": "test",
            "is_nice_habit": True,
            "periodicity": "1",
            "time_for_execution": 60
        }

        response = self.client.post(
            '/habits/habit/create/',
            data=data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        self.assertTrue(not Habit.objects.filter(pk=5).exists())

    def test_unauthorized_list_habits(self):
        """Просмотр списка привычек без авторизации."""

        response = self.client.get(
            '/habits/habit/list/',
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_unauthorized_list_all_habits(self):
        """Просмотр списка всех привычек без авторизации."""

        response = self.client.get(
            '/habits/all_habit/list/',
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_unauthorized_retrieve_habit(self):
        """Просмотр привычки без авторизации."""

        response = self.client.get(
            '/habits/habit/retrieve/2/',
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_unauthorized_update_habit(self):
        """Изменение привычки без авторизации."""

        data = {
            "time": "11:00:00"
        }

        response = self.client.patch(
            '/habits/habit/update/2/',
            data=data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_unauthorized_destroy_habit(self):
        """Удаление привычки без авторизации."""

        response = self.client.delete(
            '/habits/habit/destroy/2/',
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_retrieve_other_user_habit(self):
        """Просмотр привычки другого пользователя."""

        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            '/habits/habit/retrieve/4/',
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_update_other_user_habit(self):
        """Изменение привычки другого пользователя."""

        self.client.force_authenticate(user=self.user)

        data = {
            "time": "11:00:00"
        }

        response = self.client.patch(
            '/habits/habit/update/4/',
            data=data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_destroy_other_user_habit(self):
        """Удаление привычки другого пользователя."""

        self.client.force_authenticate(user=self.user)

        response = self.client.delete(
            '/habits/habit/destroy/4/',
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )
