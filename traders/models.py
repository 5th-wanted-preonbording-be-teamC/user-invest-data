from django.db import models


class Traders(models.Model):
    company = models.CharField(max_length=30, unique=True, blank=False, verbose_name="증권사")
    is_deposit = models.BooleanField(blank=False, verbose_name="입/출금")
    amount = models.PositiveIntegerField(verbose_name="입/출금 금액")
