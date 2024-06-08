from django.db import models


class LanguageCodes(models.TextChoices):
    EN = 'en', 'English'
    UZ = 'uz', 'Uzbek'
    RU = 'ru', 'Russian'


class Customer(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    phone = models.CharField(max_length=14)
    name = models.CharField(max_length=255)
    language = models.CharField(
        max_length=2,
        choices=LanguageCodes.choices,
        default=LanguageCodes.UZ
    )

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    price = models.IntegerField()

    def __str__(self) -> str:
        return self.name
    

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    amount = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f'{self.amount}; {self.product.name}; {self.customer.name}'
