from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User_details
from wallet.models import Wallet
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def create_user_details(sender, instance, created, **kwargs):
    if created:
    
        User_details.objects.create(user_id=instance)



@receiver(post_save, sender=User)
def wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user_id=instance)