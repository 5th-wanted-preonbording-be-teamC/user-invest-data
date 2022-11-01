from django.db import models

from users.models import User


class Trader(models.Model):
    company = models.CharField(
        max_length=30, unique=True, blank=False, verbose_name="증권사"
    )
    is_deposit = models.BooleanField(blank=False, verbose_name="입/출금")
    amount = models.PositiveIntegerField(verbose_name="입/출금 금액")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="사용자")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="입/출금 시간")
