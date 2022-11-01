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
        trader_map: Dict[str, Trader] = {}
        for _, trader, number, *_ in asset_reader:
            if number in trader_map:
                continue
            trader_map[number] = (
                Trader.objects.get(company=trader)
                if Trader.objects.filter(company=trader).exists() else
                Trader.objects.create(company=trader)
            )
        for i, j in trader_map.items():
            print(i, j)
    return trader_map.get


class Command(BaseCommand):

    help = "This command create accounts"

    def handle(self, *args, **options):
        trader_of = create_traderof_by_infocsv("./data/account_asset_info_set.csv")
        with open(
            "./data/account_basic_info_set.csv", newline=""
        ) as account_basic_info_set:
            account_reader: Final = csv.reader(account_basic_info_set)
            next(account_reader)
            for number, principal in account_reader:
                try:
                    ownername = f"{number}소유주"
                    owner = (
                        AccountOwner.objects.get(name=ownername)
                        if AccountOwner.objects.filter(name=ownername).exists() else
                        AccountOwner.objects.create(is_user=True, name=ownername)
                    )  # 추후 User 모델과 연결
                    self.stdout.write(
                        self.style.SUCCESS(f"AccountOwner {owner} created")
                    )
                    account = (
                        Account.objects.get(
                            number=number,
                        )
                        if Account.objects.filter(number=number).exists() else
                        Account.objects.create(
                            number=number,
                            name=f"{number}계좌",
                            owner=owner,
                            trader=trader_of(number),
                            principal=principal,
                        )
                    )
                    self.stdout.write(
                        self.style.SUCCESS(f"Account {account.number} created")
                    )
                except IntegrityError:
                    self.stdout.write(f"{number = }, {owner = }, {trader_of(number) = }, {int(principal) = }")
                    self.stdout.write(
                        f"{number}: {principal} {self.style.ERROR('fail!')}"
                    )
                except Trader.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"{number}의 증권사가 존재하지 않습니다."))
