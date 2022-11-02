# Generated by Django 4.1.2 on 2022-10-31 04:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Group",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        choices=[
                            ("미국주식", "미국주식"),
                            ("미국섹터주식", "미국섹터주식"),
                            ("선진국주식", "선진국주식"),
                            ("신흥국주식", "신흥국주식"),
                            ("전세계주식", "전세계주식"),
                            ("부동산 / 원자재", "부동산 / 원자재"),
                            ("채권 / 현금", "채권 / 현금"),
                        ],
                        max_length=50,
                        verbose_name="자산그룹",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Asset",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, verbose_name="종목명")),
                ("isin", models.CharField(max_length=50, verbose_name="ISIN")),
                (
                    "group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="assets",
                        to="assets.group",
                        verbose_name="자산그룹",
                    ),
                ),
            ],
        ),
    ]
