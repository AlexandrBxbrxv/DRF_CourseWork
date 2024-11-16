from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from habits.models import Habit
from users.models import User


class HabitAPITestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(
            id=1,
            email='user@test.com',
            password='test'
        )

        self.client = APIClient()

    def test_unauthorized_create_habit(self):
        """Создание привычки без авторизации."""

        data = {
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

        self.assertTrue(not Habit.objects.all().exists())

    def test_create_associated_habit_right_way(self):
        """Создание приятной привычки по-правильному."""

        self.client.force_authenticate(user=self.user)

        data = {
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
                "id": 1,
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

        self.assertTrue(Habit.objects.all().exists())

    def test_create_associated_habit_wrong_way(self):
        """Создание приятной привычки не правильно, с наградой(reward)."""

        self.client.force_authenticate(user=self.user)

        data = {
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
        print(response.json())

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {
                'non_field_errors': ['Приятная привычка не может содержать связанной привычки или вознаграждения.']
            }
        )

        self.assertTrue(not Habit.objects.all().exists())
