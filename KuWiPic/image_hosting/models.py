# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
import os


class Album(models.Model):
    PRIVATE = 'Private'
    PUBLIC = 'Public'
    UNLISTED = 'Unlisted'
    PRIVATE_TYPES = (
        (PRIVATE, 'Private'),
        (PUBLIC, 'Public'),
        (UNLISTED, 'Unlisted'))
    name = models.CharField(max_length=35, verbose_name=_('Название'))
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField()
    private_policy = models.CharField(choices=PRIVATE_TYPES, max_length=8, verbose_name='Тип')
    create_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = _('Альбом')
        verbose_name_plural = _('Альбоми')
        permissions = (
            ('album_owner', 'Album owner'),

        )

    def __str__(self):
        return u'{} [{}] [{}] - {}'.format(self.name.capitalize(),
                                         self.images_in_album.count(),
                                         self.private_policy,
                                         self.owner.username.capitalize())

    def get_absolute_url(self):
        return '/a/{}'.format(self.slug)

# ===============================================================================================


class ImageManager(models.Manager):
    def get_latest(self, to=15):
        return self.order_by('-upload_date')[:to]

# ===============================================================================================


class Image(models.Model):

    image = models.ImageField()
    album = models.ForeignKey(Album, null=True, blank=True, related_name='images_in_album', on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField()
    views = models.IntegerField(default=0)

    objects = ImageManager()

    class Meta:
        verbose_name = _('Изображения')
        verbose_name_plural = _(u'Изображения')
        ordering = ('-upload_date', )

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return '/i/{}'.format(self.slug)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        self.image.name = self.slug + '.jpg'
        super(Image, self).save()

    def delete(self, using=None, keep_parents=False):

        try:
            os.remove(self.image.path)

        except Exception as ex:
            print(ex)

        super(Image, self).delete()

# ===============================================================================================


class Comment(models.Model):
    text = models.TextField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date', )
