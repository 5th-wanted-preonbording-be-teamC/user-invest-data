from django.db.models import Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Account
from traders import serializers


class DepositAndWithdrawal(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """
        입/출금 내역 목록
        GET /api/v1/traders/{pk}/
        """
        user = request.user
        q = Q()
        if pk:
            q &= Q(pk=pk)
        if user:
            q & Q(user=user)

        trader = Trader.objects.filter(q).order_by("createdAt")
        serializer = serializers.DepositAndWithdrawal(trader)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TraderList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        사용자가 가지고 있는증권사 목록
        GET /api/v1/traders/
        """
        user = request.user
        accounts = set(Account.objects.get(user=user))
        serializer = serializers.TraderListSerializer(accounts)

        return Response(serializer.data, status=status.HTTP_200_OK)
