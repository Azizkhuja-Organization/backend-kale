from django.contrib.auth import get_user_model
from django.db import models

from common.users.base import BaseModel

User = get_user_model()


class Message(BaseModel):
    sender = models.ForeignKey(User, related_name='authorMessages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.sender.username


class Room(BaseModel):
    name = models.CharField(max_length=100)
    participants = models.ManyToManyField(
        User, related_name='roomParticipants', blank=True)
    messages = models.ManyToManyField(Message, related_name="roomMessages", blank=True)

    def __str__(self):
        return self.name
