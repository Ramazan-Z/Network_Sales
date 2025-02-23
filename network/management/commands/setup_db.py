import os

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

FILL_DATABASE = os.getenv("FILL_DATABASE", False) == "True"


class Command(BaseCommand):
    help = "Initial database installation"

    def handle(self, *args, **kwargs):
        call_command("migrate")
        if FILL_DATABASE:
            call_command("loaddata", "fixtures/network.json")
            call_command("loaddata", "fixtures/products.json")
        try:
            try:
                call_command("first_superuser")
            except IntegrityError:
                self.stdout.write(self.style.WARNING("The fitst_superuser already exists."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(str(e)))
        else:
            self.stdout.write(self.style.SUCCESS("The database is ready for use"))
