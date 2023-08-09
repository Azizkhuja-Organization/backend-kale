from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from common.users.base import BaseModel

User = get_user_model()


class ProductStatus(models.IntegerChoices):
    DRAFT = 1, "DRAFT"
    ACTIVE = 2, "ACTIVE"
    DELETED = 3, "DELETED"


class ProductCornerStatus(models.IntegerChoices):
    NEWS = 1, "NEWS"
    DISCOUNT = 2, "DISCOUNT"
    SPECIAL = 3, "SPECIAL"
    RECOMMENDATION = 4, "RECOMMENDATION"
    CHEAP = 5, "CHEAP"
    EXPENSIVE = 6, "EXPENSIVE"
    POPULAR = 7, "POPULAR"


class ProductUnit(models.TextChoices):
    M2 = "м2", "м2"
    PIECE = "шт", "шт"
    COMPLETE = "комп", "комп"


class Category(BaseModel):
    title = models.CharField(max_length=100)
    photo = models.ImageField(_("Image of Category"), upload_to='categoryImage', null=True, blank=True)
    photo_medium = ImageSpecField(source='photo', processors=[ResizeToFill(250, 250)], format='PNG',
                                  options={'quality': 90})
    photo_small = ImageSpecField(source='photo', processors=[ResizeToFill(70, 70)], format='PNG',
                                 options={'quality': 70})

    def __str__(self):
        return self.title_ru
        # return "self.title_ru"


class SubCategory(BaseModel):
    category = models.ForeignKey(Category, related_name="categorySubCategory", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title_ru


class Product(BaseModel):
    subcategory = models.ForeignKey(SubCategory, related_name="subcategoryProducts", on_delete=models.SET_NULL, null=True,
                                 blank=True)
    code = models.CharField(max_length=50)
    title = models.CharField(max_length=250)
    description = RichTextField()
    price = models.FloatField(default=0)
    material = models.CharField(max_length=100)
    unit = models.CharField(max_length=5, choices=ProductUnit.choices, default=ProductUnit.PIECE)
    file3D = models.URLField(blank=True, null=True)

    brand = models.CharField(max_length=50, null=True, blank=True)
    size = models.CharField(max_length=30, null=True, blank=True)
    manufacturer = models.CharField(max_length=20, null=True, blank=True)

    photo = models.ImageField(_("Image of Product"), upload_to='productImage', null=True, blank=True)
    photo_medium = ImageSpecField(source='photo', processors=[ResizeToFill(250, 250)], format='PNG',
                                  options={'quality': 90})
    photo_small = ImageSpecField(source='photo', processors=[ResizeToFill(70, 70)], format='PNG',
                                 options={'quality': 70})
    quantity = models.IntegerField(default=0)
    discount = models.FloatField(default=0)
    isTop = models.BooleanField(_("Is Top"), default=False)

    cornerStatus = models.IntegerField(choices=ProductCornerStatus.choices, null=True, blank=True)
    status = models.IntegerField(choices=ProductStatus.choices, default=ProductStatus.DRAFT)

    @property
    def amount(self):
        if self.discount:
            return round(self.price * (1 - self.discount / 100), 3)
        return self.price

    def __str__(self):
        return self.title_ru


class ProductImage(BaseModel):
    product = models.ForeignKey(Product, related_name='productImages', on_delete=models.CASCADE)
    photo = models.ImageField(_("Image of Product"), upload_to='productImage', null=True, blank=True)
    photo_medium = ImageSpecField(source='photo', processors=[ResizeToFill(250, 250)], format='PNG',
                                  options={'quality': 90})
    photo_small = ImageSpecField(source='photo', processors=[ResizeToFill(70, 70)], format='PNG',
                                 options={'quality': 70})
