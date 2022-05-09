from django.db import models
from account.models import User


class ItemQuerySet(models.query.QuerySet):
    def in_stock(self):
        return self.filter(in_stock=True)


class ItemManager(models.Manager):
    def get_queryset(self):
        return ItemQuerySet(self.model, using=self._db)

    def in_stock(self):
        return self.get_queryset().in_stock()


class Item(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان محصول")
    image = models.ImageField(upload_to="cart/", verbose_name="تصویر محصول")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="قیمت محصول")
    discount_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="قیمت محصول با تخفیف")
    description = models.TextField(verbose_name="توضیحات محصول")
    in_stock = models.IntegerField(default=True, verbose_name="موجود در انبار")
    likes = models.ManyToManyField(
        User, blank=True, related_name="liked_items", verbose_name="لایک")
    dislikes = models.ManyToManyField(
        User, blank=True, related_name="disliked_items", verbose_name="دیس لایک")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    objects = ItemManager()

    def get_amount_saved(self):
        return self.price - self.discount_price

    @property
    def like_count(self):
        return self.likes.count()

    @property
    def dislike_count(self):
        return self.dislikes.count()

    class Meta:
        ordering = ("-created",)
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"
