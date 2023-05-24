from django import forms


class LoginForm(forms.Form):
    email = forms.CharField(label="Email", max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(), label="Password")

