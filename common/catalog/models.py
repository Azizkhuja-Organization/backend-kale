from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from common.users.base import BaseModel, BaseMeta


class Catalog(BaseModel):
    title = models.CharField(max_length=250, null=True, blank=True)
    description = RichTextField(null=True, blank=True)

    photo = models.ImageField(_("Image of Catalog"), upload_to='catalogImage')
    photo_medium = ImageSpecField(source='photo', processors=[ResizeToFill(422, 600)], format='PNG',
                                  options={'quality': 90})
    photo_small = ImageSpecField(source='photo', processors=[ResizeToFill(211, 298)], format='PNG',
                                 options={'quality': 90})

    class Meta(BaseMeta):
        pass

    def __str__(self):
        return self.title_ru


class CatalogImage(BaseModel):
    catalog = models.ForeignKey(Catalog, related_name='catalogImages', on_delete=models.CASCADE)
    photo = models.ImageField(_("Image of Product"), upload_to='catalogImage', null=True, blank=True)
    photo_medium = ImageSpecField(source='photo', processors=[ResizeToFill(422, 600)], format='PNG',
                                  options={'quality': 90})
    photo_small = ImageSpecField(source='photo', processors=[ResizeToFill(211, 298)], format='PNG',
                                 options={'quality': 90})
