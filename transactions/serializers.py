from django.db.models import QuerySet
from rest_framework import serializers
from .models import Transaction
from assets.models import Group


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
        return obj.asset_price()

    def get_asset_isin(self, obj):
        return obj.asset.isin


class TransactionsByGroupSerializer(serializers.ListSerializer):
    child = TransactionSerializer()

    def to_representation(self, data: QuerySet[Transaction]):
        groups = Group.objects.all()
        bygroup = {group: [] for group in groups}

        for transaction in data:
            group = transaction.asset.group
            bygroup[group].append(transaction)
        return [
            {
                group.name: TransactionSerializer(
                    transactions,
                    many=True,
                ).data
                for group, transactions in bygroup.items()
                if transactions
            }
        ]
