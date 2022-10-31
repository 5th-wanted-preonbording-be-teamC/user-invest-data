from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from .serializers import UserSerializer


class Users(APIView):
    def post(self, request):
        """
        회원가입
        POST /api/v1/users
        """

        password = request.data.get("password")
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class Me(APIView):
    def get(self, request):
        """
        내 정보
        GET /api/v1/users/me
        """
        pass


class Login(APIView):
    def post(self, request):
        """
        로그인
        POST /api/v1/users/login
        """
        pass


class Logout(APIView):
    def post(self, request):
        """
        로그아웃
        POST /api/v1/users/logout
        """
        pass
