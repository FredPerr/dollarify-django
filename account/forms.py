from django.contrib.auth.forms import UserCreationForm as UCreationForm 
from django.contrib.auth.forms import UserChangeForm as UChangeForm

from .models import User


class UserCreationForm(UCreationForm):

    class Meta:
        model = User
        fields = ('email',)


class UserChangeForm(UChangeForm):

    class Meta:
        model = User
        fields = ('email',)
