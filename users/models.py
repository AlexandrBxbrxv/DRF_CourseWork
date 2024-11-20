from django.contrib.auth.models import AbstractUser
from django.db import models
from main.models import NULLABLE


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, **NULLABLE, verbose_name='email')

    tg_chat_id = models.CharField(max_length=50, **NULLABLE, verbose_name='id чата телеграмма')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
