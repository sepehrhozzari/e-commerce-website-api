from django.contrib import admin
from .models import Item


class ItemAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "discount_price", "image_tag",
                    "in_stock", "get_like_count", "get_dislike_count")
    list_filter = ("in_stock",)
    search_fields = ("title", "description")


admin.site.register(Item, ItemAdmin)
