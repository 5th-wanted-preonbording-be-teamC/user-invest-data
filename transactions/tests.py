from rest_framework.test import APITestCase
from users.models import User


class TestTransactions(APITestCase):
    def test_transactions(self):
        """
        유저가 보유한 자산 API 테스트
        GET api/v1/transactions/?group_id={id}
        """

        response = self.client.get("/api/v1/transactions/")
        data = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            data["detail"], "Authentication credentials were not provided."
        )

        user = User.objects.create(username="test")
        self.client.force_login(user)

        response = self.client.get("/api/v1/transactions/")
        data = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data["detail"], "group_id는 필수입니다.")

        response = self.client.get("/api/v1/transactions/?group_id=1")
        data = response.json()

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)
