from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        null=False,
        error_messages={"unique": ("A user with that email already exists.")},
    )
    friends = models.ManyToManyField("self", symmetrical=True)

    def __str__(self) -> str:
        return self.email


class FriendRequest(models.Model):
    sender = models.ForeignKey(
        User, related_name="sent_requests", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        User, related_name="received_requests", on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=10,
        choices=[("sent", "Sent"), ("accepted", "Accepted"), ("rejected", "Rejected")],
        default="sent",
    )
