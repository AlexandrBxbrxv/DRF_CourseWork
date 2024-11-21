from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit
from habits.paginators import HabitPaginator
from habits.serializers import HabitSerializer, HabitUpdateSerializer
from users.permissions import IsOwner


# CRUD для Habit ####################################################
class HabitCreateAPIView(generics.CreateAPIView):
    """Контроллер для создания привычки."""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        habit = serializer.save()
        habit.user = user
        habit.save()


class AllHabitListAPIView(generics.ListAPIView):
    """Контроллер для просмотра привычек всех пользователей."""
    serializer_class = HabitSerializer
    queryset = Habit.objects.filter(is_public=True)


class HabitListAPIView(generics.ListAPIView):
    """Контроллер для просмотра привычек текущего пользователя."""
    serializer_class = HabitSerializer
    pagination_class = HabitPaginator

    def get_queryset(self):
        user = self.request.user
        return Habit.objects.filter(user=user)


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """Контроллер для просмотра привычки текущего пользователя."""
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class HabitUpdateAPIView(generics.UpdateAPIView):
    """Контроллер для обновления привычки текущего пользователя."""
    serializer_class = HabitUpdateSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class HabitDestroyAPIView(generics.DestroyAPIView):
    """Контроллер для удаления привычки текущего пользователя."""
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
