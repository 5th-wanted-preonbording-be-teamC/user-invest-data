from django.db import models

class Traders(models.Model):
    company = models.CharField(max_length=30, unique=True, blank=False, verbose_name="증권사")
    stock = models.ForeignKey(Stocks, on_delete=models.CASCADE, blank=True, verbose_name="주식종목")
    account = models.ForeignKey(Accounts, on_delete=models.CASCADE, blank=True, verbose_name="계좌")

