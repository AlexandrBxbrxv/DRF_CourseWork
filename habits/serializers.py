from rest_framework import serializers

from habits.models import Habit
from habits.validators import HabitValidator


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Habit."""

    class Meta:
        model = Habit
        fields = '__all__'
        validators = [
            HabitValidator(is_nice_habit='is_nice_habit', associated_habit='associated_habit', reward='reward')
        ]
