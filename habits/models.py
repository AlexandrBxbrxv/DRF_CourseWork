from django.db import models
from main.models import NULLABLE
from users.models import User


class Habit(models.Model):

    PERIODICITY_CHOICES = [
        ('1_day', 'Через 1 день'),
        ('2_day', 'Через 2 дня'),
        ('3_day', 'Через 3 дня'),
        ('4_day', 'Через 4 дня'),
        ('5_day', 'Через 5 дней'),
        ('6_day', 'Через 6 дней'),
        ('7_day', 'Через 7 дней'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE, related_name='habits_user',
                             verbose_name='пользователь')
    place = models.CharField(max_length=200, verbose_name='место')
    time = models.TimeField(verbose_name='время')
    action = models.TextField(verbose_name='действие')

    is_nice_habit = models.BooleanField(default=False, verbose_name='признак приятной привычки')
    associated_habit = models.ForeignKey("Habit", on_delete=models.SET_NULL, **NULLABLE, related_name='nice_habit',
                                         verbose_name='связанная привычка')
    periodicity = models.CharField(max_length=5, choices=PERIODICITY_CHOICES, verbose_name='периодичность')
    reward = models.TextField(**NULLABLE, verbose_name='вознаграждение')
    time_for_execution = models.PositiveSmallIntegerField(default=120, help_text='время на выполнение в секундах',
                                                          verbose_name='время на выполнение')
    is_public = models.BooleanField(default=False, verbose_name='признак публичности')

    def __str__(self):
        return f'Привычка {self.user}'

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'
        ordering = ('user', 'time',)
