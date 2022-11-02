from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Account, AccountOwner
from .serializers import AccountSerializer, AccountDetailSerializer


class AccountsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        유저가 보유하고 있는 계좌와 계좌 총 자산을 불러옵니다.
        GET api/v1/accounts/
        """

        user = request.user
        owner = AccountOwner.objects.filter(user=user)
        if not owner.exists():
            # TODO: 계좌 등록 페이지로 연결
            return Response({"message": "계좌 소유주로 등록되어 있지 않습니다."}, status=404)
        accounts = Account.objects.filter(owner=owner.first())
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)

class AccountsDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, account_number):
        """
        유저가 보유하고 있는 계좌의 투자 상세를 불러옵니다.
        GET api/v1/accounts/{account_number}
        """
        user = request.user
        owner = AccountOwner.objects.filter(user=user)
        accounts = Account.objects.filter(owner=owner.first(), number=account_number)
        serializer = AccountDetailSerializer(accounts, many=True)
        return Response(serializer.data)


