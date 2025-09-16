from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Signal handler to create a Profile instance automatically
    when a new User instance is created.
    """
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """
    Signal handler to save the profile whenever the user object is saved.
    This ensures the profile is kept in sync with the user.
    """
    instance.profile.save()






