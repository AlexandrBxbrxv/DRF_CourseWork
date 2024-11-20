from datetime import timedelta

import requests

from celery import shared_task
from config import settings
from django.utils import timezone

from habits.models import Habit


@shared_task
def send_reminders_for_habits():
    """Находит полезные привычки для напоминания, отправляет напоминания через ТГ бота,
     записывает дату следующего напоминания."""

    today = timezone.now().today().date()
    habits_for_sending = Habit.objects.filter(is_nice_habit=False).filter(next_reminder=today)
    for habit in habits_for_sending:
        if habit.user.tg_chat_id:
            message = (f'Не забудьте выполнить полезную привычку!\n'
                       f'Время: {habit.time}\n'
                       f'Место: {habit.place}\n'
                       f'Действие: {habit.action}\n'
                       f'Время на выполнение: {habit.time_for_execution}')
            params = {
                'text': message,
                'chat_id': habit.user.tg_chat_id
            }
            requests.get(f'{settings.TG_API_URL}{settings.TG_API_TOKEN}/sendMessage', params=params)

        habit.next_reminder = today + timedelta(days=int(habit.periodicity))
