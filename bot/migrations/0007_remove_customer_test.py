# Generated by Django 5.0.6 on 2024-06-10 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0006_customer_test'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='test',
        ),
    ]
