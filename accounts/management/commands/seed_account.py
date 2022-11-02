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
) -> Tuple[Callable[[str], Optional[Trader]], Callable[[str], Optional[User]]]:
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
                if (traders := Trader.objects.filter(name=trader)).exists()
                else Trader.objects.create(name=trader)
            )
            user_map[number] = (
                users.first()
                if (users := User.objects.filter(username=username)).exists()
                # 실 서비스에서는 User 식별자를 username으로 사용하면 안 됨
                # 본인 인증 등의 추가 기능이 필요
                # 임시로 username을 식별자로 사용
                else User.objects.create(username=username)
            )
    return trader_map.get, user_map.get


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
                    user: Final = user_of(number)
                    is_user: Final = user is not None
                    owner, is_owner_created = AccountOwner.objects.filter(
                        user=user
                    ).get_or_create(
                        is_user=is_user,
                        name=user.username if is_user else f"{number}소유주",
                        user=user,
                    )
                    # if is_owner_created: owner.save()
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"AccountOwner {owner} is User {owner.user.id}."
                            if owner.is_user
                            else f"AccountOwner {owner.name} created."
                        )
                    )
                    account, is_account_created = Account.objects.filter(
                        owner=owner,
                        number=number,
                    ).get_or_create(
                            owner=owner,
                            number=number,
                            trader=trader_of(number),
                            principal=principal,
                            name=f"{number}계좌",
                    )
                    # if is_account_created: account.save()

                    self.stdout.write(
                        self.style.SUCCESS(f"Account {account.number} created.")
                    )
                except IntegrityError:
                    self.stdout.write(
                        self.style.ERROR(f"Fail to create account {number}.")
                    )
                except Trader.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"{number} has no trader."))
