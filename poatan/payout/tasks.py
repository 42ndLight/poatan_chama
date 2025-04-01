from celery import shared_task
from django.utils import timezone
from .models import PayoutCycle

@shared_task
def check_payout_cycles():
    """Runs daily to trigger payouts for active cycles ending today"""
    today = timezone.now().date()
    active_cycles = PayoutCycle.objects.filter(
        end_date=today,
        is_active=True
    )
    
    for cycle in active_cycles:
        Payout.create_payout_for_cycle(cycle)
        cycle.is_active = False  # Deactivate after processing
        cycle.save()