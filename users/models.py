from django.contrib.auth.models import AbstractUser
from django.db import models

from university.models import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    country = models.CharField(max_length=100, verbose_name='страна', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Pay(models.Model):
    PAYMENT_METHOD_CHOICES = {
        ('cash', 'Наличные'),
        ('card', 'Карта'),
    }
    user = models.ForeignKey('User', verbose_name='Пользователь', on_delete=models.CASCADE, related_name='pay_user',
                             **NULLABLE)
    date_pay = models.DateField(auto_now=False, verbose_name='Дата оплаты', **NULLABLE)
    paid_course = models.OneToOneField('university.Course', verbose_name='Курс',
                                       on_delete=models.CASCADE, related_name='paid_course_user', **NULLABLE)
    paid_lesson = models.OneToOneField('university.Lesson', verbose_name='Урок',
                                       on_delete=models.CASCADE, related_name='paid_lesson_user', **NULLABLE)
    sum_paid = models.IntegerField(verbose_name='Сумма оплаты', **NULLABLE)
    payment_method = models.CharField(max_length=4, verbose_name='Способ оплаты', choices=PAYMENT_METHOD_CHOICES,
                                      **NULLABLE)

    def __str__(self):
        return f'{self.user}'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
