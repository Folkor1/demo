from django.db import models
from cloudinary.models import CloudinaryField


class About(models.Model):
    """
    Class for about model
    """
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=1000)
    image = CloudinaryField('image', default='placeholder', blank=True)

    class Meta:
        verbose_name = 'About'
        verbose_name_plural = 'Abouts'

    def __str__(self):
        """
        Return title
        """
        return self.title
