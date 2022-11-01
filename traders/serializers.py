from rest_framework import serializers


class DepositAndWithdrawal(serializers.ModelSerializer):
    class Meta:
        model = Trader
        fields = ['id', 'is_deposit', 'amount', 'createdAt']
