from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from common.users.base import BaseModel, BaseMeta


class Portfolio(BaseModel):
    title = models.CharField(max_length=250, null=True, blank=True)
    description = RichTextField(null=True, blank=True)
    file3D = models.URLField(null=True, blank=True)
    logo = models.ImageField(_("Image for logo Portfolio"), blank=True, null=True)
    logo_medium = ImageSpecField(source='logo', processors=[ResizeToFill(1460, 575)], format='PNG',
                                  options={'quality': 90})
    logo_small = ImageSpecField(source='logo', processors=[ResizeToFill(350, 235)], format='PNG',
                                 options={'quality': 90})
    photo = models.ImageField(_("Image of Portfolio"), upload_to='portfolioImage')
    photo_medium = ImageSpecField(source='photo', processors=[ResizeToFill(1460, 575)], format='PNG',
                                  options={'quality': 90})
    photo_small = ImageSpecField(source='photo', processors=[ResizeToFill(350, 235)], format='PNG',
                                 options={'quality': 90})

    class Meta(BaseMeta):
        pass

    def __str__(self):
        return self.title


class PortfolioImage(BaseModel):
    title = models.CharField(max_length=50, default="Interior photo")
    portfolio = models.ForeignKey(Portfolio, related_name='portfolioImages', on_delete=models.CASCADE)
    photo = models.ImageField(_("Image of Portfolio"), upload_to='portfolioImage', null=True, blank=True)
    photo_medium = ImageSpecField(source='photo', processors=[ResizeToFill(1460, 575)], format='PNG',
                                  options={'quality': 90})
    photo_small = ImageSpecField(source='photo', processors=[ResizeToFill(350, 235)], format='PNG',
                                 options={'quality': 90})
