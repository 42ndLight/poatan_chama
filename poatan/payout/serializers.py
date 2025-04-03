from rest_framework import serializers
from .models import Payout, PayoutCycle
from cashpool.models import CashPool
from django.db import transaction
from django.db.models import F


class PayoutCycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayoutCycle
        fields = '__all__'
        read_only_fields = ('end_date',)

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

class ProcessPayoutSerializer(serializers.Serializer):    
    action = serializers.ChoiceField(choices=['approve', 'reject'])
    reason = serializers.CharField(required=False, allow_blank=True)
    transaction_ref = serializers.CharField(required=False)

    def validate(self, data):
        payout = self.context.get('payout')
        if not payout:
            raise serializers.ValidationError("Payout instance is required")
        return data

    def update(self, instance, validated_data):
        action = validated_data.get('action')
        reason = validated_data.get('reason', '')
        transaction_ref = validated_data.get('transaction_ref')

        with transaction.atomic():
            if action == 'approve':
                if instance.status != 'pending':
                    raise serializers.ValidationError(
                        "Only pending payouts can be approved"
                    )
                if not instance.process(transaction_ref):
                    raise serializers.ValidationError(
                        "Payout processing failed. Check logs for details."
                    )
                cash_pool = instance.chama.cash_pool
                cash_pool.balance = F('balance') - instance.amount
                cash_pool.save(update_fields=['balance'])
                cash_pool.refresh_from_db()
        
            elif action == 'reject':
                instance.status = 'failed'
                instance.failure_reason = reason
                instance.save()
            return instance
    


