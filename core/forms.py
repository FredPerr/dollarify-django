from django.forms import ModelForm
from django.contrib.auth.forms import (
    UserCreationForm, UserChangeForm, 
    AuthenticationForm,PasswordChangeForm, 
    PasswordResetForm, SetPasswordForm
)


from .models import StockTrade, User, StockMarketAccount


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')


class UserEditForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')


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
        fields = ('ticker', 'currency', 'amount', 'bought_value', 'bought_on', 'sold_on', 'sold_value', 'fees')
        exclude = ('source', )


        