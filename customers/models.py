from django.db import models

# Create your models here.

class LanguageCodes(models.TextChoices):
    EN = 'en', 'English'
    UZ = 'uz', 'Uzbek'
    RU = 'ru', 'Russian'


class Customer(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    phone = models.CharField(max_length=14)
    name = models.CharField(max_length=255)
    is_company = models.BooleanField(default=False)
    language = models.CharField(
        max_length=2,
        choices=LanguageCodes.choices,
        default=LanguageCodes.UZ
    )