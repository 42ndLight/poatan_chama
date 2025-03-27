from django.db import models
from cashpool.models import CashPool
from django.conf import settings

# Create your models here.
class Ledger(models.Model):
    TRANSACTION_TYPES = [
        ('contribution', 'Contribution'),
        ('payout', 'Payout'),
        ('adjustment', 'Adjustment'),
    ]


    transaction_id = models.CharField(max_length=100, unique=True)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    cashpool = models.ForeignKey(CashPool, on_delete=models.PROTECT)
    reference = models.CharField(max_length=255)  # Contribution/Payment ID
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']