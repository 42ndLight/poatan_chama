from rest_framework import serializers
from .models import Contribution
from django.utils import timezone
from django.db import transaction
from django.db.models import F

class ContributionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    chama = serializers.StringRelatedField()
    confirmed_by = serializers.StringRelatedField()
    
    class Meta:
        model = Contribution
        fields = ['id','amount', 'chama', 'status', 'confirmed_by', 'user'] 
        read_only_fields = ['user', 'chama', 'created_at', 'updated_at']
  
        

class ConfirmContributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contribution
        fields = ['is_confirmed', 'status', 'confirmed_by']
        read_only_fields = ['is_confirmed', 'confirmed_by']

    def update(self, instance, validated_data):
        with transaction.atomic():
            if not instance.is_confirmed:
                if not instance.transaction_ref:
                        instance.transaction_ref = instance.generate_transaction_ref()
                        instance.save()
                        
                instance.is_confirmed = True
                instance.status = 'confirmed'
                instance.confirmed_by = self.context['request'].user
                instance.completed_at = timezone.now()
                instance.save()

                cash_pool = instance.chama.cash_pool
                cash_pool.balance = F('balance') + instance.amount
                cash_pool.save(update_fields=['balance'])
                cash_pool.refresh_from_db()

        
            from transactions.services import LedgerService
            if not LedgerService.record_contribution(instance):
                if instance.is_confirmed:
                    return instance
                raise serializers.ValidationError("Failed to record ledger entry")  
            return instance