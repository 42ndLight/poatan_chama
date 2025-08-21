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
        read_only_fields = ['id','user', 'chama', 'created_at', 'updated_at']
  
        
"""
    This Serializer passes info to confirm the contribution.
    The Update method  ensure the cashpool balance is updated gracefully 
     while recording the transaction into the ledger.

"""
