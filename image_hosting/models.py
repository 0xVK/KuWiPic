from django.db import models
import datetime, string, random
from PIL import Image as PImage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
import os


class Image(models.Model):

    image = models.ImageField()
    upload_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField()

    class Meta:
        verbose_name = 'Зображення'
        verbose_name_plural = 'Зображення'

    def get_absolute_url(self):
        return self.slug

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        self.image.name = self.slug + '.jpg'
        super(Image, self).save()

        im = PImage.open(self.image.path)

        width, height = im.size
        if width > 860:
            new_width = 860
            new_height = (height * 860) / width
            new_size = new_width, new_height
            im.thumbnail(new_size, PImage.ANTIALIAS)
            im.save(self.image.path)



