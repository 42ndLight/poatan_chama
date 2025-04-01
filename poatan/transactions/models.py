from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

# Create your models here.
class LedgerEntry(models.Model):
    ENTRY_TYPES = [
        ('debit', 'Debit'),
        ('credit', 'Credit'),
    ]
    TRANSACTION_TYPES = [
        ('contribution', 'Contribution'),
        ('payout', 'Payout'),
        ('adjustment', 'Adjustment'),
    ]

    transaction_id = models.CharField(max_length=100, unique=True)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    initiated_by = models.ForeignKey(User, on_delete=models.PROTECT)
    entry_type = models.CharField(max_length=10, choices=ENTRY_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    account = models.CharField(max_length=50) 
    reference_id = models.CharField(max_length=100)
    chama = models.ForeignKey('cashpool.Chama', on_delete=models.PROTECT)
    user = models.ForeignKey(User, 
                           on_delete=models.PROTECT,
                           related_name='ledger_entries')
    description = models.TextField(blank=True)
    metadata = models.JSONField(default=dict)  




    class Meta:
        indexes = [
                    models.Index(fields=['chama', 'user']),
                    models.Index(fields=['transaction_type']),
                    models.Index(fields=['timestamp']),
                ]
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.amount} ({self.entry_type})"