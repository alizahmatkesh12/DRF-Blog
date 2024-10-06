from django.db import models
from django.utils.translation import gettext as _
from django.utils import timezone

from extensions.utils import upload_file_path

from .base import BaseModel
from .category import Category

class Post(BaseModel):
    STATUS_CHOICES = (
        ("p", "publish"),
        ("d", "draft"),
    )
    image = models.ImageField(
        upload_to=upload_file_path, blank=True,
        null=True, verbose_name=_("Image"),
        default="default/default-post.png"
    )
    author = models.ForeignKey(
        "accounts.profile",
        on_delete=models.CASCADE,
        verbose_name=_("Author"),
    )
    title = models.CharField(
        max_length=255,
        verbose_name=_("Title"),
    )
    content = models.TextField()
    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True,
        verbose_name=_("Slug"), 
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name="posts"
    )
    visits = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Visits"),
    )
    published_status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        verbose_name=_("Status"),
    )
    published_at = models.DateTimeField(verbose_name=_("Publish time"))
    
    def __str__(self):
        return f" {self.title} - {self.id}"
    
    class Meta:
        ordering = ["-published_at"]
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
