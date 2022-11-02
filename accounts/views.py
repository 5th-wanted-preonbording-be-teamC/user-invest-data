from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Account
from .serializers import AccountSerializer


class AccountsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        유저가 보유하고 있는 계좌와 계좌 총 자산을 불러옵니다.
        GET api/v1/accounts/
        """

        user = request.user
        accounts = Account.objects.filter(user=user)
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)
