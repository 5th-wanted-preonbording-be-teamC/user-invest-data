from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from .models import Transaction
from .serializers import TransactionSerializer


class TransactionsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        유저가 보유한 해당 섹터의 자산을 불러온다.
        GET api/v1/transactions/?group_id={id}
        """

        user = request.user
        group_id = request.query_params.get("group_id")

        if not group_id:
            raise ParseError("group_id는 필수입니다.")

        transactions = Transaction.objects.filter(asset__group__id=group_id, user=user)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
