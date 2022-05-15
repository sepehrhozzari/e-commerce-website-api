from django.contrib import admin
from .models import OrderItem, Order


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("user", "item", "quantity")
    search_fields = ("item__title", "item__description",
                     "user__username", "user__first_name", "user__last_name")


class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "status")


admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order, OrderAdmin)
