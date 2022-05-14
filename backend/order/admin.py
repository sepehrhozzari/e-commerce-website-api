from django.contrib import admin
from .models import OrderItem


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("user", "item", "quantity")
    search_fields = ("item__title", "item__description",
                     "user__username", "user__first_name", "user__last_name")


admin.site.register(OrderItem, OrderItemAdmin)
