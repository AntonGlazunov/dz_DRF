# Generated by Django 4.2.16 on 2024-10-01 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_rename_user_pay_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pay',
            name='payment_method',
            field=models.CharField(blank=True, choices=[('card', 'Карта'), ('cash', 'Наличные')], max_length=4, null=True, verbose_name='Способ оплаты'),
        ),
    ]
