from django.db import models

from common.users.base import BaseModel, BaseMeta
from common.users.models import User


class Address(BaseModel):
    user = models.ForeignKey(User, related_name="userAddress", on_delete=models.CASCADE)
    region = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    street = models.CharField(max_length=200)
    location = models.URLField(null=True, blank=True)

    class Meta(BaseMeta):
        pass

    def __str__(self):
        return self.user.name


class Region(models.Model):
    id = models.IntegerField(db_index=True, primary_key=True)
    name_uz = models.CharField(verbose_name="Название UZ", max_length=100)
    name_ru = models.CharField(verbose_name="Название RU", max_length=100)

    class Meta:
        verbose_name = "Область "
        verbose_name_plural = "Области "

    def __str__(self):
        return self.name_uz


class District(models.Model):
    id = models.IntegerField(db_index=True, primary_key=True)
    name_uz = models.CharField(verbose_name="Название UZ", max_length=100)
    name_ru = models.CharField(verbose_name="Название RU", max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Район "
        verbose_name_plural = "Районы "

    def __str__(self):
        return self.name_uz


class Street(models.Model):
    id = models.IntegerField(db_index=True, primary_key=True)
    name_uz = models.CharField(verbose_name="Название UZ", max_length=100)
    name_ru = models.CharField(verbose_name="Название RU", max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Местность "
        verbose_name_plural = "Местности "

    def __str__(self):
        return self.name_ru
