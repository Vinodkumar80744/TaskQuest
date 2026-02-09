from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
    help = 'Creates admin user if not exists'

    def handle(self, *args, **kwargs):
        username = os.environ.get('DJANGO_ADMIN_USER')
        email = os.environ.get('DJANGO_ADMIN_EMAIL')
        password = os.environ.get('DJANGO_ADMIN_PASSWORD')

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            self.stdout.write(self.style.SUCCESS('Admin user created'))
        else:
            self.stdout.write('Admin user already exists')
