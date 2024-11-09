from rest_framework import serializers

from habits.models import Habit


class AssociatedHabitSerializer(serializers.ModelSerializer):
    """Сериализатор связанной привычки для модели Habit."""
    is_nice_habit = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Habit
        exclude = ('associated_habit', 'reward',)

    @staticmethod
    def get_is_nice_habit(habit):
        return habit.is_nice_habit


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Habit."""
    is_nice_habit = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Habit
        fields = '__all__'

    @staticmethod
    def get_is_nice_habit(habit):
        return habit.is_nice_habit
