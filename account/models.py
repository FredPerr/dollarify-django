import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from .managers import UserManager
from .validators import validate_phone_number


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=18, validators=[validate_phone_number,], null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class AccountAttribute(models.Model):
    short_name = models.CharField(max_length=32)
    full_name = models.CharField(max_length=32, null=True)
    information = models.TextField()

    def __str__(self):
        return self.short_name


class AccountType(models.Model):
    short_name = models.CharField(max_length=32)
    full_name = models.CharField(max_length=32, null=True)
    information = models.TextField()

    def __str__(self):
        return self.short_name


class FinancialEntity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=255, null=True, blank=True)


class Account(FinancialEntity):

    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    type = models.ForeignKey(AccountType, related_name='type', on_delete=models.RESTRICT)
    attribute = models.ForeignKey(AccountAttribute, related_name='attribute', on_delete=models.RESTRICT, null=True, blank=True)

    def __str__(self) -> str:
        attrib_name = self.attribute.short_name if self.attribute else ''
        return f"{self.user.email} {self.type.short_name} {attrib_name}"


class Region(models.Model):

    types = (
        ('Country', 'Country'),
        ('State/Province', 'State/Province'),
    )

    short_name = models.CharField(max_length=5)
    full_name = models.CharField(max_length=50)
    type = models.CharField(max_length=50, choices=types)

class Holiday(models.Model):

    name = models.CharField(max_length=50)
    date = models.DateField()
    region = models.ManyToManyField(Region, 'region')


class StockMarket(models.Model):

    short_name = models.CharField(max_length=10, primary_key=True)
    full_name = models.CharField(max_length=40)
    timezone = models.CharField(max_length=12, default='UTC')
    region = models.ForeignKey(Region, on_delete=models.RESTRICT)
    open_hour = models.DecimalField(max_digits=4, decimal_places=2, default=9.5)
    close_hour = models.DecimalField(max_digits=4, decimal_places=2, default=4.0)
    lunch_start_hour = models.DecimalField(max_digits=4, decimal_places=2, default=None, null=True)
    lunch_end_hour = models.DecimalField(max_digits=4, decimal_places=2, default=None, null=True)



class Transaction(models.Model):
    source_entity = models.ForeignKey(FinancialEntity, related_name='source_entity', on_delete=models.CASCADE)
    destination_entity = models.ForeignKey(FinancialEntity, related_name='destination_entity', on_delete=models.CASCADE, null=True)
    datetime = models.DateTimeField(default=timezone.now)


class StockMarketTrade(Transaction):
    stock_market = models.ForeignKey(StockMarket, related_name='stock_market', on_delete=models.CASCADE)
    ticker = models.CharField(max_length=10)
    bought_value = models.DecimalField(decimal_places=3, max_digits=10)
    shares = models.IntegerField()
    bought_on = models.DateTimeField(default=timezone.now)
    sold_on = models.DateTimeField(null=True)
    sold_value = models.DecimalField(max_digits=10, decimal_places=3)


class Loan(Transaction):
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    due_date = models.DateField(null=True)


class Transfer(Transaction):
    amount = models.DecimalField(max_digits=15, decimal_places=2)


class Payment(Transaction):
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    reason = models.CharField(max_length=50)


class Paycheck(Transaction):
    amount = models.DecimalField(max_digits=15, decimal_places=2)
 