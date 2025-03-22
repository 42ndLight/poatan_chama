from .models import Chama
from rest_framework import serializers


class ChamaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chama
        fields = ('id', 'chama_name', 'description', 'chama_admin', 'cash_pool', 'created_at', 'updated_at')
        read_only_fields = ('id', 'chama_name', 'description', 'chama_admin', 'created_at', 'updated_at')

class RegisterChamaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chama
        fields = ('id', 'chama_name', 'description', 'chama_admin', 'cash_pool', 'created_at', 'updated_at')

    def create(self, validated_data):
        chama = Chama.objects.create_chama(**validated_data)
        return chama

