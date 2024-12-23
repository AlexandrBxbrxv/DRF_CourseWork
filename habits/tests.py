from django.db import connection
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from habits.models import Habit
from users.models import User


class HabitAPITestCase(APITestCase):

    def reset_sequence(self):
        with connection.cursor() as cursor:
            cursor.execute("ALTER SEQUENCE users_user_id_seq RESTART WITH 1;")
            cursor.execute("ALTER SEQUENCE habits_habit_id_seq RESTART WITH 1;")

    def setUp(self) -> None:
        self.reset_sequence()

        self.today = timezone.now().today().date().strftime('%Y-%m-%d')

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
            is_public=True,
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
            is_public=True,
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_associated_habit_right_way(self):
        """Создание приятной привычки по-правильному."""

        data = {
            "id": 5,
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
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            {
                "id": 5,
                "user": 1,
                "place": "test",
                "time": "12:00:00",
                "action": "test",
                "is_nice_habit": True,
                "associated_habit": None,
                "periodicity": "1",
                "time_for_execution": 60,
                "reward": None,
                "is_public": False,
                'next_reminder': self.today
            }
        )

        self.assertTrue(Habit.objects.filter(pk=5).exists())

    def test_create_associated_habit_with_reward(self):
        """Создание приятной привычки не правильно, с наградой(reward)."""

        data = {
            "id": 5,
            "place": "test",
            "time": "12:00:00",
            "action": "test",
            "is_nice_habit": True,
            "periodicity": "1",
            "time_for_execution": 60,
            "reward": "test",
        }

        response = self.client.post(
            '/habits/habit/create/',
            data=data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {
                'non_field_errors': ['Приятная привычка не может содержать вознаграждения.']
            }
        )

        self.assertTrue(not Habit.objects.filter(pk=5).exists())

    def test_create_associated_habit_with_associated_habit(self):
        """Создание приятной привычки не правильно, со связанной привычкой(associated_habit)."""

        data = {
            "id": 5,
            "place": "test",
            "time": "12:00:00",
            "action": "test",
            "is_nice_habit": True,
            "periodicity": "1",
            "time_for_execution": 60,
            "associated_habit": self.associated_habit.pk,
        }

        response = self.client.post(
            '/habits/habit/create/',
            data=data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {
                'non_field_errors': ['Приятная привычка не может содержать связанной привычки.']
            }
        )

        self.assertTrue(not Habit.objects.filter(pk=5).exists())

    def test_create_habit_with_associated_habit_and_reward(self):
        """Создание полезной привычки не правильно,
         со связанной привычкой(associated_habit) и вознаграждением(reward)."""

        data = {
            "id": 5,
            "place": "test",
            "time": "12:00:00",
            "action": "test",
            "is_nice_habit": False,
            "periodicity": "1",
            "time_for_execution": 60,
            "associated_habit": self.associated_habit.pk,
            "reward": "test"
        }

        response = self.client.post(
            '/habits/habit/create/',
            data=data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {
                'non_field_errors': ['Привычка не может содержать и связанную привычку и вознаграждение одновременно.']
            }
        )

        self.assertTrue(not Habit.objects.filter(pk=5).exists())

    def test_create_habit_right_way(self):
        """Создание полезной привычки по-правильному."""

        data = {
            "place": "test",
            "time": "12:00:00",
            "action": "test",
            "is_nice_habit": False,
            "periodicity": "1",
            "time_for_execution": 60,
            "reward": "test"
        }

        response = self.client.post(
            '/habits/habit/create/',
            data=data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.json(),
            {
                "id": 5,
                "user": 1,
                "place": "test",
                "time": "12:00:00",
                "action": "test",
                "is_nice_habit": False,
                "associated_habit": None,
                "periodicity": "1",
                "time_for_execution": 60,
                "reward": "test",
                "is_public": False,
                "next_reminder": self.today
            }
        )

        self.assertTrue(Habit.objects.filter(pk=5).exists())

    def test_create_habit_time_for_execution_greater_then_120(self):
        """Создание полезной привычки, с временем на выполнение(time_for_execution) больше 120 секунд."""

        data = {
            "id": 5,
            "place": "test",
            "time": "12:00:00",
            "action": "test",
            "is_nice_habit": False,
            "periodicity": "1",
            "time_for_execution": 121,
            "reward": "test"
        }

        response = self.client.post(
            '/habits/habit/create/',
            data=data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {
                'non_field_errors': ['Время на выполнение не должно превышать 120 секунд.']
            }
        )

        self.assertTrue(not Habit.objects.filter(pk=5).exists())

    def test_create_habit_with_habit(self):
        """Создание полезной привычки не правильно, в поле associated_habit указана полезная, а не приятная привычка."""

        data = {
            "id": 5,
            "place": "test",
            "time": "12:00:00",
            "action": "test",
            "is_nice_habit": False,
            "periodicity": "1",
            "time_for_execution": 120,
            "associated_habit": self.habit.pk
        }

        response = self.client.post(
            '/habits/habit/create/',
            data=data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {
                'non_field_errors': ['Связанная привычка должна ссылаться на приятную привычку.']
            }
        )

        self.assertTrue(not Habit.objects.filter(pk=5).exists())

    def test_list_users_habits(self):
        """Просмотр списка привычек пользователя."""

        response = self.client.get(
            '/habits/habit/list/',
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "count": 2,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": 2,
                        "place": "test",
                        "time": "12:00:00",
                        "action": "test",
                        "is_nice_habit": False,
                        "periodicity": "1",
                        "reward": None,
                        "time_for_execution": 120,
                        "is_public": False,
                        "user": 1,
                        "associated_habit": 1,
                        "next_reminder": self.today
                    },
                    {
                        "id": 1,
                        "place": "test",
                        "time": "12:02:00",
                        "action": "test",
                        "is_nice_habit": True,
                        "periodicity": "1",
                        "reward": None,
                        "time_for_execution": 60,
                        "is_public": False,
                        "user": 1,
                        "associated_habit": None,
                        "next_reminder": self.today
                    }
                ]
            }
        )

    def test_list_all_habits(self):
        """Просмотр списка привычек всех пользователей."""

        response = self.client.get(
            '/habits/all_habit/list/',
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            [
                {
                    "id": 4,
                    "place": "test",
                    "time": "12:00:00",
                    "action": "test",
                    "is_nice_habit": False,
                    "periodicity": "1",
                    "reward": None,
                    "time_for_execution": 120,
                    "is_public": True,
                    "user": 2,
                    "associated_habit": 3,
                    "next_reminder": self.today
                },
                {
                    "id": 3,
                    "place": "test",
                    "time": "12:02:00",
                    "action": "test",
                    "is_nice_habit": True,
                    "periodicity": "1",
                    "reward": None,
                    "time_for_execution": 60,
                    "is_public": True,
                    "user": 2,
                    "associated_habit": None,
                    "next_reminder": self.today
                }
            ]
        )

    def test_retrieve_users_habit(self):
        """Просмотр привычки пользователя."""
        response = self.client.get(
            '/habits/habit/retrieve/2/',
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "id": 2,
                "user": 1,
                "place": "test",
                "time": "12:00:00",
                "action": "test",
                "is_nice_habit": False,
                "associated_habit": 1,
                "periodicity": "1",
                "time_for_execution": 120,
                "reward": None,
                "is_public": False,
                "next_reminder": self.today
            }
        )

    def test_update_users_habit_to_wrong_values(self):
        """Обновление привычки пользователя не правильно,
         попытка добавить reward в привычку у которой есть associated_habit."""

        data = {
            "reward": "test"
        }

        response = self.client.patch(
            '/habits/habit/update/2/',
            data=data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {
                'non_field_errors': ['Привычка не может содержать и связанную привычку и вознаграждение одновременно.']
            }
        )

    def test_update_users_habit(self):
        """Обновление привычки пользователя."""

        data = {
            "time": "13:20:25",
            "periodicity": "2",
            "time_for_execution": 100,
            "is_public": True
        }

        response = self.client.patch(
            '/habits/habit/update/1/',
            data=data,
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {
                "id": 1,
                "user": 1,
                "place": "test",
                "time": "13:20:25",
                "action": "test",
                "is_nice_habit": True,
                "associated_habit": None,
                "periodicity": "2",
                "time_for_execution": 100,
                "reward": None,
                "is_public": True,
                "next_reminder": self.today
            }
        )

    def test_destroy_users_habit(self):
        """Удаление привычки пользователя."""

        response = self.client.delete(
            '/habits/habit/destroy/2/',
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertTrue(not Habit.objects.filter(pk=2).exists())
