from rest_framework import serializers
from .models import LedgerEntry
from users.serializers import UserSerializer  
from cashpool.serializers import ChamaSerializer
from rest_framework import serializers

class LedgerEntrySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    chama = ChamaSerializer(read_only=True)
    initiated_by = UserSerializer(read_only=True)

    class Meta:
        model = LedgerEntry
        fields = '__all__'
        read_ony_fields = [
            'id',
            'transaction_id',
            'timestamp',
            'initiated_by'
        ]

    def validate(self, data):
        transaction_type = data.get('transaction_type')
        entry_type = data.get('entry_type')
        account = data.get('account')

        valid_accounts = {
            'contribution' : ['cashpool', 'member_equity'],
            'payout' : ['cashpool', 'member_equity'],
            'adjustment' : ['cashpool', 'adjustment']
        }

        if transaction_type not in valid_accounts:
            raise serializers.ValidationError('Invalid Transaction Type')
        if account not in valid_accounts[transaction_type]:
            raise serializers.ValidationError(f"Account {account} not valid for {transaction_type} transactios")

        return data
    
class LedgerFilterSerializer(serializers.Serializer):
    chama = serializers.IntegerField(required=False)
    user = serializers.IntegerField(required=False)
    transaction_type = serializers.ChoiceField(
        choices=LedgerEntry.TRANSACTION_TYPES, 
        required=False
    )
    entry_type = serializers.ChoiceField(
        choices=LedgerEntry.ENTRY_TYPES,
        required=False
    )
    start_date = serializers.DateTimeField(required=False)
    end_date = serializers.DateTimeField(required=False)
    account = serializers.CharField(required=False)

    def validate(self, data):
        if data.get('start_date') and data.get('end_date'):
            if data['start_date'] > data['end_date']:
                raise serializers.ValidationError(
                    "End date must be after start date"
                )
        return data


class BalanceSerializer(serializers.Serializer):
    user = serializers.IntegerField()
    username = serializers.CharField(source='user__username')
    total_debits = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_credits = serializers.DecimalField(max_digits=12, decimal_places=2)
    balance = serializers.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        fields = [
            'user',
            'username',
            'total_debits',
            'total_credits',
            'balance'
        ]