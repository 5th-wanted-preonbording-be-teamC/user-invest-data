from django.db import models


class Stock(models.Model):
    company = models.CharField(max_length=100)
    isin = models.CharField(max_length=12, primary_key=True)
    ticker = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.ticker
