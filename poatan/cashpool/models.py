from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Sum

User = get_user_model()

# Create your models here.
class Chama(models.Model):
    chama_name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    chama_admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="administered_chamas")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

class CashPool(models.Model):
    chama = models.OneToOneField(Chama, on_delete=models.CASCADE, related_name="cash_pool")
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def update_balance(self):
        total_contributions = self.chama.contributions.filter(is_confrimed=True).aggregate(Sum('amount'))['amount__sum'] or 0
        total_payouts = self.chama.payouts.aggregate(Sum('amount'))['amount__sum'] or 0
        self.balance = total_contributions - total_payouts
        self.save()

