from .models import Chama, CashPool
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from contributions.models import Contribution
from django.contrib.auth import get_user_model


class ChamaSerializer(serializers.ModelSerializer):
    chama_admin = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(),
        required=False
    )

    class Meta:
        model = Chama
        fields = ('id', 'name', 'description', 'chama_admin', 'cash_pool', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at')  

    def validate(self, data):
        request = self.context.get('request')
        instance = self.instance
        
        if instance:
            if instance.chama_admin != request.user:
                raise serializers.ValidationError("Only the current admin can modify chama details")
            
            if 'chama_admin' in data and data['chama_admin'] not in instance.members.all():
                raise serializers.ValidationError("New admin must be a current member")
                
        return data

    def update(self, instance, validated_data):
        new_admin = validated_data.pop('chama_admin', None)
        
        if new_admin and new_admin != instance.chama_admin:

            if instance.chama_admin not in instance.members.all():
                instance.members.add(instance.chama_admin)
            instance.chama_admin = new_admin
        
        return super().update(instance, validated_data)

class CashPoolSerializer(serializers.ModelSerializer):
    chama_name = serializers.CharField(source='chama.name', read_only=True)
    
    class Meta:
        model = CashPool
        fields = ('id', 'chama', 'chama_name', 'balance', 'updated_at')
        read_only_fields = ('id', 'chama_name')

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



