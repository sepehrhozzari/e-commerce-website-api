from django.contrib import admin
from .models import Item, CartItem, Cart


class ItemAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "discount_price", "image_tag",
                    "in_stock", "get_like_count", "get_dislike_count")
    list_filter = ("in_stock",)
    search_fields = ("title", "description")


class CartItemAdmin(admin.ModelAdmin):
    list_display = ("user", "item", "quantity", "is_paid")
    list_filter = ("is_paid",)
    ordering = ("is_paid",)


admin.site.register(Item, ItemAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Cart)
