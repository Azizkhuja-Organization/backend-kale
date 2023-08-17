from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from common.users.base import BaseModel


class Banner(BaseModel):
    title = models.CharField(max_length=250)
    description = models.TextField()
    phone = models.CharField(max_length=15)
    startDate = models.DateField(null=True, blank=True)
    endDate = models.DateField(null=True, blank=True)
    videoURL = models.URLField(null=True, blank=True)
    photo = models.ImageField(_("Image of News"), upload_to='newsImage')
    photo_medium = ImageSpecField(source='photo', processors=[ResizeToFill(792, 420)], format='PNG',
                                  options={'quality': 90})
    photo_small = ImageSpecField(source='photo', processors=[ResizeToFill(792, 420)], format='PNG',
                                 options={'quality': 90})

    def __str__(self):
        return self.title
