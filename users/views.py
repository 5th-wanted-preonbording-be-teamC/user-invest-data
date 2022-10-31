from rest_framework.views import APIView


class Me(APIView):
    def get(self, request):
        """
        내 정보
        GET /api/v1/users/me
        """
        pass


class Users(APIView):
    def post(self, request):
        """
        회원가입
        POST /api/v1/users
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
