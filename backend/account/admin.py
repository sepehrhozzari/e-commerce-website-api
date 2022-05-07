from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


UserAdmin.fieldsets += (None,
                        {"fields": ("profile_picture", "city", "address")}),
UserAdmin.list_display += ("city",)
UserAdmin.list_filter += ("city",)
UserAdmin.search_fields += ("address",)

admin.site.register(User, UserAdmin)
