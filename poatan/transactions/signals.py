from django.db.models.signals import post_save
from django.dispatch import receiver
from contributions.models import Contribution
from payout.models import Payout
from .services import LedgerService
import logging


logger = logging.getLogger(__name__)

@receiver(post_save, sender=Contribution)
def handle_contribution(sender, instance, created, **kwargs):
    """Dual-layer recording: via save() AND signals"""
    if instance.status == 'confirmed':
        try:
            LedgerService.record_contribution(instance)
        except Exception as e:
            logger.error(f"Signal failed to record contribution {instance.id}: {e}")

@receiver(post_save, sender=Contribution)
def record_contribution(sender, instance, created, **kwargs):
    if instance.status == 'confirmed' and not created:
        LedgerService.record_contribution(instance)

@receiver(post_save, sender=Payout)
def record_payout(sender, instance, created, **kwargs):
    if instance.status == 'completed' and not created:
        LedgerService.record_payout(instance)