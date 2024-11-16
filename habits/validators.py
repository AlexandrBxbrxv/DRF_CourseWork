from rest_framework import serializers


class HabitValidator:
    """Проверяет что поля associated_habit и reward не заполнены одновременно."""

    def __call__(self, value):
        self.is_nice_habit = dict(value).get("is_nice_habit")
        self.associated_habit = dict(value).get("associated_habit")
        self.reward = dict(value).get("reward")
        self.time_for_execution = int(dict(value).get("time_for_execution"))

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

        if self.time_for_execution > 120:
            message = 'Время на выполнение не должно превышать 120 секунд.'
            raise serializers.ValidationError(message)
