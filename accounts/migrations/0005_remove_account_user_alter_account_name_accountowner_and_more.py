# Generated by Django 4.1.2 on 2022-11-02 02:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("accounts", "0004_account_trader_history"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="account",
            name="user",
        ),
        migrations.AlterField(
            model_name="account",
            name="name",
            field=models.CharField(max_length=150, null=True, verbose_name="계좌명"),
        ),
        migrations.CreateModel(
            name="AccountOwner",
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
                ("is_user", models.BooleanField(default=False)),
                ("name", models.CharField(max_length=150, verbose_name="이름")),
                (
                    "user",
                    models.OneToOneField(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="account",
            name="owner",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="accounts.accountowner",
                verbose_name="계좌주",
            ),
            preserve_default=False,
        ),
    ]
