from .models import Chama, CashPool
from rest_framework import serializers
from contributions.models import Contribution


class ChamaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chama
        fields = ('id', 'chama_name', 'description', 'chama_admin', 'cash_pool', 'created_at', 'updated_at')
        read_only_fields = ('id', 'chama_admin', 'created_at', 'updated_at')

class CashPoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashPool
        fields = ('chama', 'balance')

class RegisterChamaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chama
        fields = ('id', 'chama_name', 'description', 'chama_admin', 'cash_pool', 'created_at', 'updated_at')

    def create(self, validated_data):
        chama = Chama.objects.create_chama(**validated_data)
        return chama
    

class JoinChamaSerializer(serializers.Serializer):
    chama_id = serializers.IntegerField()

    def save(self, **kwargs):
        user = self.context['request'].user
        chama = Chama.objects.get(id=self.validated_data['chama_id'])
        user.chama = chama
        user.save()
        return user

class ChamaMemberSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()

    class Meta:
        model = Chama
        fields = ('id', 'chama_name', 'members')

    def get_members(self, obj):
        return [{"username": user.username, "role": user.role} for user in obj.members.all()]



