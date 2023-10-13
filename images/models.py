from django.db import models

from users.models import User


# Create your models here.


class Image(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    thumbnail_200 = models.ImageField(upload_to='files/thumbnails/', blank=True)
    thumbnail_400 = models.ImageField(upload_to='files/thumbnails/', blank=True)
    original_image = models.ImageField(upload_to='files/originals/', blank=True, null=True)

    # expiring_link = models.CharField(max_length=100, blank=True, null=True)
    # expiration_time = models.DateTimeField(blank=True, null=True)
