from django.conf import settings
from django.db import models


NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    preview = models.ImageField(upload_to='university/', verbose_name='Превью', **NULLABLE)
    description = models.TextField(verbose_name='описание')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец', **NULLABLE)

    def __str__(self):
        return f'{self.title} {self.description}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='описание')
    preview = models.ImageField(upload_to='university/', verbose_name='Превью', **NULLABLE)
    video_URL = models.URLField(max_length=100, verbose_name='Ссылка на видео', **NULLABLE)
    course = models.ForeignKey('Course', verbose_name='Курс', on_delete=models.CASCADE, **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Владелец', **NULLABLE)

    def __str__(self):
        return f'{self.title} {self.description} {self.course}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

