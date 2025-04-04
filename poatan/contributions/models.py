from django.db import models, transaction
from cashpool.models import Chama
from django.utils import timezone
import uuid
from django.contrib.auth import get_user_model
from django.db.models import F
import logging

logger = logging.getLogger(__name__)

# Calls User model from settings.py
User = get_user_model()

"""
    A model to handle a Contribution and its nessecary attributes
    A contribution can have a status for the various steps in processing and a type
    Its Save method ensures cash pool updates after confirming a contribution

"""

class Contribution(models.Model):
    CONTRIBUTION_TYPES = (
        ('regular', 'Regular'),
        ('special', 'Special'),
        ('fine', 'Fine'),
    )
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected'),
    ]

    contribution_type = models.CharField(max_length=20, choices=CONTRIBUTION_TYPES, default='regular')
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name = "contributions")
    chama = models.ForeignKey(Chama, on_delete=models.CASCADE, related_name="contributions", default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)
    confirmed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='confirmed_contributions')
    transaction_ref = models.CharField(max_length=100, unique=True, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Algorithm creates a random reference number for each confrimed contribution
    def generate_transaction_ref(self):
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        random_part = uuid.uuid4().hex[:6].upper()
        return f"CNT-{timestamp}-{random_part}"


    def save(self, *args, **kwargs):
        with transaction.atomic(): 
            is_new = self._state.adding
            old_instance = None
        
            if not is_new:
                old_instance = Contribution.objects.get(pk=self.pk)
                old_status = old_instance.status
      
            super().save(*args, **kwargs)

            if self.status == 'confirmed' and (is_new or old_status != 'confirmed'):
                    try:
                        cash_pool = self.chama.cash_pool
                        cash_pool.balance = F('balance') + self.amount
                        cash_pool.save(update_fields=['balance'])
                        cash_pool.refresh_from_db()                    
                 

                    except Exception as e:
                        logger.error(
                            f"CashPool update failed for {self}. "
                            f"Chama: {self.chama_id}, "
                            f"Amount: {self.amount}. "
                            f"Ledger recording failed: {str(e)}",
                            exc_info=True
                        )

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.status}"
    

    

