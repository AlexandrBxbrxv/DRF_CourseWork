from rest_framework import serializers


class HabitValidator:
    """Проверяет что поля associated_habit и reward не заполнены одновременно."""
    def __init__(self, is_nice_habit, associated_habit, reward):
        self.is_nice_habit = is_nice_habit
        self.associated_habit = associated_habit
        self.reward = reward

    def __call__(self, value):
        self.is_nice_habit = dict(value).get(self.is_nice_habit)
        self.associated_habit = dict(value).get(self.associated_habit)
        self.reward = dict(value).get(self.reward)

        if self.is_nice_habit:
            if self.associated_habit is not None:
                message = 'Приятная привычка не может содержать связанной привычки.'
                raise serializers.ValidationError(message)
            if self.reward is not None:
                message = 'Приятная привычка не может содержать вознаграждения.'
                raise serializers.ValidationError(message)

        if not self.is_nice_habit:
            if self.associated_habit and self.reward is not None:
                message = 'Привычка не может содержать и связанную привычку и вознаграждение одновременно.'
                raise serializers.ValidationError(message)

