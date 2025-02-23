import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Создание суперпользователя."

    def handle(self, *args, **options):
        get_user_model().objects.create_user(
            username=os.getenv("SUPERUSER_USERNAME", "superuser"),
            password=os.getenv("SUPERUSER_PASSWORD", "superuser"),
            is_staff=True,
            is_superuser=True,
        )
        self.stdout.write(self.style.SUCCESS("Successfully created superuser."))
