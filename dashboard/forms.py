from django.forms import ModelForm

from account.models import StockMarketAccount


class StockMarketAccountCreateForm(ModelForm):

    class Meta:
        model = StockMarketAccount
        fields = ('name', 'verbose', 'exchange')
        exclude = ('user_id', )