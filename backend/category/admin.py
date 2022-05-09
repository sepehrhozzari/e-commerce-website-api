from django.contrib import admin
from .models import Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "image_tag", "is_active", "position", "parent")


admin.site.register(Category, CategoryAdmin)
