from rest_framework import serializers

from traders.models import Trader


class TradersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trader
        fields = ['id', 'company']