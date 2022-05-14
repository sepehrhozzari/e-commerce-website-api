from django.db import models
from account.models import User
from cart.models import Item


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="order_items", verbose_name="کاربر")
    item = models.ForeignKey(Item, on_delete=models.CASCADE,
                             related_name="order_items", verbose_name="محصول")
    quantity = models.IntegerField(default=1, verbose_name="تعداد")
