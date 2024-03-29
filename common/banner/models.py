from django.db import models
from django.utils.translation import gettext_lazy as _
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from common.users.base import BaseModel, BaseMeta


class Banner(BaseModel):
    photo = models.ImageField(_("Image of Banner"), upload_to='bannerImage', null=True, blank=True)
    photo_medium = ImageSpecField(source='photo', processors=[ResizeToFill(1463, 420)], format='PNG',
                                  options={'quality': 100})
    photo_small = ImageSpecField(source='photo', processors=[ResizeToFill(322, 209)], format='PNG',
                                 options={'quality': 70})
    photo2 = models.ImageField(_("Image of Banner"), upload_to='bannerImage', null=True, blank=True)
    photo_medium2 = ImageSpecField(source='photo2', processors=[ResizeToFill(1463, 420)], format='PNG',
                                   options={'quality': 100})
    photo_small2 = ImageSpecField(source='photo2', processors=[ResizeToFill(322, 209)], format='PNG',
                                  options={'quality': 70})
    photo3 = models.ImageField(_("Image of Banner"), upload_to='bannerImage', null=True, blank=True)
    photo_medium3 = ImageSpecField(source='photo3', processors=[ResizeToFill(1463, 420)], format='PNG',
                                   options={'quality': 100})
    photo_small3 = ImageSpecField(source='photo3', processors=[ResizeToFill(322, 209)], format='PNG',
                                  options={'quality': 70})
    url = models.CharField(max_length=250, null=True, blank=True)

    class Meta(BaseMeta):
        pass

    def __str__(self):
        return f"Banner #{self.id}"


class SmallBanner(BaseModel):
    photo = models.ImageField(_("Image of SmallBanner"), upload_to='smallBannerImage', null=True, blank=True)
    photo_medium = ImageSpecField(source='photo', processors=[ResizeToFill(967, 265)], format='PNG',
                                  options={'quality': 100})
    photo_small = ImageSpecField(source='photo', processors=[ResizeToFill(322, 209)], format='PNG',
                                 options={'quality': 70})
    photo2 = models.ImageField(_("Image of SmallBanner"), upload_to='smallBannerImage', null=True, blank=True)
    photo_medium2 = ImageSpecField(source='photo2', processors=[ResizeToFill(967, 265)], format='PNG',
                                   options={'quality': 100})
    photo_small2 = ImageSpecField(source='photo2', processors=[ResizeToFill(322, 209)], format='PNG',
                                  options={'quality': 70})
    photo3 = models.ImageField(_("Image of SmallBanner"), upload_to='smallBannerImage', null=True, blank=True)
    photo_medium3 = ImageSpecField(source='photo3', processors=[ResizeToFill(967, 265)], format='PNG',
                                   options={'quality': 100})
    photo_small3 = ImageSpecField(source='photo3', processors=[ResizeToFill(322, 209)], format='PNG',
                                  options={'quality': 70})
    url = models.CharField(max_length=250, null=True, blank=True)

    class Meta(BaseMeta):
        pass

    def __str__(self):
        return f"SmallBanner #{self.id}"


class PointerNumber(BaseModel):
    client = models.CharField(max_length=20)
    product = models.CharField(max_length=20)
    project = models.CharField(max_length=20)
    delivered = models.CharField(max_length=20)

    class Meta(BaseMeta):
        pass

    def __str__(self):
        return f"PointerNumber #{self.id}"


class HeaderDiscount(BaseModel):
    text = models.CharField(max_length=100)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"HeaderDiscount #{self.id}"
