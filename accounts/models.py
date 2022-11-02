import hashlib
from django.db import models
from traders.models import Trader
from users.models import User


class Transfer(models.Model):
    account_number = models.CharField(max_length=80, verbose_name="계좌번호")
    user_name = models.CharField(max_length=80, verbose_name="유저명")
    transfer_amount = models.PositiveIntegerField(verbose_name="거래금액")

    def __str__(self):
        return f"{self.user_name}의 {self.account_number} 계좌 {self.transfer_amount} 입금"

    def get_hash(transfer):
        hash_string = (
            f"{transfer.account_number}{transfer.user_name}{transfer.transfer_amount}"
        )
        return hashlib.sha512(hash_string.encode("utf-8")).hexdigest()


class AccountOwner(models.Model):
    """
    계좌 소유자
    계좌가 존재할 때, 계좌 소유자는 반드시 존재해야 한다.
    하지만 계좌 소유자가 서비스 사용자라는 보장은 없다.
    따라서 계좌 소유자는 서비스 사용자와는 별도로 관리한다.
    """

    is_user = models.BooleanField(default=False)
    name = models.CharField(max_length=150, verbose_name="이름")
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Account(models.Model):
    number: models.CharField = models.CharField(
        max_length=20,
        primary_key=True,
        verbose_name="계좌번호",
    )
    name: models.CharField = models.CharField(
        max_length=150,
        verbose_name="계좌명",
        null=True,
    )
    owner: models.ForeignKey = models.ForeignKey(
        AccountOwner,
        on_delete=models.CASCADE,
        verbose_name="계좌주",
    )
    trader: models.ForeignKey = models.ForeignKey(
        Trader,
        on_delete=models.CASCADE,
        verbose_name="증권사",
    )
    principal: models.PositiveBigIntegerField = models.PositiveBigIntegerField(
        verbose_name="투자원금",
    )

    def __str__(self) -> str:
        return f"{self.owner}의 계좌 {self.number}"


class History(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name="계좌")
