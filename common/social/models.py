from django.db import models

from common.users.base import BaseModel


class Social(BaseModel):
    telegram = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)

    def __str__(self):
        return "Social"


class Map(BaseModel):
    title = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    text = models.TextField()
    location = models.TextField()
    isMap = models.BooleanField(default=False)

    def __str__(self):
        return self.title + " " + self.phone
