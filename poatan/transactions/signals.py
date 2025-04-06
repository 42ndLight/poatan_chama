
from django.db.models.signals import post_save
"""
signals.py

This module defines Django signal handlers for the Contribution and Payout models.
It listens to post-save events and triggers ledger recording operations via the LedgerService.
"""
from django.dispatch import receiver
from contributions.models import Contribution
from payout.models import Payout
from .services import LedgerService
import logging


logger = logging.getLogger(__name__)

@receiver(post_save, sender=Contribution)
def handle_contribution(sender, instance, created, **kwargs):
    if instance.status == 'confirmed':
        try:
            LedgerService.record_contribution(instance)
        except Exception as e:
            logger.error(f"Signal failed to record contribution {instance.id}: {e}")

@receiver(post_save, sender=Payout)
def handle_payout_completion(sender, instance, **kwargs):
    if instance.status == 'completed':
        try:
            LedgerService.record_payout(instance)
        except Exception as e:
            logger.error(f"Failed to auto-record payout {instance.id}: {e}")

