from django.db import models
from django.contrib.auth import get_user_model
from cashpool.models import CashPool
from django.db.models import Sum
from django.utils import timezone
from transactions.services import LedgerService

User = get_user_model()

# Create your models here.
class PayoutCycle(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    chama = models.ForeignKey('cashpool.Chama', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.start_date} to {self.end_date})"

    @property
    def is_current(self):
        today = timezone.now().date()
        return self.start_date <= today <= self.end_date


class Payout(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ]

    cashpool = models.ForeignKey(CashPool, on_delete=models.PROTECT)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    cycle = models.ForeignKey(PayoutCycle, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_ref = models.CharField(max_length=100, blank=True)
    initiated_by = models.ForeignKey(User, 
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   related_name='initiated_payouts')
    created_at = models.DateTimeField(auto_now_add=True)
    failure_reason = models.TextField(blank=True)
    completed_at = models.DateTimeField(null=True)

    def __str__(self):
        return f"Payout #{self.id} - {self.recipient.username} - {self.amount}"
    
    @classmethod
    def calculate_payout(user, cycle):
        from contributions.models import Contribution

        total_contributions = Contribution.objects.filter(
            user=user,
            chama=cycle.chama,
            created_at__date__gte=cycle.start_date,
            created_at__date__lte=cycle.end_date,
            status='confirmed'
        ).aggregate(total=Sum('amount'))['total'] or 0
        return total_contributions * 0.5
    
    @classmethod
    def create_payout_for_cycle(cls, cycle, initiated_by=None):
        chama = cycle.chama
        payout = []

        for member in chama.members.all():
            amount = cls.calculate_for_user(member, cycle)
            if amount > 0:
                payouts = cls(
                    cashpool = chama.cashpool,
                    recipient = member,
                    cycle = cycle,
                    amount = amount,
                    status = 'pending',
                    initiated_by=initiated_by
                )
                payouts.append(payout)

        cls.objects.bulk_create(payouts)
        return len(payouts)
    
    def process(self, transaction_ref=None):
        self.status='processing'
        if transaction_ref:
            self.transaction_ref = transaction_ref
        self.save

        self.status='completed'
        self.completed_at = timezone.now()
        self.save()
        LedgerService.record_payout(self)