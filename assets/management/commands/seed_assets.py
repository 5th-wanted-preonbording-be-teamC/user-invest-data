import csv
from django.db import IntegrityError
from django.core.management.base import BaseCommand
from ...models import Asset, Group


class Command(BaseCommand):

    help = "This command create assets & group"

    def handle(self, *args, **options):
        with open(
            "./data/asset_group_info_set.csv", newline=""
        ) as asset_group_info_set:
            asset_reader = csv.reader(asset_group_info_set)
            next(asset_reader)  # skip header
            for name, isin, group_name in asset_reader:
                try:
                    group, _ = Group.objects.get_or_create(name=group_name)
                    asset = Asset.objects.create(
                        name=name,
                        isin=isin,
                        group=group,
                    )
                    self.stdout.write(
                        f"create {asset} {self.style.SUCCESS('success!')}"
                    )
                except IntegrityError:
                    self.stdout.write(
                        f"{name} already exists {self.style.ERROR('fail!')}"
                    )
