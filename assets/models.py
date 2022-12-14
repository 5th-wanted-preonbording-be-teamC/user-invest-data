from django.db import models


class Group(models.Model):
    class GroupNameChoices(models.TextChoices):
        AMERICA_STOCK = ("미국 주식", "미국 주식")
        AMERICA_SECTOR_STOCK = ("미국섹터 주식", "미국섹터 주식")
        DEVELOPED_COUNTRY_STOCK = ("선진국 주식", "선진국 주식")
        EMERGING_MARKET_STOCK = ("신흥국 주식", "신흥국 주식")
        WORLD_STOCK = ("전세계 주식", "전세계 주식")
        PROPERTY_AND_MATERIALS = ("부동산 / 원자재", "부동산 / 원자재")
        BOND_AND_CASH = ("채권 / 현금", "채권 / 현금")

    name = models.CharField(
        max_length=50,
        choices=GroupNameChoices.choices,
        unique=True,
        verbose_name="자산그룹",
    )

    def __str__(self):
        return self.name


class Asset(models.Model):
    name = models.CharField(max_length=50, verbose_name="종목명")
    isin = models.CharField(max_length=50, unique=True, verbose_name="ISIN")
    group = models.ForeignKey(
        "Group",
        on_delete=models.CASCADE,
        related_name="assets",
        verbose_name="자산그룹",
    )

    def __str__(self):
        return self.name
