from django.forms import ModelForm

from account.models import Account, FinancialEntity


class FinancialEntityCreateForm(ModelForm):

    class Meta:
        model = FinancialEntity
        fields = ('name', 'description')


class AccountCreateForm(ModelForm):

    class Meta:
        model = Account
        fields = ('name', 'type', 'attribute', 'description')
        exclude = ('user_id', )
