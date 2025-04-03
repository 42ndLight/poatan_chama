from django.db import transaction
from .models import LedgerEntry
from django.db import IntegrityError
import logging


logger = logging.getLogger(__name__)

class LedgerService:
    @classmethod
    def record_contribution(cls, contribution):
        transaction_id = f"cont_{contribution.id}"
        
        # Check if entry exists first
        if LedgerEntry.objects.filter(transaction_id=transaction_id).exists():
            logger.warning(f"Ledger entry already exists for contribution {contribution.id}")
            return False
            
        try:
            with transaction.atomic():
                # Create debit entry
                LedgerEntry.objects.create(
                    transaction_id=transaction_id,
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
                
                # Create credit entry with suffix
                LedgerEntry.objects.create(
                    transaction_id=f"{transaction_id}_cr",
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
            return True
            
        except IntegrityError as e:
            logger.error(f"Failed to record contribution {contribution.id}: {str(e)}")
            return False
        

    def record_payout(cls, payout):
        transaction_id = f"cont_{payout.id}"
        
        # Check if entry exists first
        if LedgerEntry.objects.filter(transaction_id=transaction_id).exists():
            logger.warning(f"Ledger entry already exists for contribution {payout.id}")
            return False
        
        try:    
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
                    entry_type='debit',
                    transaction_type='payout',
                    amount=payout.amount,
                    account='member_equity',
                    reference_id=str(payout.id),
                    chama=payout.cashpool.chama,
                    user=payout.recipient,
                    initiated_by=payout.initiated_by,
                    description=f"Payout debit from {payout.recipient.username}"
                )
            return True
        
        except IntegrityError as e:
            logger.error(f"Failed to record contribution {payout.id}: {str(e)}")
            return False