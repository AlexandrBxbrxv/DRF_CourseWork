from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit


class PermissionAPITestCase(APITestCase):
    def setUp(self) -> None:
        pass

    def test_unauthorized_create_habit(self):
        """Создание привычки без авторизации."""

        data = {
            "id": 1,
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

        self.assertTrue(not Habit.objects.filter(pk=1).exists())

    def test_unauthorized_list(self):
        """Просмотр списка привычек без авторизации."""

        response = self.client.get(
            '/habits/habit/list/',
            format='json'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )
