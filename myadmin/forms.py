from django import forms

class AdminRegisterForm(forms.Form):
    username = forms.CharField(label='username',max_length=100)
    password = forms.CharField(widget=forms.PasswordInput,max_length=100)
