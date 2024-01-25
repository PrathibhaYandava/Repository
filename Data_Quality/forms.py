
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class OnpremiseForm(forms.Form):
    Domain = forms.CharField(label="Domain")
    Repository = forms.CharField(label="Repository")
    HostName = forms.CharField(label="HostName")
    Port = forms.CharField(label="Port")
    UserName = forms.CharField(label="UserName")
    Password = forms.CharField(label="Password")


class CloudForm(forms.Form):
    IDomain = forms.CharField(label="IDomain")
    IRepository = forms.CharField(label="IRepository")
    IURL = forms.CharField(label="IURL")
    IUserName = forms.CharField(label="IUserName")
    IPassword = forms.CharField(label="IPassword")