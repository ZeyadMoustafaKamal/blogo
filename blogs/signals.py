from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Blog

@receiver(post_save,sender=Blog)
def creating_blog_handler(instance, created, **kwargs):
    if created:
        if not instance.members.exists():
            instance.members.add(instance.owner)
            instance.save()
