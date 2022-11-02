from rest_framework.test import APITestCase
from .models import AccountOwner
from users.models import User


class TestAccounts(APITestCase):
    def test_accounts(self):
        """
        유저가 보유한 계좌의 총 자산 테스트
        GET api/v1/accounts/
        """

        # 비로그인 상태 요청
        response = self.client.get("/api/v1/accounts/")
        data = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            data["detail"], "Authentication credentials were not provided."
        )

        # 유저 생성 및 로그인 상태 요청(계좌 소유자로 등록되어 있지 않은 경우)
        user = User.objects.create(username="test")
        self.client.force_login(user)
        response = self.client.get("/api/v1/accounts/")
        data = response.json()
        self.assertEqual(response.status_code, 404)

        # 계좌 소유주 생성 후 요청
        AccountOwner.objects.get_or_create(
            is_user=True,
            name=user.name,
            user=user,
        )
        response = self.client.get("/api/v1/accounts/")
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
