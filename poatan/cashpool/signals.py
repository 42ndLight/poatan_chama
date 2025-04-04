from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Chama, CashPool

"""
Automatically creates a CashPool when a new Chama is created 

""" 

@receiver(post_save, sender=Chama)
def create_cashpool(sender, instance, created, **kwargs):  
    CashPool.objects.get_or_create(chama=instance)