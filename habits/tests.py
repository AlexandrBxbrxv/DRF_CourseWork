from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from habits.models import Habit
from users.models import User


class HabitAPITestCase(APITestCase):

    def setUp(self) -> None:
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
            periodicity='1_day',
            reward=None,
            time_for_execution=60,
            is_public=False
        )

        self.habit = Habit.objects.create(
            user=self.user,
            place='test',
            time='12:00:00',
            action='test',
            is_nice_habit=False,
            associated_habit=self.associated_habit,
            periodicity='1_day',
            reward=None,
            time_for_execution=120,
            is_public=False
        )

        self.client = APIClient()

    def test_unauthorized_create_habit(self):
        """Создание привычки без авторизации."""

        data = {
            "id": 3,
            "place": "test",
            "time": "12:00:00",
            "action": "test",
            "is_nice_habit": True,
            "periodicity": "1_day",
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

        self.assertTrue(not Habit.objects.filter(pk=3).exists())

    def test_create_associated_habit_right_way(self):
        """Создание приятной привычки по-правильному."""

        self.client.force_authenticate(user=self.user)

        data = {
            "id": 3,
            "place": "test",
            "time": "12:00:00",
            "action": "test",
            "is_nice_habit": True,
            "periodicity": "1_day",
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
                "id": 3,
                "user": 1,
                "place": "test",
                "time": "12:00:00",
                "action": "test",
                "is_nice_habit": True,
                "associated_habit": None,
                "periodicity": "1_day",
                "time_for_execution": 60,
                "reward": None,
                "is_public": False
            }
        )

        self.assertTrue(Habit.objects.filter(pk=3).exists())

    def test_create_associated_habit_with_reward(self):
        """Создание приятной привычки не правильно, с наградой(reward)."""

        self.client.force_authenticate(user=self.user)

        data = {
            "id": 3,
            "place": "test",
            "time": "12:00:00",
            "action": "test",
            "is_nice_habit": True,
            "periodicity": "1_day",
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

        self.assertTrue(not Habit.objects.filter(pk=3).exists())

    def test_create_associated_habit_with_associated_habit(self):
        """Создание приятной привычки не правильно, со связанной привычкой(associated_habit)."""

        self.client.force_authenticate(user=self.user)

        data = {
            "id": 3,
            "place": "test",
            "time": "12:00:00",
            "action": "test",
            "is_nice_habit": True,
            "periodicity": "1_day",
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

        self.assertTrue(not Habit.objects.filter(pk=3).exists())

    def test_create_habit_with_associated_habit_and_reward(self):
        """Создание полезной привычки не правильно,
         со связанной привычкой(associated_habit) и вознаграждением(reward)."""

        self.client.force_authenticate(user=self.user)

        data = {
            "id": 3,
            "place": "test",
            "time": "12:00:00",
            "action": "test",
            "is_nice_habit": False,
            "periodicity": "1_day",
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

        self.assertTrue(not Habit.objects.filter(pk=3).exists())

    def test_create_habit_right_way(self):
        """Создание полезной привычки по-правильному."""

        self.client.force_authenticate(user=self.user)

        data = {
            "id": 10,
            "place": "test",
            "time": "12:00:00",
            "action": "test",
            "is_nice_habit": False,
            "periodicity": "1_day",
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
                "id": 10,
                "user": self.user.pk,
                "place": "test",
                "time": "12:00:00",
                "action": "test",
                "is_nice_habit": False,
                "associated_habit": None,
                "periodicity": "1_day",
                "time_for_execution": 60,
                "reward": "test",
                "is_public": False
            }
        )

        self.assertTrue(Habit.objects.filter(pk=10).exists())

    def test_create_habit_time_for_execution_greater_then_120(self):
        """Создание полезной привычки, с временем на выполнение(time_for_execution) больше 120 секунд."""

        self.client.force_authenticate(user=self.user)

        data = {
            "id": 3,
            "place": "test",
            "time": "12:00:00",
            "action": "test",
            "is_nice_habit": False,
            "periodicity": "1_day",
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

        self.assertTrue(not Habit.objects.filter(pk=3).exists())
