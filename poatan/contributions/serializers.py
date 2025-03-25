from rest_framework import serializers
from .models import Contribution

class ContributionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    chama = serializers.StringRelatedField()
    confirmed_by = serializers.StringRelatedField()
    
    class Meta:
        model = Contribution
        fields = '__all__'
        read_only_fields = ('status', 'created_at', 'updated_at')

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
    
    

class ConfirmContributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contribution
        fields = ["is_confirmed"] 

    def update(self, instance, validated_data):
        instance.is_confirmed = validated_data.get('is_confirmed', instance.is_confirmed)
        instance.save()
        if instance.is_confirmed:
            instance.chama.cash_pool.update_balance()
        return instance