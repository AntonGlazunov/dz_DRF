from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def mailing(instance):
    users_list = []
    users = instance.sub_course.user
    for user in users:
        users_list.append(user.email)
    subject_mail = f'Обновление курса {instance.title}'
    text_mail = (f'Добрый день, в курсе {instance.title} произошли изменения.')
    send_mail(subject_mail, text_mail, settings.EMAIL_HOST_USER, users_list, fail_silently=True)
