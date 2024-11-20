from rest_framework import serializers

from habits.models import Habit


class HabitValidator:
    """Проверяет что поля associated_habit и reward не заполнены одновременно,
     максимальное время на выполнение не больше 120, associated_habit не ссылается на полезную привычку."""

    def __init__(self, instance=None):
        self.instance = instance

    def __call__(self, value):

        # Получение данных, если данных не было в patch методе, они загружаются из объекта(instance)
        is_nice_habit = dict(value).get("is_nice_habit")
        if is_nice_habit is None:
            is_nice_habit = self.instance.is_nice_habit

        associated_habit = dict(value).get("associated_habit")
        if associated_habit is None:
            if self.instance is None:
                associated_habit = None
            else:
                associated_habit = self.instance.associated_habit

        reward = dict(value).get("reward")
        if reward is None:
            if self.instance is None:
                reward = None
            else:
                reward = self.instance.reward

        time_for_execution = dict(value).get("time_for_execution")
        if time_for_execution is None:
            time_for_execution = self.instance.time_for_execution

        # Проверка приятной привычки
        if is_nice_habit:
            if associated_habit is not None:
                message = 'Приятная привычка не может содержать связанной привычки.'
                raise serializers.ValidationError(message)
            if reward is not None:
                message = 'Приятная привычка не может содержать вознаграждения.'
                raise serializers.ValidationError(message)

        # Проверка полезной привычки
        if not is_nice_habit:
            if associated_habit and reward is not None:
                message = 'Привычка не может содержать и связанную привычку и вознаграждение одновременно.'
                raise serializers.ValidationError(message)

        # Проверка времени на выполнение
        if int(time_for_execution) > 120:
            message = 'Время на выполнение не должно превышать 120 секунд.'
            raise serializers.ValidationError(message)

        # Проверка, что associated_habit не ссылается на полезную привычку
        if associated_habit is not None:
            is_associated_habit_is_nice_habit = Habit(associated_habit).is_nice_habit
            if not is_associated_habit_is_nice_habit:
                message = 'Связанная привычка должна ссылаться на приятную привычку.'
                raise serializers.ValidationError(message)
