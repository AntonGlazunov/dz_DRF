from django.core.management import BaseCommand

from university.models import Lesson, Course
from users.models import Pay
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='test3@mail.com',
            first_name='test',
            last_name='sky',
        )
        user.set_password('200818')
        user.save()

        user = User.objects.create(
            email='test4@mail.com',
            first_name='test',
            last_name='sky',
        )
        user.set_password('200818')
        user.save()

        pay = Pay.objects.create(
            user=User.objects.get(email='test3@mail.com'),
            date_pay='2024-01-02',
            paid_lesson=Lesson.objects.get(pk=1),
            sum_paid=1000,
            payment_method='cash'
        )
        pay.save()

        pay = Pay.objects.create(
            user=User.objects.get(email='test3@mail.com'),
            date_pay='2024-01-02',
            paid_course=Course.objects.get(pk=2),
            sum_paid=10000,
            payment_method='card'
        )
        pay.save()

        pay = Pay.objects.create(
            user=User.objects.get(email='test4@mail.com'),
            date_pay='2024-01-03',
            paid_lesson=Lesson.objects.get(pk=1),
            sum_paid=1000,
            payment_method='cash'
        )
        pay.save()

        pay = Pay.objects.create(
            user=User.objects.get(email='test4@mail.com'),
            date_pay='2024-01-03',
            paid_course=Course.objects.get(pk=2),
            sum_paid=10000,
            payment_method='card'
        )
        pay.save()
