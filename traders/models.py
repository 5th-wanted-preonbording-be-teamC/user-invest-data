from django.db import models

class Trader(models.Model):
    name = models.CharField(max_length=30, unique=True, blank=False, verbose_name="증권사")
    group_id = models.PositiveIntegerField(verbose_name="자산그룹_id")
    amount = models.PositiveIntegerField(verbose_name="수량")
    price = models.PositiveIntegerField(verbose_name="금액")
    # 매수:True/매도:False
    is_buy = models.BooleanField(blank=False, verbose_name="매수/매도")
    transactions = models.ForeignKey(
        "transactions.Transaction", on_delete=models.CASCADE, verbose_name="거래"
    )
