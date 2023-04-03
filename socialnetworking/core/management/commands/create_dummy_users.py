from django.core.management.base import BaseCommand, CommandError
from core.functions import create_dummy_users


class Command(BaseCommand):
    help = 'Create Dummy Users'

    def handle(self, *args, **options):
        if create_dummy_users():
            self.stdout.write(self.style.SUCCESS('Successfully Created Dummy Users'))
        else:
            self.stdout.write(self.style.ERROR('Something Went Wrong While creating Dummy Users'))

