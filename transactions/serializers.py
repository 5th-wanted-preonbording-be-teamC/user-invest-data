from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    asset_name = serializers.SerializerMethodField()
    asset_price = serializers.SerializerMethodField()
    asset_isin = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ("asset_name", "asset_price", "asset_isin")

    def get_asset_name(self, obj):
        return obj.asset.name

    def get_asset_price(self, obj):
        return obj.price * obj.amount

    def get_asset_isin(self, obj):
        return obj.asset.isin
