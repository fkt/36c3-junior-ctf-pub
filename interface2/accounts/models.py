from django.utils.timezone import now
from django.db import models
from django.contrib.auth.models import AbstractUser

from challenges.models import Challenge

class User(AbstractUser):
    stage = models.IntegerField(default=1)
    stage_time = models.DateTimeField(default=now)
    last_chal_time = models.DateTimeField(default=now)
    solves = models.ManyToManyField(Challenge, blank=True)

