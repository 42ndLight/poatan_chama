from rest_framework import serializers
from .models import Payout, PayoutCycle

class PayoutCycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayoutCycle
        fields = '__all__'
        read_only_fields = ('end_date',)

class PayoutSerializer(serializers.ModelSerializer):
    recipient_name = serializers.CharField(source='recipient.username', read_only=True)
    initiator_name = serializers.CharField(source='initiated_by.username', read_only=True)
    cashpool_name = serializers.CharField(source='cashpool.chama.name', read_only=True)

    class Meta:
        model = Payout
        fields = '__all__'
        read_only_fields = ('status', 'transaction_ref', 'completed_at', 'failure_reason', 'initiated_by')

class ProcessPayoutSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=['approve', 'rejected'])
    reason = serializers.CharField(required=False)

