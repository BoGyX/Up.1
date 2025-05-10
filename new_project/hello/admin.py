from django.contrib import admin
from .models import (
    Category,
    Manufacturer,
    Artist,
    VinylRecord,
    User,
    Order,
    Cart,
    OrderDetail
)

# Регистрация моделей в админке Django
admin.site.register(Category)
admin.site.register(Manufacturer)
admin.site.register(Artist)
admin.site.register(VinylRecord)
admin.site.register(User)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(OrderDetail)
