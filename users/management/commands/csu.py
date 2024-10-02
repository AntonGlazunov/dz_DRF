from django.core.management import BaseCommand

from university.models import Lesson, Course
from users.models import Pay
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@mail.com',
            first_name='test',
            last_name='sky',
            is_superuser=True,
            is_staff=True
        )
        user.set_password('200818')
        user.save()

        user = User.objects.create(
            email='moder2@mail.com',
            first_name='test',
            last_name='sky',
        )
        user.set_password('200818')
        user.save()


