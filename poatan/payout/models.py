from django.db import models

# Create your models here.
class PayoutCycle(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    chama = models.ForeignKey('cashpool.Chama', on_delete=models.CASCADE)

class Payout(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cycle = models.ForeignKey(PayoutCycle, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_ref = models.CharField(max_length=100, blank=True)
    initiated_by = models.ForeignKey(settings.AUTH_USER_MODEL, 
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   related_name='initiated_payouts')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True)