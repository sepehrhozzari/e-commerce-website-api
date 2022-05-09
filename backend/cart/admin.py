from django.contrib import admin
from .models import Item


class ItemAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "discount_price", "image_tag",
                    "in_stock", "like_count", "dislike_count", "hits_count")


admin.site.register(Item, ItemAdmin)
