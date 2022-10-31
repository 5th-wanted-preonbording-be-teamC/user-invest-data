import csv
from django.db import IntegrityError
from django.core.management.base import BaseCommand
from ...models import Transaction
from users.models import User
from assets.models import Asset


class Command(BaseCommand):

    help = "This command create transactions"

    def handle(self, *args, **options):
        with open(
            "./data/account_asset_info_set.csv", newline=""
        ) as account_asset_info_set:
            account_asset_info_reader = csv.reader(account_asset_info_set)
            for index, row in enumerate(account_asset_info_reader):
                try:
                    if index != 0:
                        user = User.objects.get(name=row[0])
                        asset = Asset.objects.get(isin=row[4])
                        transaction = Transaction.objects.create(
                            price=int(row[5]),
                            amount=int(row[6]),
                            user=user,
                            asset=asset,
                        )
                        self.stdout.write(
                            f"create {transaction} {self.style.SUCCESS('success!')}"
                        )
                except IntegrityError:
                    self.stdout.write(f"{self.style.ERROR('fail!')}")
                except User.DoesNotExist:
                    self.stdout.write(f"존재하지 않는 유저입니다 {self.style.ERROR('fail!')}")
                except Asset.DoesNotExist:
                    self.stdout.write(f"존재하지 않는 자산입니다 {self.style.ERROR('fail!')}")
