import csv
from django.db import IntegrityError
from django.core.management.base import BaseCommand
from ...models import Account, AccountOwner
from traders.models import Trader
from typing import Callable, Final, List, Iterator, Dict


def create_traderof_by_infocsv(fp: str) -> Callable[[str], Trader]:
    with open(fp) as asset_group_info_set:
        asset_reader: Iterator[List[str]] = csv.reader(asset_group_info_set)
        next(asset_reader)  # skip header
        trader_map: Dict[str, Trader] = {
            number: Trader.objects.get(company=trader)
            for _, trader, number, *_ in asset_reader
        }
    return trader_map.get


trader_of = create_traderof_by_infocsv("./data/asset_group_info_set.csv")


class Command(BaseCommand):

    help = "This command create accounts"

    def handle(self, *args, **options):
        with open(
            "./data/account_basic_info_set.csv", newline=""
        ) as account_basic_info_set:
            account_reader: Final = csv.reader(account_basic_info_set)
            next(account_reader)
            for number, principal in account_reader:
                try:
                    owner = AccountOwner.objects.create(
                        is_user=True, name=f"{number}소유주"
                    )  # 이후 User 모델과 연결
                    account = Account.objects.create(
                        number=number,
                        principal=principal,
                        trader=trader_of(number),
                        owner=owner,
                    )
                    self.stdout.write(
                        f"create {account} {self.style.SUCCESS('success!')}"
                    )
                except IntegrityError:
                    self.stdout.write(
                        f"{number}: {principal} {self.style.ERROR('fail!')}"
                    )
                except Trader.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"{number}의 증권사가 존재하지 않습니다."))
