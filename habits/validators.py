from rest_framework import serializers


class HabitValidator:
    """Проверяет что поля associated_habit и reward не заполнены одновременно."""
    def __init__(self, is_nice_habit, associated_habit, reward):
        self.is_nice_habit = is_nice_habit
        self.associated_habit = associated_habit
        self.reward = reward

    def __call__(self, is_nice_habit, associated_habit, reward):
        if is_nice_habit:
            if associated_habit or reward is not None:
                message = 'Приятная привычка не может содержать связанной привычки или вознаграждения.'
                raise serializers.ValidationError(message)

        if not associated_habit:
            if associated_habit and reward is not None:
                message = 'Привычка не может содержать и связанную привычку и вознаграждение одновременно.'
                raise serializers.ValidationError(message)

