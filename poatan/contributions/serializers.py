from rest_framework import serializers
from .models import Contribution
from django.utils import timezone
from django.db import transaction
from django.db.models import F

"""
    A serializer for Contribution data when perfoming CRUD operations on the Contribution
    The Contribution can only be Created and Read
"""
class ContributionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    chama = serializers.StringRelatedField()
    confirmed_by = serializers.StringRelatedField()
    
    class Meta:
        model = Contribution
        fields = ['id','amount', 'chama', 'status', 'confirmed_by', 'user'] 
        read_only_fields = ['user', 'chama', 'created_at', 'updated_at']
  
        
"""
    This Serializer passes info to confirm the contribution.
    The Update method  ensure the cashpool balance is updated gracefully 
     while recording the transaction into the ledger.

"""
class ConfirmContributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contribution
        fields = ['status', 'confirmed_by']
        read_only_fields = ['confirmed_by']

    def validate(self, data):
        if self.instance.status != 'pending':
            raise serializers.ValidationError(
                "Only pending contributions can be confirmed"
            )
        return data

    def update(self, instance, validated_data):
        with transaction.atomic():
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
            
            #Recording the contribution on the ledger
            from transactions.services import LedgerService
            if not LedgerService.record_contribution(instance):
                if instance.is_confirmed:
                    return instance
                raise serializers.ValidationError("Failed to record ledger entry")  
            return instance