from django.db import models
from users.models import User
# from traders.models import Trader


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
        return self.user.name


class Account(models.Model):
    number: models.CharField = models.CharField(
        max_length=20,
        primary_key=True,
        verbose_name="계좌번호",
        )
    user: models.ForeignKey = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="계좌주",
    )
    # trader: models.ForeignKey = models.ForeignKey(
    #     Trader,
    #     on_delete=models.CASCADE,
    # verbose_name="증권사")
    principal: models.PositiveBigIntegerField = models.PositiveBigIntegerField(
        verbose_name="투자원금",
    )

    def __str__(self) -> str:
        return f"{self.user}의 계좌 {self.number}"
