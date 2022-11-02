from rest_framework.views import APIView, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from django.http import HttpResponseRedirect
from accounts.models import Account
from accounts.serializers import AccountSerializer


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
            accounts = Account.objects.filter(user=user)
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
