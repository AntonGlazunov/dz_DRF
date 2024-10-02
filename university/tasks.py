from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from datetime import timedelta, date, datetime
from university.models import Course
from users.models import Subscription, User


@shared_task
def mailing(course_pk):
    email_list = []
    course = Course.objects.get(pk=course_pk)
    subs = Subscription.objects.filter(course=course)
    for sub in subs:
        email_list.append(sub.user.email)
    subject_mail = f'Обновление курса {course.title}'
    text_mail = (f'Добрый день, в курсе {course.title} произошли изменения.')
    send_mail(subject_mail, text_mail, settings.EMAIL_HOST_USER, email_list, fail_silently=True)
    print('Письмо отправленно')


@shared_task
def check_last_login():
    users = User.objects.filter(is_active=True, is_staff=False, is_superuser=False, last_login__isnull=False)
    date_delta = timedelta(30)
    for user in users:
        date_block = date.today() - date_delta
        if user.last_login <= date_block:
            print('Блокировка пользователя')
            user.is_active = False
            user.save()
