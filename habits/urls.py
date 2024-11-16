from habits.apps import HabitsConfig
from django.urls import path

from habits.views import HabitCreateAPIView

app_name = HabitsConfig.name

urlpatterns = [
    path('habit/create/', HabitCreateAPIView.as_view(), name='habit_create'),
]
