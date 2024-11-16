import os

from django.core.management import BaseCommand
from dotenv import load_dotenv
from config.settings import BASE_DIR
from users.models import User

load_dotenv(BASE_DIR / '.env')


class Command(BaseCommand):
    """Создает суперпользователя."""
    def handle(self, *args, **options):
        user = User.objects.create(
            email=os.getenv('ADMIN_EMAIL'),
            is_staff=True,
            is_superuser=True
        )

        user.set_password(os.getenv('ADMIN_PASSWORD'))
        user.save()
