from rest_framework import serializers

from habits.models import Habit


class AssociatedHabitSerializer(serializers.ModelSerializer):
    """Сериализатор связанной привычки для модели Habit."""
    class Meta:
        model = Habit
        exclude = ('reward',)


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Habit."""
    class Meta:
        model = Habit
        exclude = ('is_nice_habit',)
