# Курсовая работа модуля DRF

### Запуск
Заполните ".env.sample" своими данными и переименуйте его в ".env"\
В консоль пропишите из папки проекта DRF_Homework>`docker-compose build`\
После загрузки пропишите DRF_Homework>`docker-compose up`

DevLog

_v1.1_
1. Оформлен Dockerfile
2. Оформлен docker-compose.yaml
3. Проект настроен на работу с докером

_v1.0.1_
1. Исправлена ошибка не верной даты в тестах
2. Из контроллера HabitListAPIView удалено ограничение доступа IsOwner

_v1_
1. Добавлены библиотеки django-cors-headers, drf-yasg, redis, celery, eventlet, django-celery-beat, requests
2. Настройка CORS, drf-yasg, celery
3. Реализована периодическая задача отправки напоминания о привычке через ТГ бота

_v0.2.1_
1. Исправлена ошибка автоинкрементации в тестах
2. CRUD для Habit покрыт тестами
3. Доступы к эндпоинтам покрыты тестами

_v0.2_
1. Установлена библиотека coverage
2. Реализован валидатор для Habit
3. CRUD для Habit
4. Валидация Habit покрыта тестами.

_v0.1_
1. Установлены библиотеки djangorestframework, flake8, djangorestframework-simplejwt
2. Добавлено приложение habits
3. Добавлена модель Habit
4. Реализованы логин и регистрация

_v0_
1. Установлены библиотеки django, python-dotenv, psycopg2
2. Все чувствительные данные засекречены
3. Добавлены приложения main, users
4. Добавлена модель User
