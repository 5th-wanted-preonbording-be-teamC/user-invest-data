from django.db.models import QuerySet
from rest_framework import serializers
from transactions.models import Transaction
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    total_assets = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ("number", "name", "total_assets")

    def get_total_assets(self, obj):
        transactions = obj.transactions.all()
        return sum(transaction.asset_price() for transaction in transactions)


class AccountDetailSerializer(serializers.ModelSerializer):
    total_assets = serializers.SerializerMethodField()
    total_profit = serializers.SerializerMethodField()
    profit_rate = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = (
            "name",
            "trader",
            "number",
            "total_assets",
            "principal",
            "total_profit",
            "profit_rate",
        )

    def get_total_assets(self, obj: Account) -> int:
        transactions: QuerySet[Transaction] = obj.transactions.all()
        return sum(transaction.asset_price() for transaction in transactions)

    def get_total_profit(self, obj: Account) -> int:
        return self.get_total_assets(obj) - obj.principal

    def get_profit_rate(self, obj: Account) -> float:
        return self.get_total_profit(obj) / obj.principal * 100
