from .models import Chama, CashPool
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

'''A serializer to process info on a chama'''
'''Modifying chama_admin to ensure  the creator of a chama is the admin'''
'''Formating the CashPool balance from its model'''
class ChamaSerializer(serializers.ModelSerializer):
    chama_admin = serializers.PrimaryKeyRelatedField(
        queryset=get_user_model().objects.all(),
        required=False
    )
    cash_pool_balance = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        source='cash_pool.balance',
        read_only=True
    )

    class Meta:
        model = Chama
        fields = ('id', 'name', 'description', 'chama_admin', 'cash_pool_balance', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'cash_pool_balance')  

    '''Logic to create a new chama when data is validated'''
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

    '''Validation Checks to ensure the person requesting the creation is an Admin'''
    def validate(self, data):
        request = self.context.get('request')
        instance = self.instance
        
        if instance:
            if instance.chama_admin != request.user:
                raise serializers.ValidationError("Only the current admin can modify chama details")
            
            if 'chama_admin' in data and data['chama_admin'] not in instance.members.all():
                raise serializers.ValidationError("New admin must be a current member")
                
        return data

    '''Allows admin to promote user roles '''
    def update(self, instance, validated_data):
        new_admin = validated_data.pop('chama_admin', None)
        
        if new_admin and new_admin != instance.chama_admin:

            if instance.chama_admin not in instance.members.all():
                instance.members.add(instance.chama_admin)
            instance.chama_admin = new_admin
        
        return super().update(instance, validated_data)

'''A serializer to pass info related to a chama's cashpool'''
class CashPoolSerializer(serializers.ModelSerializer):
    chama_name = serializers.CharField(source='chama.name', read_only=True)
    
    class Meta:
        model = CashPool
        fields = ('id', 'chama', 'chama_name', 'balance', 'updated_at')
        read_only_fields = ('id', 'chama_name')

'''A serializer to pass info when registering a chama'''
class RegisterChamaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chama
        fields = ('name', 'description', 'chama_admin')

"""
A serializer for users to join a chama
Handles:
    -Chama existence validation before joining
    -User can join a chama
    
"""
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
    
"""Serializer handles Chama Membership"""
class ChamaMemberSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()

    class Meta:
        model = Chama
        fields = ('id', 'name', 'members')
    # Shows chama members
    def get_members(self, obj):
        return [{"username": user.username, "role": user.role} for user in obj.members.all()]



