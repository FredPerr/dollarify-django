from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserCreationForm, UserChangeForm
from .models import (
    FinancialEntity, Holiday, Loan, Paycheck, Payment, Region, Transfer, User, Account, AccountType, 
    AccountAttribute, StockMarket, StockMarketTrade,
)


class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
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


admin.site.register(User, CustomUserAdmin)
admin.site.register(Account)
admin.site.register(AccountType)
admin.site.register(AccountAttribute)
admin.site.register(StockMarket)
admin.site.register(StockMarketTrade)
admin.site.register(FinancialEntity)
admin.site.register(Region)
admin.site.register(Holiday)
admin.site.register(Loan)
admin.site.register(Transfer)
admin.site.register(Payment)
admin.site.register(Paycheck)


