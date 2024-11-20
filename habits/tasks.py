from datetime import timedelta

import requests

from config import settings
from celery import shared_task
from django.utils import timezone

from habits.models import Habit


@shared_task
def send_telegram_reminder(habit):
    params = {
        'text': f'Не забудьте выполнить полезную привычку! Сегодня в {habit.time} {habit.place} {habit.action}',
        'chat_id': habit.user.tg_chat_id
    }
    if habit.user.tg_chat_id:
        requests.get(f'{settings.TG_API_URL}{settings.TG_API_TOKEN}/sendMessage', params=params)


def send_reminders_for_habits():
    """Находит полезные привычки для напоминания, отправляет напоминания через ТГ бота,
     записывает дату следующего напоминания."""

    today = timezone.now().today().date()
    habits_for_sending = Habit.objects.filter(is_nice_habit=False).filter(next_reminder__lte=today)

    for habit in habits_for_sending:
        send_telegram_reminder.delay(habit)
        habit.next_reminder = today + timedelta(days=int(habit.periodicity))
