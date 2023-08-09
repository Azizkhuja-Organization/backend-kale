from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from common.users.base import BaseModel


class Catalog(BaseModel):
    title = models.CharField(max_length=250)
    description = RichTextField()

    photo = models.ImageField(_("Image of Catalog"), upload_to='catalogImage')
    photo_medium = ImageSpecField(source='photo', processors=[ResizeToFill(250, 250)], format='PNG',
                                  options={'quality': 90})
    photo_small = ImageSpecField(source='photo', processors=[ResizeToFill(70, 70)], format='PNG',
                                 options={'quality': 70})

    def __str__(self):
        return self.title


class CatalogImage(BaseModel):
    catalog = models.ForeignKey(Catalog, related_name='catalogImages', on_delete=models.CASCADE)
    photo = models.ImageField(_("Image of Product"), upload_to='catalogImage', null=True, blank=True)
    photo_medium = ImageSpecField(source='photo', processors=[ResizeToFill(250, 250)], format='PNG',
                                  options={'quality': 90})
    photo_small = ImageSpecField(source='photo', processors=[ResizeToFill(70, 70)], format='PNG',
                                 options={'quality': 70})
