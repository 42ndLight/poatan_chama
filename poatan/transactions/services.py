"""
services.py
This module provides services for managing ledger entries in a Django application. 
It includes functionality to record contributions and payouts in the ledger while 
ensuring data integrity through the use of database transactions.
Classes:
    LedgerService:
        A service class that provides methods to record contributions and payouts 
        as ledger entries. It ensures that duplicate entries are not created and 
        handles database integrity errors gracefully.
Methods:
    LedgerService.record_contribution(contribution):
        Records a contribution as a debit entry in the ledger. Checks for duplicate 
        entries before creating a new one. Uses a database transaction to ensure 
        atomicity and logs any errors encountered.
    LedgerService.record_payout(payout):
        Records a payout as a credit entry in the ledger. Checks for duplicate 
        entries before creating a new one. Uses a database transaction to ensure 
        atomicity and raises an exception if an error occurs.
"""
from .models import LedgerEntry
from django.db import IntegrityError
import logging
from django.db import transaction

logger = logging.getLogger(__name__)



class LedgerService:
    @classmethod
    def record_contribution(cls, contribution):
        transaction_id = f"cont_{contribution.transaction_ref}"
        
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
        
            return True
            
        except IntegrityError as e:
            logger.error(f"Failed to record contribution {contribution.id}: {str(e)}")
            return False
        
    @classmethod
    def record_payout(cls, payout):
        transaction_id = payout.transaction_ref
        
        # Check if entry exists first
        if LedgerEntry.objects.filter(transaction_id=transaction_id).exists():
            logger.warning(f"Ledger entry already exists for payout {payout.id}")
            return True
        
        try:    
            with transaction.atomic():
                LedgerEntry.objects.create(
                    transaction_id=transaction_id,
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
        
            return True
        
        except IntegrityError as e:
            logger.error(f"Failed to record payout {payout.id}: {str(e)}")
            raise