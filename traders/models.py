from django.db import models

class Traders(models.Model):
    company = models.CharField(max_length=30, unique=True, blank=False, verbose_name="증권사")

    # 증권 회사가 자기고있는 계좌정보
    # accounts = models.ForeignKey(...)
    # 증권회사에서 이루어진 거래 내역
    # transactions = models.ForeignKey(...)

