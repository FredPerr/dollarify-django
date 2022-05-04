import uuid

from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models import (
    Model, CharField, EmailField, 
    BooleanField, DateTimeField, 
    DateField, UUIDField, 
    ForeignKey, DecimalField, 
    IntegerField, CASCADE, 
    RESTRICT,
)


from .managers import UserManager
from .validators import validate_phone_number


class User(AbstractBaseUser, PermissionsMixin):
    email = EmailField('email address', unique=True)
    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)
    phone = CharField(max_length=18, validators=[validate_phone_number,], null=True)
    is_staff = BooleanField(default=False)
    is_active = BooleanField(default=True)
    date_joined = DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name} ({self.email})'


##################
# Account models #
##################


class Entity(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = CharField(max_length=50)
    verbose = CharField(max_length=100, null=True, blank=True)


class Account(Entity):
    user = ForeignKey(User, CASCADE, 'user_fk')

    def __str__(self):
        return f"{self.name} ({self.user.email})"


class StockExchange(Entity):
    region = CharField(max_length=30)
    timezone = CharField(max_length=12, default='UTC')
    open_hour = DecimalField(max_digits=4, decimal_places=2, default=9.5)
    close_hour = DecimalField(max_digits=4, decimal_places=2, default=4.0)
    lunch_start_hour = DecimalField(max_digits=4, decimal_places=2, default=None, null=True, blank=True)
    lunch_end_hour = DecimalField(max_digits=4, decimal_places=2, default=None, null=True, blank=True)


class StockMarketAccount(Account):
    exchange = ForeignKey(StockExchange, RESTRICT, 'exchange_fk')

    # TODO: add properties that fetch account value from stock trades.


class CheckingAccount(Account):
    host = ForeignKey(Entity, RESTRICT, 'host_fk')


######################
# Transaction models #
######################


class Transaction(Model):
    """
    Transaction of an amount between two entities.
    """

    datetime = DateTimeField(default=timezone.now)
    amount = DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        abstract = True


class Transfer(Transaction):
    """
    Transaction from an Account to a named entity.
    """

    source = ForeignKey(Account, CASCADE, 'source_fk')
    withdrew = BooleanField()
    """
    If true, the amount of the transfer will be withdrawn from the Account.
    Otherwise, it will be added.
    """


class FundTransfer(Transaction):
    """
    Transaction between two accounts.
    """

    source = ForeignKey(Account, CASCADE, 'source_fundtransfer')
    target = ForeignKey(Account, CASCADE, 'target_fundtransfer')


class StockTrade(Transaction):
    source = ForeignKey(StockMarketAccount, CASCADE, 'source_stocktrade')

    ticker = CharField(max_length=10)
    bought_value = DecimalField(max_digits=10, decimal_places=3)
    shares = IntegerField()
    bought_on = DateTimeField(default=timezone.now)
    sold_on = DateTimeField(null=True)
    sold_value = DecimalField(max_digits=10, decimal_places=3)


class Loan(Transaction):

    target = ForeignKey(Account, CASCADE, 'target_loan')
    source = ForeignKey(Account, CASCADE, 'source_loan')
    """
    The target account is the account on which the money is loaned.
    """
    interest_rate = DecimalField(max_digits=4, decimal_places=2, default=1)
    due_date = DateTimeField(null=True, blank=True)


class Payment(Transaction):
    source = ForeignKey(Account, CASCADE, 'source_payment')
    target = ForeignKey(Account, CASCADE, 'target_payment')
    motive = CharField(max_length=24, null=True, blank=True)


class Paycheck(Transaction):
    source = ForeignKey(Account, CASCADE, 'source_paycheck')
    target = ForeignKey(Account, CASCADE, 'target_paycheck')
    hours = DecimalField(null=True, blank=True, max_digits=7, decimal_places=2)
    
    period_start = DateField(null=True, blank=True)
    period_end = DateField(null=True, blank=True)

    over_hours = DecimalField(null=True, blank=True, max_digits=6, decimal_places=2)
    over_rate = DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
