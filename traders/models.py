from django.db import models

class Trader(models.Model):
    company = models.CharField(max_length=30, unique=True, blank=False, verbose_name="증권사")
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, blank=True, verbose_name="주식종목")
    account = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, verbose_name="계좌")

