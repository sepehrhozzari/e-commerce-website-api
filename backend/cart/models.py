from django.db import models
from account.models import User, IPAddress
from django.utils.html import format_html
from category.models import Category


class ItemQuerySet(models.query.QuerySet):
    def in_stock(self):
        return self.filter(in_stock=True)


class ItemManager(models.Manager):
    def get_queryset(self):
        return ItemQuerySet(self.model, using=self._db)

    def in_stock(self):
        return self.get_queryset().in_stock()


class Item(models.Model):
    category = models.ForeignKey(
        Category, null=True, on_delete=models.SET_NULL, related_name="items", verbose_name="دسته بندی")
    title = models.CharField(max_length=200, verbose_name="عنوان محصول")
    image = models.ImageField(upload_to="cart/", verbose_name="تصویر محصول")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="قیمت محصول")
    discount_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="قیمت محصول با تخفیف")
    description = models.TextField(verbose_name="توضیحات محصول")
    in_stock = models.BooleanField(default=True, verbose_name="موجود در انبار")
    likes = models.ManyToManyField(
        User, blank=True, related_name="liked_items", verbose_name="لایک")
    dislikes = models.ManyToManyField(
        User, blank=True, related_name="disliked_items", verbose_name="دیس لایک")
    hits = models.ManyToManyField(
        IPAddress, blank=True, through="ItemHit", related_name="hits", verbose_name="بازدید ها")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    objects = ItemManager()

    def image_tag(self):
        return format_html(f"<img src='{self.image.url}' width=150 height=100>")
    image_tag.short_description = "تصویر محصول"

    def get_amount_saved(self):
        return self.price - self.discount_price

    def get_like_count(self):
        return self.likes.count()
    get_like_count.short_description = "تعداد لایک ها"

    def get_dislike_count(self):
        return self.dislikes.count()
    get_dislike_count.short_description = "تعداد دیس لایک"

    def get_hits_count(self):
        return self.hits.count()
    get_hits_count.short_description = "تعداد بازدید ها"

    class Meta:
        ordering = ("-created",)
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"


class ItemHit(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="cart_items", verbose_name="کاربر")
    item = models.ForeignKey(Item, on_delete=models.CASCADE,
                             related_name="cart_items", verbose_name="محصول")
    quantity = models.IntegerField(default=1, verbose_name="تعداد")

    def __str__(self):
        return f"{self.quantity} عدد از {self.item}"

    class Meta:
        verbose_name = "آیتم سبد خرید"
        verbose_name_plural = "آیتم های سبد خرید"

    @property
    def total_price(self):
        return self.item.price * self.quantity

    @property
    def total_discount_price(self):
        return self.item.discount_price * self.quantity

    @property
    def amount_saved(self):
        return self.total_price - self.total_discount_price


class Cart(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="carts", verbose_name="کاربر")
    items = models.ManyToManyField(
        CartItem, related_name="carts", verbose_name="محصولات")

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = "سبد خرید"
        verbose_name_plural = "سبد های خرید"

    @property
    def total_price(self):
        total = 0
        for cart_item in self.items.all():
            total += cart_item.get_total_price()
        return total

    @property
    def total_discount_price(self):
        total = 0
        for cart_item in self.items.all():
            total += cart_item.get_total_discount_price()
        return total
