from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserCreationForm, UserEditForm
from .models import *


class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserEditForm
    model = User
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


MODELS = (
    Entity, Account, StockExchange,
    StockMarketAccount, 

    FundTransfer, StockTrade, 
    Loan, Payment, Paycheck, CurrencyRate,
    IncomeAccount
)


admin.site.register(User, CustomUserAdmin)

for model in MODELS:
    admin.site.register(model)
