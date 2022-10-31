from django.db import models

from stocks.models import Stock


class Trader(models.Model):
    company = models.CharField(max_length=30, verbose_name="증권사명")
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, blank=True, verbose_name="주식")

