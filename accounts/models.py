from django.db import models
from users.models import User
# from traders.models import Trader


class Account(models.Model):
    number = models.CharField(
        max_length=20,
        primary_key=True,
        verbose_name="계좌번호",
        )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="계좌주",
    )
    # trader = models.ForeignKey(
    #     Trader,
    #     on_delete=models.CASCADE,
    # verbose_name="증권사")
    principal = models.PositiveBigIntegerField(verbose_name="투자원금")

    def __str__(self):
        return f"{self.user}의 계좌 {self.number}"
