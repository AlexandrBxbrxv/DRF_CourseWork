from rest_framework import generics

from habits.models import Habit
from habits.serializers import HabitSerializer


class HabitCreateAPIView(generics.CreateAPIView):
    """Контроллер для создания привычки."""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
