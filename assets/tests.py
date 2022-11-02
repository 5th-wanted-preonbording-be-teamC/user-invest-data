from rest_framework.test import APITestCase
from users.models import User


class TestAssetsGroups(APITestCase):
    def test_assets_groups(self):
        """
        유저가 보유한 자산의 자산군 목록 테스트
        GET api/v1/assets/groups/
        """

        response = self.client.get("/api/v1/assets/groups/")
        data = response.json()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            data["detail"], "Authentication credentials were not provided."
        )

        user = User.objects.create(username="test")
        self.client.force_login(user)

        response = self.client.get("/api/v1/accounts/")
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
