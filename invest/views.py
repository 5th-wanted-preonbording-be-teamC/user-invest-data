from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from django.http import HttpResponseRedirect
from accounts.models import Account, AccountOwner
from accounts.serializers import AccountSerializer, AccountDetailSerializer


class InvestsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """
        GET /api/v1/invest/user/<int:pk>/

        투자 화면
        - 계좌명
        - 증권사
        - 계좌번호
        - 계좌 총 자산
        """

        user = request.user
        if user.id == pk:
            owner = AccountOwner.objects.filter(user=user)
            if not owner.exists():
                # TODO: 계좌 등록 페이지로 연결
                return Response({"message": "계좌 소유주로 등록되어 있지 않습니다."}, status=404)
            accounts = Account.objects.filter(owner=owner.first())
            serializer = AccountSerializer(accounts, many=True)
            return Response(serializer.data)
        return Response(HTTP_400_BAD_REQUEST)


class RedirectToSelfView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        GET /api/v1/invest/user/
        본인의 투자 화면으로 redirect
        """

        return HttpResponseRedirect(f"/api/v1/invest/users/{request.user.id}/")


class InvestDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_pk, account_pk):
        """
        GET /api/v1/invest/user/<int:user_pk>/account/<int:account_pk>/

        투자 상세 화면
        - 계좌명
        - 증권사
        - 계좌번호
        - 계좌 총 자산
        - 투자 원금
        - 총 수익금 (총 자산 - 투자 원금)
        - 수익률 (총 수익금 / 투자 원금 * 100)
        """

        user = request.user
        if user.id != user_pk:
            return Response(HTTP_400_BAD_REQUEST)
        filtered_owner = AccountOwner.objects.filter(user=user)
        if not filtered_owner.exists():
            # TODO: 계좌 등록 페이지로 연결
            return Response({"message": "계좌 소유주로 등록되어 있지 않습니다."}, status=404)
        owner = filtered_owner.first()
        filtered_account = Account.objects.filter(
            owner=owner,
            number=account_pk,
        )
        if not filtered_account.exists():
            return Response(
                {"message": "{owner.name} 님의 {account_pk} 계좌를 조회할 수 없습니다."},
                status=404,
            )
        serializer = AccountDetailSerializer(filtered_account, many=True)
        return Response(serializer.data)
