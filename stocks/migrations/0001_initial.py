# Generated by Django 4.1.2 on 2022-10-31 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Stock",
            fields=[
                ("company", models.CharField(max_length=100)),
                (
                    "isin",
                    models.CharField(max_length=12, primary_key=True, serialize=False),
                ),
                ("ticker", models.CharField(max_length=10, unique=True)),
            ],
        ),
    ]