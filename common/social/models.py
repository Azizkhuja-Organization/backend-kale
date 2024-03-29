from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from common.users.base import BaseModel


class Social(BaseModel):
    telegram = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    youtube = models.URLField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return "Social"


class Filial(BaseModel):
    social = models.ForeignKey(Social, related_name="filial", on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    location = models.URLField(null=True, blank=True)
    phone = models.CharField(max_length=14)

    def __str__(self):
        return self.phone


# class FilialImage(BaseModel):
#     filial = models.ForeignKey(Filial, related_name='filialImages', on_delete=models.CASCADE)
#     photo = models.ImageField(_("Image of Filial"), upload_to='filialImage', null=True, blank=True)
#     photo_medium = ImageSpecField(source='photo', processors=[ResizeToFill(1460, 575)], format='PNG',
#                                   options={'quality': 90})
#     photo_small = ImageSpecField(source='photo', processors=[ResizeToFill(350, 235)], format='PNG',
#                                  options={'quality': 90})


class Map(BaseModel):
    title = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=20)
    text = models.TextField(null=True, blank=True)
    location = models.TextField()
    isMap = models.BooleanField(default=False)

    def __str__(self):
        return self.phone
