from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Chama, CashPool

@receiver(post_save, sender=Chama)
def create_cashpool(sender, instance, created, **kwargs):
    # Automatically creates a CashPool when a new Chama is created    
    CashPool.objects.get_or_create(chama=instance)