# Generated by Django 4.2.16 on 2024-09-23 10:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('university', '0008_course_owner_lesson_owner'),
        ('users', '0009_alter_pay_payment_method'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pay',
            name='payment_method',
            field=models.CharField(blank=True, choices=[('cash', 'Наличные'), ('card', 'Карта')], max_length=4, null=True, verbose_name='Способ оплаты'),
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_course', to='university.course', verbose_name='Курс')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_user', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
    ]
