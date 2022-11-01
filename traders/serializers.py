from rest_framework import serializers

from traders.models import Trader


class DepositAndWithdrawal(serializers.ModelSerializer):
    class Meta:
        model = Trader
        fields = ["id", "is_deposit", "amount", "createdAt"]
