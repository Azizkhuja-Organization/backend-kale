from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from common.users.base import BaseModel


class Portfolio(BaseModel):
    title = models.CharField(max_length=250)
    description = RichTextField()
    file3D = models.URLField(null=True, blank=True)
    photo = models.ImageField(_("Image of Portfolio"), upload_to='portfolioImage')
    photo_medium = ImageSpecField(source='photo', processors=[ResizeToFill(300, 300)], format='PNG',
                                  options={'quality': 90})
    photo_small = ImageSpecField(source='photo', processors=[ResizeToFill(80, 80)], format='PNG',
                                 options={'quality': 80})

    def __str__(self):
        return self.title


class PortfolioImage(BaseModel):
    portfolio = models.ForeignKey(Portfolio, related_name='portfolioImages', on_delete=models.CASCADE)
    photo = models.ImageField(_("Image of Product"), upload_to='portfolioImage', null=True, blank=True)
    photo_medium = ImageSpecField(source='photo', processors=[ResizeToFill(250, 250)], format='PNG',
                                  options={'quality': 90})
    photo_small = ImageSpecField(source='photo', processors=[ResizeToFill(70, 70)], format='PNG',
                                 options={'quality': 70})
