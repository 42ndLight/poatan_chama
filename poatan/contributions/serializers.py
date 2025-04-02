from rest_framework import serializers
from .models import Contribution


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
        fields = ["is_confirmed"]
        read_only_fields = ["is_confirmed"]

    def update(self, instance, validated_data):
        instance.is_confirmed = True
        instance.status = 'confirmed'
        instance.save()
        
        return instance