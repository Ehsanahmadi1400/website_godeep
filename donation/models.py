from django.contrib.auth.models import User
from django.db import models


class Donation(models.Model):

    title = models.CharField(max_length=64, null=True, blank=True)
    price = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    is_enable = models.BooleanField(default=True)

    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} {self.price}"

