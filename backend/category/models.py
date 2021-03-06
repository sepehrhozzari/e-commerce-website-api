from django.db import models
from django.utils.html import format_html


class CategoryManager(models.Manager):
    def is_active(self):
        return self.filter(is_active=True)


class Category(models.Model):
    parent = models.ForeignKey("self", default=None, null=True, blank=True, on_delete=models.SET_NULL,
                               related_name="children", verbose_name="زیردسته")
    title = models.CharField(max_length=200, verbose_name="عنوان دسته بندی")
    image = models.ImageField(upload_to="category/",
                              verbose_name="تصویر دسته بندی")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    position = models.IntegerField(verbose_name="پوزیشن")

    def __str__(self):
        return self.title

    objects = CategoryManager()

    class Meta:
        ordering = ("parent__id", "position")
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"

    def image_tag(self):
        return format_html(f"<img src='{self.image.url}' width=150 height=100>")
    image_tag.short_description = "تصویر دسته بندی"
