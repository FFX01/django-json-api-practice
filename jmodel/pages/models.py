from django.db import models


class Page(models.Model):

    title = models.CharField(
        max_length=255,
        blank=False
    )
    slug = models.SlugField(
        max_length=300,
        blank=True
    )
    meta_title = models.CharField(
        max_length=120,
        blank=True
    )
    meta_description = models.CharField(
        max_length=200,
        blank=True
    )
    css = models.TextField(
        blank=True
    )
    content = models.TextField(
        blank=True
    )

    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'
