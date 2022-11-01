from rest_framework import serializers

from accounts.models import Account
from traders.models import Trader


class DepositAndWithdrawal(serializers.ModelSerializer):
    class Meta:
        model = Trader
        fields = ["id", "is_deposit", "amount", "createdAt"]


class TraderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["trader_id", "number", "principal"]
