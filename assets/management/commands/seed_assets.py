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
            for index, row in enumerate(asset_reader):
                try:
                    if index != 0:
                        group, created = Group.objects.get_or_create(name=row[2])
                        asset = Asset.objects.create(
                            name=row[0],
                            isin=row[1],
                            group=group,
                        )
                        self.stdout.write(
                            f"create {asset} {self.style.SUCCESS('success!')}"
                        )
                except IntegrityError:
                    self.stdout.write(
                        f"{row[0]} already exists {self.style.ERROR('fail!')}"
                    )
