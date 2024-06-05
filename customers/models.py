from django.db import models

# Create your models here.

class LanguageType(models.IntegerChoices):
    EN = 1, 'English'
    UZ = 2, 'Uzbek'
    RU = 3, 'Russian'


class Customer(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    phone = models.CharField(max_length=14)
    name = models.CharField(max_length=255)
    is_company = models.BooleanField(default=False)
    lang = models.PositiveSmallIntegerField(
        choices=LanguageType.choices, default=LanguageType.UZ
    )