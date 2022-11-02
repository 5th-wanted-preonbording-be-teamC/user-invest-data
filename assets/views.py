from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Group
from transactions.models import Transaction
from .serializers import GroupSerializer


class AssetsGroupView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        유저가 보유한 종목의 섹션 목록을 불러옵니다.
        GET api/v1/assets/group/
        """

        user = request.user
        groups_id = (
            Transaction.objects.filter(user=user)
            .values_list("asset__group__id", flat=True)
            .distinct()
        )
        groups = Group.objects.filter(id__in=groups_id)
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)
