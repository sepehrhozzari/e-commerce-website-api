from django.db import models


class Category(models.Model):
    parent = models.ForeignKey("self", null=True, on_delete=models.SET_NULL,
                               related_name="children", verbose_name="زیردسته")
    title = models.CharField(max_length=200, verbose_name="عنوان دسته بندی")
    image = models.ImageField(upload_to="category/",
                              verbose_name="تصویر دسته بندی")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    position = models.IntegerField(verbose_name="پوزیشن")