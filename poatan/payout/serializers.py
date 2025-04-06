from django.utils import timezone
from rest_framework import serializers
from .models import Payout, PayoutCycle
import logging
from django.db import IntegrityError, transaction

logger = logging.getLogger(__name__)

class PayoutCycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayoutCycle
        fields = '__all__'
        read_only_fields = ('end_date',)

"""
    A serializer for Payout data when perfoming CRUD operations on the Payout
    The Payout can only be Created and Read
    Handles:
        Payout Creation: on Valid data passed by user and ensures the creator of payout is the user
        Validation:  Ensure payout is made from a valid Cashpool and user is an admin

"""
class PayoutSerializer(serializers.ModelSerializer):
    recipient_name = serializers.CharField(source='recipient.username', read_only=True)
    initiator_name = serializers.CharField(source='initiated_by.username', read_only=True)

    class Meta:
        model = Payout
        fields = [
            'id', 'amount', 'recipient', 'cashpool',
            'recipient_name', 'initiator_name',
            'status', 'transaction_ref', 'completed_at', 'failure_reason'
        ]
        read_only_fields = (
            'id', 'status', 'transaction_ref', 'completed_at', 
            'failure_reason', 'initiated_by'
        )
    def validate(self, data):
        cashpool = data.get('cashpool')
        if not cashpool:
            raise serializers.ValidationError({"cashpool": "Cashpool is required"})
            
        if cashpool.chama.chama_admin != self.context['request'].user:
            raise serializers.ValidationError(
                {"admin": "Only the chama admin can create payouts"}
            )
        return data
    
    def create(self, validated_data):
        validated_data['initiated_by'] = self.context['request'].user
        return super().create(validated_data)

"""
    This Serializer passes info to process the Payout;
    The Update method  ensure the cashpool balance is updated gracefully 
     while recording the transaction into the ledger.

"""
class ProcessPayoutSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=['approve', 'reject'])
    reason = serializers.CharField(required=False, allow_blank=True)
   
    def validate(self, data):
        payout = self.instance
        if not payout:
            raise serializers.ValidationError("Payout instance is required")
        
        if payout.status != 'pending':
            raise serializers.ValidationError("Only pending payouts can be processed")
        
        return data

    def update(self, instance, validated_data):
        action = validated_data.get('action')
        reason = validated_data.get('reason', '')
        
        try:
            with transaction.atomic():
                if action == 'approve':
                    instance.status = 'processing'
                    instance.save()
                    
                    # Generate fresh transaction_ref if not set
                    if not instance.transaction_ref:
                        instance.transaction_ref = instance.generate_transaction_ref()
                        instance.save()
                    
                    from transactions.services import LedgerService
                    LedgerService.record_payout(instance)

                    instance.status = 'completed'
                    instance.completed_at = timezone.now()
                    instance.save()

                elif action == 'reject':
                    instance.status = 'failed'
                    instance.failure_reason = reason
                    instance.save()

                return instance
                
        except Exception as e:
            logger.error(f"Error processing payout {instance.id}: {str(e)}")
            instance.status = 'failed'
            instance.failure_reason = str(e)
            instance.save()
            raise serializers.ValidationError(str(e))
           
"""
    This Serializer processes the Payout, pushes info to confirm a payout 

"""
class PayoutProcessResponseSerializer(serializers.ModelSerializer):
    recipient_name = serializers.CharField(source='recipient.username', read_only=True)
    initiator_name = serializers.CharField(source='initiated_by.username', read_only=True)

    class Meta:
        model = Payout
        fields = [
            'id', 'amount', 'status', 'transaction_ref',
            'completed_at', 'failure_reason',
            'recipient_name', 'initiator_name'
        ]
        read_only_fields = fields


