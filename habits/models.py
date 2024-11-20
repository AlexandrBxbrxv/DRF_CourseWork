from django.db import models

from main.models import NULLABLE
from users.models import User


class Habit(models.Model):

    PERIODICITY_CHOICES = [
        ('1', 'Через 1 день'),
        ('2', 'Через 2 дня'),
        ('3', 'Через 3 дня'),
        ('4', 'Через 4 дня'),
        ('5', 'Через 5 дней'),
        ('6', 'Через 6 дней'),
        ('7', 'Через 7 дней'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE, related_name='habits_user',
                             verbose_name='пользователь')
    place = models.CharField(max_length=200, verbose_name='место')
    time = models.TimeField(verbose_name='время')
    action = models.TextField(verbose_name='действие')

    is_nice_habit = models.BooleanField(default=False, verbose_name='признак приятной привычки')
    associated_habit = models.ForeignKey("Habit", on_delete=models.SET_NULL, **NULLABLE, related_name='nice_habit',
                                         verbose_name='связанная привычка')
    periodicity = models.CharField(max_length=1, default='1', choices=PERIODICITY_CHOICES, verbose_name='периодичность')
    reward = models.TextField(**NULLABLE, verbose_name='вознаграждение')
    time_for_execution = models.PositiveSmallIntegerField(default=120, help_text='время на выполнение в секундах',
                                                          verbose_name='время на выполнение')
    is_public = models.BooleanField(default=False, verbose_name='признак публичности')

    next_reminder = models.DateField(**NULLABLE, auto_now=True, verbose_name='дата следующего напоминания')

    def __str__(self):
        return f'Привычка {self.user}'

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'
        ordering = ('user', 'time',)
