# Курсовая работа модуля DRF

Создайте базу данных в PostgreSQL

Заполните ".env.sample" своими данными и переименуйте его в ".env"

Для запуска периодических задач:
Запустите redis-server, пропишите в консоль: 
celery -A config worker -l INFO -P eventlet
celery -A config beat -l INFO

Для запуска сайта: python manage.py runserver

DevLog

`v1.0.1`
1. Исправлена ошибка не верной даты в тестах
2. Из контроллера HabitListAPIView удалено ограничение доступа IsOwner

`v1`
1. Добавлены библиотеки django-cors-headers, drf-yasg, redis, celery, eventlet, django-celery-beat, requests
2. Настройка CORS, drf-yasg, celery
3. Реализована периодическая задача отправки напоминания о привычке через ТГ бота

`v0.2.1`
1. Исправлена ошибка автоинкрементации в тестах
2. CRUD для Habit покрыт тестами
3. Доступы к эндпоинтам покрыты тестами

`v0.2`
1. Установлена библиотека coverage
2. Реализован валидатор для Habit
3. CRUD для Habit
4. Валидация Habit покрыта тестами.

`v0.1`
1. Установлены библиотеки djangorestframework, flake8, djangorestframework-simplejwt
2. Добавлено приложение habits
3. Добавлена модель Habit
4. Реализованы логин и регистрация

`v0`
1. Установлены библиотеки django, python-dotenv, psycopg2
2. Все чувствительные данные засекречены
3. Добавлены приложения main, users
4. Добавлена модель User
