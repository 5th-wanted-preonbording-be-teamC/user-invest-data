from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from accounts.models import Account, AccountOwner
from accounts.serializers import AccountSerializer, AccountDetailSerializer
from transactions.models import Transaction
from transactions.serializers import TransactionsByGroupSerializer


class ErRes:
    @staticmethod
    def data_status(msg, status):
        return {"data": {"message": msg}, "status": status}

    USER_ID_NOT_MATCH_WITH_USER_PK = data_status("권한이 없습니다.", 403)
    # 사용자의 아이디와 사용자가 요청한 API의 user_pk가 일치하지 않을 때
    USER_CONNECTED_NO_ACCOUNTOWNER = data_status("계좌 소유주로 등록되어 있지 않습니다.", 404)
    # 요청한 사용자에게 연결된 계좌 소유자가 없을 때

    @staticmethod
    def USER_DONT_HAVE_THE_ACCOUNT(name, account):
        # 사용자가 조회할 수 없는 계좌를 요청했을 때
        return ErRes.data_status(
            f"{name} 님의 {account} 계좌를 조회할 수 없습니다.",
            404,
            # 403이 아닌 이유: 계좌가 존재할 때 403을 리턴하면
            # 계좌가 존재하지 간접적으로 정보가 노출된다.
            # 이를 방지하기 위해 본인의 계좌 이외의 계좌를 요청하면 항상 404를 리턴한다.
        )


class InvestsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_pk):
        """
        투자 화면API

        Request:
        GET /api/v1/invest/user/<int:user_pk>/

        Response:
        [
            {
                'name': 계좌명,
                'trader': 증권사,
                'number': 계좌번호,
                'total_profit': 계좌 총 자산,
            },
            ...
        ]
        """

        user = request.user
        if user.id != user_pk:
            return Response(**ErRes.USER_ID_NOT_MATCH_WITH_USER_PK)
        owner = AccountOwner.objects.filter(user=user)
        if not owner.exists():
            # TODO: 계좌 등록 페이지로 연결
            return Response(**ErRes.USER_CONNECTED_NO_ACCOUNTOWNER)
        accounts = Account.objects.filter(owner=owner.first())
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)


class RedirectToSelfView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        GET /api/v1/invest/user/
        본인의 투자 화면(/api/v1/invest/user/<int:user_pk>/)으로 redirect
        """

        return HttpResponseRedirect(f"/api/v1/invest/user/{request.user.id}/")


class InvestDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_pk, account_pk):
        """
        투자 상세 화면 API
        Request:
        GET /api/v1/invest/user/<int:user_pk>/account/<int:account_pk>/

        Response:
        {
            'name': 계좌명,
            'trader': 증권사ID,
            'number': 계좌번호,
            'total_assets': 계좌 총 자산,
            'principal': 투자 원금,
            'total_profit': 총 수익금,
            'profit_rate': 수익률
        }
        """

        user = request.user
        if user.id != user_pk:
            return Response(**ErRes.USER_ID_NOT_MATCH_WITH_USER_PK)
        filtered_owner = AccountOwner.objects.filter(user=user)
        if not filtered_owner.exists():
            # TODO: 계좌 등록 페이지로 연결
            return Response(**ErRes.USER_CONNECTED_NO_ACCOUNTOWNER)
        owner = filtered_owner.first()
        filtered_account = Account.objects.filter(
            owner=owner,
            number=account_pk,
        )
        if not filtered_account.exists():
            return Response(**ErRes.USER_DONT_HAVE_THE_ACCOUNT(owner.name, account_pk))
        account = filtered_account.first()
        serializer = AccountDetailSerializer(account)
        return Response(serializer.data)


class InvestTransactionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_pk, account_pk):
        """
        보유종목 화면 API
        Request:
        GET /api/v1/invest/user/<int:user_pk>/account/<int:account_pk>/assets

        Response:
        {
            보유 종목의 자산군:
            [
                {
                    'asset_name': 보유 종목명,
                    'asset_price': 보유 종목의 평가 금액 (종목 보유 수량 * 종목 현재가),
                    'asset_isin': 보유 종목 ISIN,
                },
                ...
            ]
            , ...
        }
        """

        user = request.user
        if user.id != user_pk:
            return Response(**ErRes.USER_ID_NOT_MATCH_WITH_USER_PK)
        filtered_owner = AccountOwner.objects.filter(user=user)
        if not filtered_owner.exists():
            # TODO: 계좌 등록 페이지로 연결
            return Response(**ErRes.USER_CONNECTED_NO_ACCOUNTOWNER)
        owner = filtered_owner.first()
        filtered_account = Account.objects.filter(
            owner=owner,
            number=account_pk,
        )
        if not filtered_account.exists():
            return Response(**ErRes.USER_DONT_HAVE_THE_ACCOUNT(owner.name, account_pk))
        account = filtered_account.first()
        transactions = Transaction.objects.filter(account=account)
        serializer = TransactionsByGroupSerializer(
            transactions,
        )
        return Response(serializer.data)
