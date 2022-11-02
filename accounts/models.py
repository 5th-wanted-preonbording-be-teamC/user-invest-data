from django.db import models

from traders.models import Trader
from users.models import User


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
    name = models.CharField(max_length=80, verbose_name="계좌명")
    trader: models.ForeignKey = models.ForeignKey(
        Trader,
        on_delete=models.CASCADE,
        verbose_name="증권사"
    )
    principal: models.PositiveBigIntegerField = models.PositiveBigIntegerField(
        verbose_name="투자원금",
    )

    def __str__(self) -> str:
        return f"{self.user}의 계좌 {self.number}"

class History(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name="계좌")

