from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    CITY_CHOICES = (
        ("TEHRAN", "تهران"),
        ("SHIRAZ", "شیراز"),
        ("ISFAHAN", "اصفحان"),
        ("ARDABIL", "اردبیل"),
        ("TABRIZ", "تبریز"),
        ("KARAJ", "کرج"),
    )
    email = models.EmailField(unique=True, verbose_name="ایمیل")
    profile_picture = models.ImageField(upload_to="account/", blank=True)
    city = models.CharField(
        max_length=20, choices=CITY_CHOICES, verbose_name="شهر")
    address = models.TextField(verbose_name="آدرس")
