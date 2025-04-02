from rest_framework import serializers
from .models import Payout, PayoutCycle
from cashpool.models import CashPool

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
    action = serializers.ChoiceField(choices=['approve', 'rejected'])
    reason = serializers.CharField(required=False, allow_blank=True)

