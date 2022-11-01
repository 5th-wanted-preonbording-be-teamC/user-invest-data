from django.db import models

class Trader(models.Model):
    name = models.CharField(max_length=30, unique=True, blank=False, verbose_name="증권사")
