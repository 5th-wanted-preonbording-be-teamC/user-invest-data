# Generated by Django 4.1.2 on 2022-11-01 02:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_account_principal_alter_account_number_and_more"),
        ("transactions", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="transaction",
            name="account",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="transactions",
                to="accounts.account",
                verbose_name="계좌",
            ),
            preserve_default=False,
        ),
    ]
