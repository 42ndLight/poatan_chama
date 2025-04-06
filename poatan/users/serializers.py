from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.db.models import Sum
from payout.models import Payout
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password

User = get_user_model() #importng from Global user model

""" 
    A serializer to pass info relevant to user
    Defining Contribution stats and Payout Stats to show user 
    their current status at one time done 
    via methods get_payout_stats or get_contributions_stats

"""
class UserSerializer(serializers.ModelSerializer):
    contribution_stats = serializers.SerializerMethodField()
    payout_stats = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 
                  'last_name', 'is_staff', 'is_active', 
                  'date_joined', 'contribution_stats', 'payout_stats']

    def get_contribution_stats(self, obj):
        contributions = obj.contributions.all()
        return {
            'count': contributions.count(),
            'total_amount': contributions.aggregate(total=Sum('amount'))['total'] or 0
        }

    def get_payout_stats(self, obj):
        payouts = Payout.objects.filter(recipient=obj)
        return {
            'count': payouts.count(),
            'total_amount': payouts.aggregate(total=Sum('amount'))['total'] or 0
        }
"""
    This Serializer to parse info to create a new user
"""

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone_no', 'role', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
"""
    This Serializer to parse info to login a user
    It uses JWT tokens to provide authorization and authentication for users
"""
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        from django.contrib.auth import authenticate

        user = authenticate(**data)
        if not user:
            raise serializers.ValidationError("Invalid USER credentials")
        
        refresh = RefreshToken.for_user(user)
        return{
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user' : UserSerializer(user).data
            }

"""
    This Serializer to parse info to update a user profile
    A user can change their username, email and phone number
"""  
class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_no', 'role']

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_no = validated_data.get('phone_no', instance.phone_no)
        instance.role = validated_data.get('role', instance.role)
        instance.save()
        return instance

"""
    This Serializer to parse info to allow a user to change their accounts password
    The payload should contain the old password and newpassword confirmed twice to change the password
"""
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    confirm_password = serializers.CharField(required=True)
    
    # Method to  ensure old password is correct
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect")
        return value
    
    def validate(self, data):
        """Ensure new_password and confirm_password match."""
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match"})
        return data
    
    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance

"""
    This Serializer to parse info to allow a user to delete their profile
    The User should pass their password to successfully delete tjeir profile
""" 
class UserDeleteSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['password']
    # Method to compare passwords
    def validate_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Password is incorrect")
        return value
    
    # Method to delete user instance
    def delete(self, instance):
        instance.delete()
        return instance