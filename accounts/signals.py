from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profil


@receiver(post_save, sender=User)
def profil_olustur(sender, instance, created, **kwargs):
    if created:
        Profil.objects.create(kullanici=instance)


@receiver(post_save, sender=User)
def profil_kaydet(sender, instance, **kwargs):
    if hasattr(instance, "profil"):
        instance.profil.save()