from rest_framework import serializers
from .models import Contribution

class ContributionSerializer(serializers.ModelSerializer):
    class Meta:
        models = Contribution
        fields = ["id", "user", "amount", "is_confirmed", "created_at"]
        read_only_fields = ["id", "user", "is_confirmed", "created_at"]

        def create(self, validated_data):
            validated_data["user"] = self.context["request"].user
            return super().create(validated_data)
        
        def update(self, instance, validated_data):
            instance.is_confirmed = validated_data.get('is_confirmed', instance.is_confirmed)
            instance.save()
            if instance.is_confirmed:
                instance.chama.cash_pool.update_balance()
            return instance
        
class ConfirmContributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contribution
        fields = ["is_confrimed"]

    def update(self, instance,  validated_data):
        instance.is_confirmed = True
        instance.save()
        return instance
    