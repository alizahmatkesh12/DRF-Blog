from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .users import User
import uuid



class Profile(models.Model):
    """
    Profile class for each user which is being created to hold the information
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=250, unique=True)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    image = models.ImageField(blank=True, null=True)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email
    
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.user.email.split("@")[0]
            if Profile.objects.filter(username=self.username).exists():
                self.username = f"{self.username}-{uuid.uuid4().hex[:8]}"
        super().save(*args, **kwargs)


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    """
    Signal for post creating a user which activates when a user being created ONLY
    """
    if created:
        Profile.objects.create(user=instance)