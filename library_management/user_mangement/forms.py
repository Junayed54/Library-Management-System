from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import UserCreationForm
from datetime import date
class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(max_length = 30, required=True)
    class Meta(UserCreationForm.Meta):
        fields = ('username', 'email') 




class ModifiedLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['password'].label = 'Password'





class ChangePasswordForm(PasswordChangeForm):
    pass






class ReturnBookForm(forms.Form):
    return_date = forms.DateField(label='Return Date', widget=forms.DateInput(attrs={'type': 'date'}), initial=date.today)
