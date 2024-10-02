from django.contrib.auth.models import AbstractUser
from django.db import models

from university.models import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    country = models.CharField(max_length=100, verbose_name='страна', **NULLABLE)
    last_login = models.DateField(auto_now=False, verbose_name='Дата последнего входа', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}, {self.is_active}'


class Pay(models.Model):
    PAYMENT_METHOD_CHOICES = {
        ('cash', 'Наличные'),
        ('card', 'Карта'),
    }
    owner = models.ForeignKey('User', verbose_name='Пользователь', on_delete=models.CASCADE, related_name='pay_user',
                             **NULLABLE)
    date_pay = models.DateField(auto_now=False, verbose_name='Дата оплаты', **NULLABLE)
    paid_course = models.ForeignKey('university.Course', verbose_name='Курс',
                                    on_delete=models.CASCADE, related_name='paid_course_user', **NULLABLE)
    paid_lesson = models.ForeignKey('university.Lesson', verbose_name='Урок',
                                    on_delete=models.CASCADE, related_name='paid_lesson_user', **NULLABLE)
    sum_paid = models.IntegerField(verbose_name='Сумма оплаты', **NULLABLE)
    status_paid = models.BooleanField(verbose_name='Статус оплаты', default=False)
    url_paid = models.URLField(max_length=1000, verbose_name='Ссылка на оплату', **NULLABLE)
    payment_method = models.CharField(max_length=4, verbose_name='Способ оплаты', choices=PAYMENT_METHOD_CHOICES,
                                      **NULLABLE)

    def __str__(self):
        return f'{self.user}'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'


class Subscription(models.Model):
    user = models.ForeignKey('users.User', verbose_name='Пользователь',
                             on_delete=models.CASCADE, related_name='sub_user', **NULLABLE)
    course = models.ForeignKey('university.Course', verbose_name='Курс',
                               on_delete=models.CASCADE, related_name='sub_course', **NULLABLE)

    def __str__(self):
        return f'{self.user} {self.course}'
