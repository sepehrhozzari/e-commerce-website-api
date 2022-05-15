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

    @property
    def total_amount_saved(self):
        return self.total_price - self.total_discount_price


class Order(models.Model):
    STATUS_CHOICES = (
        ("P", "در حال انجام"),
        ("C", "تحویل داده شده"),
        ("F", "کنسل شده"),
    )
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL,
                             related_name="orders", verbose_name="کاربر")
    status = models.CharField(max_length=1, choices=STATUS_CHOICES,
                              default="P", verbose_name="وضعیت")
    items = models.ManyToManyField(
        OrderItem, related_name="orders", verbose_name="محصولات")

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارش ها"

    def __str__(self):
        return f"سفارش کاربر {self.user}"

    @property
    def total_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.total_price
        return total

    @property
    def total_discount_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.total_discount_price
        return total

    @property
    def total_amount_saved(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.total_amount_saved
        return total
