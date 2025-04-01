from datetime import timedelta
from django.db import models
from django.contrib.auth import get_user_model
from cashpool.models import CashPool
from django.db.models import Sum
from django.utils import timezone
from transactions.services import LedgerService
import logging

logger = logging.getLogger(__name__)

User = get_user_model()

# Create your models here.
class PayoutCycle(models.Model):
    PERIOD_CHOICES = [
        ('fortnight', 'Fortnightly (14 days)'),
        ('month', 'Monthly (30 days)')
    ]
    
    name = models.CharField(max_length=100)
    period = models.CharField(max_length=10, choices=PERIOD_CHOICES, default='month')
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    chama = models.ForeignKey('cashpool.Chama', on_delete=models.CASCADE)

    def can_trigger(self, user):
        return self.chama.admin == user

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.period == 'fortnight':
                self.end_date = self.start_date + timedelta(days=14)
            else:
                self.end_date = self.start_date + timedelta(days=30)
        super().save(*args, **kwargs)

    @classmethod
    def check_and_create_payouts(cls):
        today = timezone.now().date()
        for cycle in cls.objects.filter(end_date=today, is_active=True):
            cls.create_payout_for_cycle(cycle)

    def trigger_payouts(self, initiated_by=None):
        success = 0
        for member in self.chama.members.all():
            try:
                amount = self.calculate_for_user(member)
                if amount > 0:
                    Payout.objects.create(
                        cashpool=self.chama.cashpool,
                        recipient=member,
                        cycle=self,
                        amount=amount,
                        initiated_by=initiated_by
                    )
                    success += 1
            except Exception as e:
                logger.error(f"Payout failed for {member}: {str(e)}")
        return success



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