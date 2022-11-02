from rest_framework import serializers
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    total_assets = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ("number", "name", "total_assets")

    def get_total_assets(self, obj):
        total_assets = 0
        total_assets += obj.principal
        transactions = obj.transactions.all()
        for transaction in transactions:
            total_assets += transaction.asset_price()
        return total_assets
