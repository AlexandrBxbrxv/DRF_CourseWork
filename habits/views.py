from rest_framework import generics

from habits.models import Habit
from habits.serializers import HabitSerializer


class HabitCreateAPIView(generics.CreateAPIView):
    """Контроллер для создания привычки."""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        habit = serializer.save()
        habit.user = user
        habit.save()
