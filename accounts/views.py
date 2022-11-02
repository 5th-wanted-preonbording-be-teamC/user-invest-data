from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from .models import Account, AccountOwner
from .serializers import AccountSerializer, TransferSerializer


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


class AccountTransferView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        입금 거래 정보들을 서버에 등록합니다.(Phase 1)
        POST api/v1/accounts/transfer/
        """

        serializer = TransferSerializer(data=request.data)
        if serializer.is_valid():
            transfer = serializer.save()
            return Response({"transfer_identifier": transfer.id})
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
