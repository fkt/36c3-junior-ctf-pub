from django.db import models

class Challenge(models.Model):
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=1000)
    flag = models.CharField(max_length=256)
    stage = models.IntegerField()
    files = models.FileField(blank=True)
    is_published = models.BooleanField(default=False)
