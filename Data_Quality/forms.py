
from django import forms

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