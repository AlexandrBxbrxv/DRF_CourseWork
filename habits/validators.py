from rest_framework import serializers


class HabitValidator:
    """Проверяет что поля associated_habit и reward не заполнены одновременно."""
    def __init__(self, is_nice_habit, associated_habit, reward):
        self.is_nice_habit = is_nice_habit
        self.associated_habit = associated_habit
        self.reward = reward

    def __call__(self, value):
        self.is_nice_habit = value.get(self.is_nice_habit)
        self.associated_habit = value.get(self.associated_habit)
        self.reward = value.get(self.reward)

        if self.is_nice_habit:
            if self.associated_habit or self.reward is not None:
                message = 'Приятная привычка не может содержать связанной привычки или вознаграждения.'
                raise serializers.ValidationError(message)

        if not self.is_nice_habit:
            if self.associated_habit and self.reward is not None:
                message = 'Привычка не может содержать и связанную привычку и вознаграждение одновременно.'
                raise serializers.ValidationError(message)

