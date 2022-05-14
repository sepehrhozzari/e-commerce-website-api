from django.contrib import admin
from .models import OrderItem


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("user", "item", "quantity")


admin.site.register(OrderItem, OrderItemAdmin)
