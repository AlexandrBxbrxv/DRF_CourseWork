# Generated by Django 4.2.2 on 2024-11-20 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habits', '0005_habit_periodicity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='next_reminder',
            field=models.DateField(auto_now=True, null=True, verbose_name='дата следующего напоминания'),
        ),
    ]