from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
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
        return Response({"detail": serializer.errors}, status=HTTP_400_BAD_REQUEST)


class Me(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        내 정보
        GET /api/v1/users/me
        """

        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


class Login(APIView):
    def post(self, request):
        """
        로그인
        POST /api/v1/users/login
        """

        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError("Username or password is required.")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response({"status": True})
        return Response(
            {"detail": "Invalid user data."},
            status=HTTP_400_BAD_REQUEST,
        )


class Logout(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        로그아웃
        POST /api/v1/users/logout
        """
        logout(request)
        return Response({"status": True})
