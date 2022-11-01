from django.db import models
from users.models import User
from traders.models import Trader


class Account(models.Model):
    number = models.CharField(max_length=20, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trader = models.ForeignKey(Trader, on_delete=models.CASCADE)

    def __str__(self):
        return self.account_name
