# Generated by Django 4.1.2 on 2022-10-31 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("assets", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="asset",
            name="isin",
            field=models.CharField(max_length=50, unique=True, verbose_name="ISIN"),
        ),
    ]
