from django.db import models


class Transaction(models.Model):

    """Transaction Model Definition"""

    price = models.PositiveIntegerField(verbose_name="가격")
    amount = models.PositiveIntegerField(verbose_name="수량")
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="transactions",
        verbose_name="유저",
    )
    asset = models.ForeignKey(
        "assets.Asset",
        on_delete=models.CASCADE,
        related_name="transactions",
        verbose_name="자산",
    )
    account = models.ForeignKey(
        "accounts.Account",
        on_delete=models.CASCADE,
        related_name="transactions",
        verbose_name="계좌",
    )

    def __str__(self):
        return f"{self.user}의 {self.asset} 추가"

    def asset_price(transaction):
        return transaction.price * transaction.amount
