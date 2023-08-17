from django.db import models

from common.users.base import BaseModel
from common.users.models import User


class Address(BaseModel):
    user = models.ForeignKey(User, related_name="userAddress", on_delete=models.CASCADE)
    region = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    street = models.CharField(max_length=200)
    location = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.user.name
