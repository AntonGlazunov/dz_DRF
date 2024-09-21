from datetime import date

from django.core.management import BaseCommand

from university.models import Lesson, Course
from users.models import User

from users.models import Pay


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@mail.com',
            first_name='Admin',
            last_name='Kr_py',
            is_staff=True,
            is_superuser=True
        )
        user.set_password('200818')

        pay1 = Pay.objects.create(
            user=user,
            date_pay=date.today(),
            paid_lesson=Lesson.objects.get(pk=1),
            sum_paid=1000,
            payment_method='cash'
        )

        pay2 = Pay.objects.create(
            user=user,
            date_pay=date.today(),
            paid_course=Course.objects.get(pk=2),
            sum_paid=10000,
            payment_method='card'
        )
        pay2.save()
        user.save()
        pay1.save()
