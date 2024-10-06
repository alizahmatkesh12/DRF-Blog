from django.db import models
from django.utils.translation import gettext as _
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Create time"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Update time"))
    is_deleted = models.BooleanField(default=False, verbose_name=_("Delete post?"))
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Delete time"))


    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()