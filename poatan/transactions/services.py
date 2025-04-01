from django.db import transaction
from .models import LedgerEntry

class LedgerService:
    @classmethod
    def record_contribution(cls, contribution):
        with transaction.atomic():
            LedgerEntry.objects.create(
                transaction_id=f"cont_{contribution.id}",
                transaction_type='contribution',
                entry_type='debit',
                amount=contribution.amount,
                account='cashpool',
                reference_id=str(contribution.id),
                chama=contribution.chama,
                user=contribution.user,
                initiated_by=contribution.confirmed_by,
                description=f"Contribution from {contribution.user.username}"
            )
            LedgerEntry.objects.create(
                transaction_id=f"cont_{contribution.id}",
                transaction_type='contribution',
                entry_type='credit',
                amount=contribution.amount,
                account='member_equity',
                reference_id=str(contribution.id),
                chama=contribution.chama,
                user=contribution.user,
                initiated_by=contribution.confirmed_by,
                description=f"Contribution credit to {contribution.user.username}"
            )
    def record_payout(cls, payout):
        with transaction.atomic():
            LedgerEntry.objects.create(
                transaction_id=f"payout_{payout.id}",
                                transaction_type='payout',
                                entry_type='credit',
                                amount=payout.amount,
                                account='cashpool',
                                reference_id=str(payout.id),
                                chama=payout.cashpool.chama,
                                user=payout.recipient,
                                initiated_by=payout.initiated_by,
                                description=f"Payout to {payout.recipient.username}"
            )
            LedgerEntry.objects.create(
                transaction_id=f"payout_{payout.id}",
                                transaction_type='payout',
                                entry_type='debit',
                                amount=payout.amount,
                                account='member_equity',
                                reference_id=str(payout.id),
                                chama=payout.cashpool.chama,
                                user=payout.recipient,
                                initiated_by=payout.initiated_by,
                                description=f"Payout debit from {payout.recipient.username}"
            )