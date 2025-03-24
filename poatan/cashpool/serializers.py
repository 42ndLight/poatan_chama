from .models import Chama, CashPool
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from contributions.models import Contribution


class ChamaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chama
        fields = ('id', 'name', 'description', 'chama_admin', 'cash_pool', 'created_at', 'updated_at')
        read_only_fields = ('id', 'chama_admin', 'created_at', 'updated_at')

class CashPoolSerializer(serializers.ModelSerializer):
    chama_name = serializers.CharField(source='chama.name', read_only=True)
    
    class Meta:
        model = CashPool
        fields = ('id', 'chama', 'chama_name', 'balance', 'updated_at')
        read_only_fields = ('id', 'chama_name', 'updated_at')

class RegisterChamaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chama
        fields = ('name', 'description', 'chama_admin')


class JoinChamaSerializer(serializers.Serializer):
    chama_id = serializers.IntegerField()

    def validate_chama_id(self, value):
        chama = get_object_or_404(Chama, id=value)
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        chama = Chama.objects.get(id=self.validated_data['chama_id'])
        
        # Check if user is already a member
        if chama.members.filter(id=user.id).exists():
            raise serializers.ValidationError("You are already a member of this chama")
            
        # Add user to chama members (many-to-many relationship)
        chama.members.add(user)
        return {
            "user": user,
            "chama": chama
        }

class ChamaMemberSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()

    class Meta:
        model = Chama
        fields = ('id', 'name', 'members')

    def get_members(self, obj):
        return [{"username": user.username, "role": user.role} for user in obj.members.all()]



