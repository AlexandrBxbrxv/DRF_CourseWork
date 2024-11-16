from habits.apps import HabitsConfig
from django.urls import path

from habits.views import HabitCreateAPIView, HabitListAPIView, HabitRetrieveAPIView

app_name = HabitsConfig.name

urlpatterns = [
    path('habit/create/', HabitCreateAPIView.as_view(), name='habit_create'),
    path('habit/list/', HabitListAPIView.as_view(), name='habit_list'),
    path('habit/retrieve/', HabitRetrieveAPIView.as_view(), name='habit_retrieve'),
]
