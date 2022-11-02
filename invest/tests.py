from rest_framework.test import APITestCase
from users.models import User
from accounts.models import Account, AccountOwner
from accounts.serializers import AccountSerializer, AccountDetailSerializer
from assets.models import Asset, Group
from traders.models import Trader
from transactions.models import Transaction
from transactions.serializers import TransactionsByGroupSerializer


def set_api_url(user_pk=None, account_pk=None, assets=False):
    return (
        "/api/v1/invest/user/"
        + (f"{user_pk}/" if user_pk else "")
        + (f"account/{account_pk}/" if account_pk else "")
        + ("assets/" if assets else "")
    )


class TestInvest(APITestCase):
    def setUp(self):
        # Y___: 잡혀야 하는 ___
        # N___: 잡히지 않아야 하는 ___
        # 유저 생성
        self.Yuser = User.objects.create(username="Y")
        self.Nuser = User.objects.create(username="N")
        self.user_without_owner = User.objects.create(username="without_owner")
        # 증권사 생성
        self.trader = Trader.objects.create(name="trader")
        # 계좌 소유자 생성
        self.Yown = AccountOwner.objects.create(
            is_user=True, user=self.Yuser, name=self.Yuser.name
        )
        self.Nown = AccountOwner.objects.create(is_user=False, name="non-user")
        # 계좌 생성
        self.Yacc = Account.objects.create(
            name="test1",
            number="1234",
            trader=self.trader,
            owner=self.Yown,
            principal=100,
        )
        self.Nacc = Account.objects.create(
            name="test2",
            number="5678",
            trader=self.trader,
            owner=self.Yown,
            principal=100,
        )
        # 자산 그룹 생성
        Ygrp = Group.objects.create(name="채권 / 현금")
        Ngrp = Group.objects.create(name="전세계 주식")
        # 자산 생성
        self.Yass1 = Asset.objects.create(
            name="asset1",
            isin="isin1",
            group=Ygrp,
        )
        self.Yass2 = Asset.objects.create(
            name="asset2",
            isin="isin2",
            group=Ygrp,
        )
        self.Nass = Asset.objects.create(
            name="asset3",
            isin="isin3",
            group=Ngrp,
        )
        # 거래 생성
        self.transaction1 = Transaction.objects.create(
            price=1,
            amount=1,
            user=self.Yuser,
            asset=self.Yass1,
            account=self.Yacc,
        )
        self.transaction2 = Transaction.objects.create(
            price=2,
            amount=2,
            user=self.Yuser,
            asset=self.Yass2,
            account=self.Yacc,
        )
        self.transaction3 = Transaction.objects.create(
            price=4,
            amount=4,
            user=self.Yuser,
            asset=self.Nass,
            account=self.Yacc,
        )

    def test_redirect_user(self):
        # 로그인 사용자는 본인 ID를 이용하여 pk 리다이렉트
        self.client.force_login(self.Yuser)
        response = self.client.get(set_api_url())
        self.assertRedirects(response, set_api_url(self.Yuser.id))
        self.client.logout()

    def test_invest(self):
        # 로그인 사용자와 pk가 일치하는 경우 200
        self.client.force_login(self.Yuser)
        response = self.client.get(set_api_url(self.Yuser.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0], AccountSerializer(self.Yacc).data)
        self.client.logout()
        # 로그인 사용자와 pk가 불일치하는 경우 403
        self.client.force_login(self.Nuser)
        response = self.client.get(set_api_url(self.Yuser.id))
        self.assertEqual(response.status_code, 403)
        self.client.logout()
        # 계좌 소유자가 아닌 사용자의 경우 404
        self.client.force_login(self.user_without_owner)
        response = self.client.get(set_api_url(self.user_without_owner.id))
        self.assertEqual(response.status_code, 404)

    def test_invests_detail(self):
        # 로그인 사용자가 소유한 계좌를 요청했을 경우 200
        self.client.force_login(self.Yuser)
        response = self.client.get(set_api_url(self.Yuser.id, self.Yacc.number))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, AccountDetailSerializer(self.Yacc).data)
        self.client.logout()
        # 로그인 사용자가 소유하지 않은 계좌를 요청했을 경우 404
        self.client.force_login(self.Nuser)
        response = self.client.get(set_api_url(self.Nuser.id, self.Yacc.number))
        self.assertEqual(response.status_code, 404)
        self.client.logout()

    def test_invest_transactions_view(self):
        # 로그인 사용자가 소유한 계좌의 자산을 요청했을 경우 200
        self.client.force_login(self.Yuser)
        response = self.client.get(set_api_url(self.Yuser.id, self.Yacc.number, True))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            TransactionsByGroupSerializer(
                Transaction.objects.filter(account=self.Yacc),
            ).data,
        )
