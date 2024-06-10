from django.contrib import admin

from .models import Customer, Product, Order

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'language', 'location_google', 'telegram_id')

    def location_google(self, obj):
        return f'https://www.google.com/maps?q={obj.latitude},{obj.longitude}'
    location_google.allow_tags = True
    location_google.short_description = "Location  (Google)"

    # def location_yandex(self, obj):
    #     return f'https://yandex.com/maps/?ll={obj.latitude},{obj.longitude}'
    # location_yandex.allow_tags = True
    # location_yandex.short_description = "Location  (Yandex)"

admin.site.register(Product)
admin.site.register(Order)