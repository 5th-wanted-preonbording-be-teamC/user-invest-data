from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from traders import serializers
from traders.models import Trader


class TradersView(APIView):
    def get(self, request):
        traders = Trader.objects.all()
        serializer = serializers.TredersSerializer(traders)
        return Response(serializer.data, status=status.HTTP_200_OK)
