from django.forms import ModelForm, NumberInput
from django.urls import reverse_lazy
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import (
    UserCreationForm, 
    AuthenticationForm,PasswordChangeForm, 
    PasswordResetForm, SetPasswordForm
)

from core.widget import DatePickerInput, TimePickerInput


from .models import IncomeAccount, IncomeSourceEntity, Paycheck, StockTrade, User, StockMarketAccount


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')


class UserEditForm(ModelForm):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    password = ReadOnlyPasswordHashField(
        label="Password",
        help_text=
            "Raw passwords are not stored, so there is no way to see this "
            "user's password, but you can change the password using "
            '<a href="{}">this form</a>.',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get("password")
        if password:
            password.help_text = password.help_text.format(reverse_lazy('password:change'))
        user_permissions = self.fields.get("user_permissions")
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.select_related(
                "content_type"
            )

class UserConnectForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('email',)


class UserRecoverForm(PasswordResetForm):
    pass
    

class UserPasswordChangeForm(PasswordChangeForm):
    pass


class UserPasswordSetForm(SetPasswordForm):
    pass


#################
# Account forms #
#################

class StockMarketAccountCreateForm(ModelForm):

    class Meta:
        model = StockMarketAccount
        fields = ('name', 'verbose', 'exchange')
        exclude = ('user_id', )



class StockMarketTradeCreateForm(ModelForm):

    class Meta:
        model = StockTrade
        fields = ('ticker', 'currency', 'amount', 'bought_value', 'bought_on_date', 'bought_on_time', 'sold_on_date', 'sold_on_time', 'sold_value', 'fees')
        exclude = ('source', )
        widgets = {
            'bought_on_date': DatePickerInput(),
            'bought_on_time': TimePickerInput(),
            'sold_on_date': DatePickerInput(),
            'sold_on_time': TimePickerInput(),
            'amount': NumberInput(attrs={
                'step':1, 
                'pattern':'^\\$?(([1-9](\\d*|\\d{0,2}(,\\d{3})*))|0)(\\.\\d{1,2})?$'
            })
        }



class IncomeAccountCreateForm(ModelForm):

    class Meta:
        model = IncomeAccount
        fields = ('source',)
        exclude = ('user_id', )



class PaycheckCreateForm(ModelForm):

    class Meta:
        model = Paycheck
        fields = ('amount', 'hours', 'period_start', 'period_end', 'over_hours', 'over_rate')
        exclude = ('target', )


class IncomeSourceCreateForm(ModelForm):

    class Meta:
        model = IncomeSourceEntity
        fields = ('name', 'verbose')