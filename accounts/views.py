from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.exceptions import ParseError, NotFound
from .models import Account, AccountOwner, Transfer
from transactions.models import Transaction
from assets.models import Asset
from users.models import User
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


class AccountTransferResultView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Phase 1에서 등록한 거래 정보를 검증 후 실제 고객의 자산을 업데이트합니다.
        POST api/v1/accounts/transfer/result/
        """

        signature = request.data.get("signature")
        transfer_identifier = request.data.get("transfer_identifier")

        if not signature or not transfer_identifier:
            raise ParseError(detail="signature 또는 transfer_identifier는 필수입니다.")

        # signature 검증
        transfer = get_object_or_404(Transfer, pk=transfer_identifier)
        hash = transfer.get_hash()
        if hash != signature:
            raise ParseError(detail="일치하는 signature를 찾을 수 없습니다.")

        try:
            # 계좌 검색 후 원금 추가
            account = Account.objects.get(
                number=transfer.account_number, owner__name=transfer.user_name
            )
            account.principal += transfer.transfer_amount
            account.save()

            # 자산 추가
            user = User.objects.get(name=transfer.user_name)
            asset = Asset.objects.get(group__name="채권 / 현금")
            Transaction.objects.create(
                price=1,
                amount=transfer.transfer_amount,
                user=user,
                asset=asset,
                account=account,
            )
            return Response({"status": True})
        except Account.DoesNotExist:
            raise NotFound(detail="일치하는 계좌가 존재하지 않습니다.")
        except User.DoesNotExist:
            raise NotFound(detail="일치하는 유저가 존재하지 않습니다.")
        except Asset.DoesNotExist:
            raise NotFound(detail="일치하는 자산이 존재하지 않습니다.")
