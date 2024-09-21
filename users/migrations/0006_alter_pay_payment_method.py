# Generated by Django 4.2.16 on 2024-09-21 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_pay_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pay',
            name='payment_method',
            field=models.CharField(blank=True, choices=[('cash', 'Наличные'), ('card', 'Карта')], max_length=4, null=True, verbose_name='Способ оплаты'),
        ),
    ]
