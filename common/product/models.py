import os
from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from common.users.base import BaseModel, BaseMeta

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
    title = models.CharField(max_length=100, null=True, blank=True)
    photo = models.ImageField(_("Image of Category"), upload_to='categoryImage', null=True, blank=True)
    photo_medium = ImageSpecField(source='photo', processors=[ResizeToFill(500, 500)], format='PNG',
                                  options={'quality': 90})
    photo_small = ImageSpecField(source='photo', processors=[ResizeToFill(200, 200)], format='PNG',
                                 options={'quality': 90})

    def __str__(self):
        return self.title_ru
        # return f"#{self.id}"


class SubCategory(BaseModel):
    category = models.ForeignKey(Category, related_name="categorySubCategory", on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.title_ru
        # return f"#{self.id}"


class Product(BaseModel):
    subcategory = models.ForeignKey(SubCategory, related_name="subcategoryProducts", on_delete=models.SET_NULL,
                                    null=True,
                                    blank=True)
    code = models.CharField(max_length=50)
    title = models.CharField(max_length=250, null=True, blank=True)
    description = RichTextField(null=True, blank=True)
    price = models.FloatField(default=0)
    discountPrice = models.FloatField(null=True, blank=True)
    material = models.CharField(max_length=100, null=True, blank=True)
    unit = models.CharField(max_length=5, choices=ProductUnit.choices, default=ProductUnit.PIECE)
    file3D = models.URLField(blank=True, null=True)

    brand = models.CharField(max_length=50, null=True, blank=True)
    size = models.CharField(max_length=30, null=True, blank=True)
    manufacturer = models.CharField(max_length=20, null=True, blank=True)

    photo = models.ImageField(_("Image of Product"), upload_to='productImage', null=True, blank=True)
    quantity = models.IntegerField(default=0)
    discount = models.FloatField(default=0)
    isTop = models.BooleanField(_("Is Top"), default=False)

    cornerStatus = models.IntegerField(choices=ProductCornerStatus.choices, null=True, blank=True)
    status = models.IntegerField(choices=ProductStatus.choices, default=ProductStatus.DRAFT)

    class Meta(BaseMeta):
        pass

    @property
    def amount(self):
        # if self.discount:
        #     return round(self.price * (1 - self.discount / 100), 3)
        if self.discountPrice:
            return self.discountPrice
        return self.price

    def __str__(self):
        # return self.title_ru
        return f"#{self.id}"

    def save(self, *args, **kwargs):
        if self.photo:
            img = Image.open(self.photo)
            img = self.make_square(img)
            buffer = BytesIO()
            img.save(buffer, format='JPEG')  # You can change the format if needed
            self.photo.save(self.photo.name, ContentFile(buffer.getvalue()), save=False)

            print("HERE 4")
        super().save(*args, **kwargs)

    def make_square(self, image):
        width, height = image.size
        new_size = max(width, height)
        new_image = Image.new("RGB", (new_size, new_size), "white")  # Use "RGBA" for transparency
        new_image.paste(image, ((new_size - width) // 2, (new_size - height) // 2))
        return new_image


class ProductImage(BaseModel):
    product = models.ForeignKey(Product, related_name='productImages', on_delete=models.CASCADE)
    photo = models.ImageField(_("Image of Product"), upload_to='productImage', null=True, blank=True)
    photo_medium = ImageSpecField(source='photo', processors=[ResizeToFill(500, 500)], format='PNG',
                                  options={'quality': 90})
    photo_small = ImageSpecField(source='photo', processors=[ResizeToFill(200, 200)], format='PNG',
                                 options={'quality': 90})
