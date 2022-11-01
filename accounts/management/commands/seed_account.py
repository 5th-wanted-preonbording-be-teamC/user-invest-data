import csv
from django.db import IntegrityError
from django.core.management.base import BaseCommand
from ...models import Account, AccountOwner
from traders.models import Trader
from users.models import User
from typing import Callable, Final, Tuple, Iterator, Dict, Optional

info_csv: Final[str] = "./data/account_asset_info_set.csv"


def create_traderof_userof_by_infocsv(
        fp: str = info_csv,
        ) -> Tuple[
            Callable[[str], Optional[Trader]],
            Callable[[str], Optional[User]]
        ]:
    with open(fp) as asset_group_info_set:
        asset_reader: Iterator[Tuple[str]] = csv.reader(asset_group_info_set)
        next(asset_reader)  # skip header
        trader_map: Dict[str, Trader] = {}
        user_map: Dict[str, Trader] = {}
        for username, trader, number, *_ in asset_reader:
            if number in trader_map:
                continue
            trader_map[number] = (
                traders.first()
                if (traders := Trader.objects.filter(company=trader)).exists() else
                Trader.objects.create(company=trader)
            )
            user_map[number] = (
                users.first()
                if (users := User.objects.filter(username=username)).exists() else
                User.objects.create(username=username)
            )
    return trader_map.get, user_map.get


def get_owner(user: Optional[User], default_name: str) -> AccountOwner:
    if user is not None:
        # 사용자가 존재하는 경우
        owners = AccountOwner.objects.filter(user=user)
        # 사용자와 연결된 계좌 소유자 검색
        if owners.exists():
            # 사용자와 연결된 계좌 소유자가 존재하는 경우
            owner = owners.first()
            # 해당 계좌 소유자를 계좌 소유자로 사용
        else:
            # 사용자와 연결된 계좌 소유자가 존재하지 않는 경우
            owner = AccountOwner.objects.create(
                is_user=True,
                user=user,
                name=user.username,
            )
            # 계좌 소유자 생성 후 계좌 소유자로 사용
    else:
        # 사용자가 존재하지 않는 경우
        owner = AccountOwner.objects.create(
            is_user=False,
            name=default_name,  # f"{number}소유주"
        )
        # 임의의 계좌 소유자 생성 후 계좌 생성
    return owner


class Command(BaseCommand):

    help = "This command create accounts"

    def handle(self, *args, **options):
        trader_of, user_of = create_traderof_userof_by_infocsv()
        with open(
            "./data/account_basic_info_set.csv", newline=""
        ) as account_basic_info_set:
            account_reader: Final = csv.reader(account_basic_info_set)
            next(account_reader)
            for number, principal in account_reader:
                try:
                    user = user_of(number)
                    owner = get_owner(user, f"{number}소유주")
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"AccountOwner {owner} is User {owner.user.id}."
                            if owner.is_user else
                            f"AccountOwner {owner.name} created."
                        )
                    )
                    account = (
                        accounts.first()
                        if (accounts := Account.objects.filter(number=number)).exists() else
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
                    self.stdout.write(
                        f"{number}: {principal} {self.style.ERROR('fail!')}"
                    )
                except Trader.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"{number}의 증권사가 존재하지 않습니다."))
