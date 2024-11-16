from habits.apps import HabitsConfig
from django.urls import path

from habits.views import HabitCreateAPIView, HabitListAPIView, HabitRetrieveAPIView, HabitUpdateAPIView, \
    HabitDestroyAPIView, AllHabitListAPIView

app_name = HabitsConfig.name

urlpatterns = [
    path('habit/create/', HabitCreateAPIView.as_view(), name='habit_create'),
    path('all_habit/list/', AllHabitListAPIView.as_view(), name='all_habit_list'),
    path('habit/list/', HabitListAPIView.as_view(), name='habit_list'),
    path('habit/retrieve/<int:pk>/', HabitRetrieveAPIView.as_view(), name='habit_retrieve'),
    path('habit/update/<int:pk>/', HabitUpdateAPIView.as_view(), name='habit_update'),
    path('habit/destroy/<int:pk>/', HabitDestroyAPIView.as_view(), name='habit_destroy'),
]
