from rest_framework import serializers

from habits.models import Habit
from habits.validators import HabitValidator


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Habit."""

    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ('user',)
        validators = [HabitValidator()]


class HabitUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для эндпоинта update модели Habit."""
    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ('user',)
        validators = [HabitValidator()]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for validator in self.Meta.validators:
            if isinstance(validator, HabitValidator):
                validator.instance = self.instance
