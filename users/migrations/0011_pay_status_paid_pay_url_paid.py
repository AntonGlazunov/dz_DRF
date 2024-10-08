# Generated by Django 4.2.16 on 2024-09-28 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_pay_payment_method_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='pay',
            name='status_paid',
            field=models.BooleanField(default=False, verbose_name='Статус оплаты'),
        ),
        migrations.AddField(
            model_name='pay',
            name='url_paid',
            field=models.URLField(blank=True, max_length=100, null=True, verbose_name='Ссылка на оплату'),
        ),
    ]
