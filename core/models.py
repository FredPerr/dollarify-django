import uuid
from decimal import Decimal
import datetime
import logging

from django.utils import timezone
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models import (
    Model, CharField, EmailField, 
    BooleanField, DateTimeField, 
    DateField, UUIDField, 
    ForeignKey, DecimalField, 
    CASCADE, RESTRICT, TimeField
)


from .managers import UserManager
from .validators import validate_phone_number
from .currency import CURRENCIES
from . import currency


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


    def __str__(self):
        return f"{self.name} ({self.id})"


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

    def __str__(self):
        return f"{self.verbose} ({self.name})"


class StockMarketAccount(Account):
    exchange = ForeignKey(StockExchange, RESTRICT, 'exchange_fk')
    currency = CharField(max_length=4, choices=CURRENCIES)


class IncomeSourceEntity(Entity):
    pass


class IncomeAccount(Account):

    source = ForeignKey(IncomeSourceEntity, RESTRICT, 'source_income')

    @property
    def paychecks(self):
        return Paycheck.objects.filter(target=self)

    @property
    def total_earned(self):
        total = 0
        for paycheck in self.paychecks:
            total += paycheck.amount
        return total
    
    def total_time(self):
        total = 0
        for paycheck in self.paychecks:
            total += paycheck.hours
        return total


    def __str__(self):
        return f"{self.name}"


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


class FundTransfer(Transaction):
    """
    Transaction between two accounts.
    """

    source = ForeignKey(Account, CASCADE, 'source_fundtransfer')
    target = ForeignKey(Account, CASCADE, 'target_fundtransfer')


class StockTrade(Transaction):
    source = ForeignKey(StockMarketAccount, CASCADE, 'source_stocktrade')

    ticker = CharField(max_length=10)
    currency = CharField(max_length=4, choices=CURRENCIES)
    bought_value = DecimalField(max_digits=10, decimal_places=3, validators=[MinValueValidator(0.001)])
    bought_on_date = DateField(default=timezone.now)
    bought_on_time = TimeField(default=datetime.time(0,0))
    sold_on_date = DateField(null=True, blank=True)
    sold_on_time = TimeField(default=datetime.time(0,0))
    sold_value = DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    fees = DecimalField(max_digits=10, decimal_places=2, default=0)

    @property
    def bought_on(self):
        return datetime.datetime.combine(self.bought_on_date, self.bought_on_time)
    
    @property
    def sold_on(self):
        if self.sold_on_date and self.sold_on_time:
            return datetime.datetime.combine(self.sold_on_date, self.sold_on_time)

    @property
    def active(self):
        return not (self.sold_value or self.sold_on)

    @property
    def last_value(self):
        return Decimal(0.0) if self.active else self.sold_value

    @property
    def total_value(self):
        # logging.error(msg=str(self.active))
        return round(Decimal(self.last_value) * Decimal(self.amount) * CurrencyRate.objects.get(from_cur=self.currency, to_cur=self.source.currency).rate, 2)

    @property
    def profit_percent(self):
        return round(100 * (self.last_value / self.bought_value - 1), 2)

    @property
    def profit(self):
        return round((self.last_value - self.bought_value) * self.amount, 2)

    @property
    def duration(self):
        offset = self.sold_on if not self.active else datetime.datetime.replace(timezone.now(), tzinfo=None)

        return offset - self.bought_on

    def __str__(self):
        return f"{self.source.id} ({self.source.name}) {self.ticker} {self.amount}"


class Loan(Transaction):

    target = ForeignKey(Account, CASCADE, 'target_loan')
    source = ForeignKey(Entity, CASCADE, 'source_loan')
    """
    The target account is the account on which the money is loaned.
    """
    interest_rate = DecimalField(max_digits=4, decimal_places=2, default=1)
    due_date = DateTimeField(null=True, blank=True)


class Payment(Transaction):
    source = ForeignKey(Account, CASCADE, 'source_payment')
    target = ForeignKey(Entity, CASCADE, 'target_payment')
    motive = CharField(max_length=24, null=True, blank=True)


class Paycheck(Transaction):
    target = ForeignKey(IncomeAccount, CASCADE, 'target_paycheck')
    hours = DecimalField(null=True, blank=True, max_digits=7, decimal_places=2)
    
    period_start = DateField(null=True, blank=True)
    period_end = DateField(null=True, blank=True)

    over_hours = DecimalField(null=True, blank=True, max_digits=6, decimal_places=2)
    over_rate = DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, default=1.5)

    def __str__(self):
        period = f" from {self.period_start} to {self.period_end}" if self.period_end and self.period_start else ""
        return f"Paycheck #{self.id}: {self.hours} hours for ${self.amount}{period}"



class CurrencyRate(Model):

    from_cur = CharField(max_length=4)
    to_cur = CharField(max_length=4)
    last_value = DecimalField(max_digits=10, decimal_places=5)
    last_updated = DateTimeField(default=timezone.now)

    @property
    def rate(self):
        if datetime.datetime.now(timezone.utc) - self.last_updated > datetime.timedelta(hours=3):
            try:
                rate = currency.get_conversion_rate(self.from_cur, self.to_cur)
                self.last_value = rate
                self.last_updated = timezone.now()
                self.save()
                return round(rate, 2)
            except:
                print('Could not reload the conversion rate.')
        return round(self.last_value, 2)

    def __str__(self):
        return f"{self.from_cur}/{self.to_cur}"



