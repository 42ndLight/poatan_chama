from django.db import models, transaction
from cashpool.models import Chama
from django.contrib.auth import get_user_model
from django.db.models import F
from django.core.exceptions import ValidationError
import logging



logger = logging.getLogger(__name__)
# Create your models here.
User = get_user_model()

class Contribution(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name = "contributions")
    chama = models.ForeignKey(Chama, on_delete=models.CASCADE, related_name="contributions", default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """Ensure cash pool updates after confirming contribution."""
        with transaction.atomic():  # Ensure atomicity
            super().save(*args, **kwargs)  # Save the contribution
            if self.is_confirmed:
                try:
                    # Update the cash pool balance
                    self.chama.cash_pool.balance = F('balance') + self.amount
                    self.chama.cash_pool.save()
                except Exception as e:
                    # Log the error and re-raise
                    logger.error(f"Failed to update cash pool for Chama '{self.chama.name}'. Error: {str(e)}")
                    raise ValidationError(f"Failed to update cash pool: {str(e)}")

    

    def __str__(self):
        return f"{self.user.username} - {self.amount}"
    

