# capture/models.py
from django.db import models

class CapturedImage(models.Model):
    image = models.ImageField(upload_to='photos/')
    timestamp = models.DateTimeField(auto_now_add=True)
