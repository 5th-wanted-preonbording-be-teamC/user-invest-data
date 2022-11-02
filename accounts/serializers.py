from rest_framework import serializers
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    total_assets = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ("number", "name", "total_assets")

    def get_total_assets(self, obj):
        transactions = obj.transactions.all()
        return sum(transaction.asset_price() for transaction in transactions)


class AccountDetailSerializer(AccountSerializer):
    trader_name = serializers.CharField(source='trader.name')
    total_profits = serializers.SerializerMethodField()
    assets_yield = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ("name", "trader_name", "number", "total_assets", "principal", "total_profits", "assets_yield")

    def get_total_profits(self, obj):
        return self.get_total_assets(obj) - obj.principal
    def get_assets_yield(self, obj):
        return round(self.get_total_profits(obj) / obj.principal * 100, 2)