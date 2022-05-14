from django.db import models
from account.models import User
from cart.models import Item


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="order_items", verbose_name="کاربر")
    item = models.ForeignKey(Item, on_delete=models.CASCADE,
                             related_name="order_items", verbose_name="محصول")
    quantity = models.IntegerField(default=1, verbose_name="تعداد")

    def __str__(self):
        return f"{self.quantity} عدد از {self.item}"

    class Meta:
        verbose_name = "آیتم سفارش"
        verbose_name_plural = "آیتم های سفارش"

    @property
    def total_price(self):
        return self.item.price * self.quantity

    @property
    def total_discount_price(self):
        return self.item.discount_price * self.quantity
