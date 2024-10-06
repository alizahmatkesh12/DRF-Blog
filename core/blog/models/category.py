from django.db import models
from django.utils.translation import gettext as _
from django.utils.text import slugify

from .base import BaseModel

class Category(BaseModel):
    name = models.CharField(max_length=255, unique=True, verbose_name=_("Name"),)
    slug = models.SlugField(max_length=255, unique=True, blank=False,)
    
    class Meta:
        ordering = ["-id"]
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        
    def __str__(self):
        return self.name
    
