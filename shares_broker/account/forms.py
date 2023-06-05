from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms

CURRENCY_CHOICES =(
    ("GBP", "£-GBP"),
    ("EUR", "€-EUR"),
    ("NGN", "₦-NGN"),
    ("CAD", "$-CAD"),
    ("JPY", "¥-JPY"),
)

# USD,EUR,NGN,GBP,CAD,YEN

class SignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    ucurrency = forms.ChoiceField(choices=CURRENCY_CHOICES)

    class Meta:
        model = User
        fields = ('ucurrency', 'username', 'email', 'password1', 'password2')


    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        for field in ['ucurrency', 'username', 'password1', 'password2']:
            self.fields[field].help_text = None
            self.fields[field].widget.attrs['class'] = 'form-control'


class SignInForm(AuthenticationForm):
    
    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(SignInForm, self).__init__(*args, **kwargs)

        for field in ['username', 'password']:
            self.fields[field].widget.attrs['class'] = 'form-control'


# Password Reset Form
class ResetPwd(forms.Form):
    old_pwd = forms.CharField()
    new_pwd = forms.EmailField()
    renew_pwd = forms.EmailField()

    class Meta:
        model = User
        fields = [
            'old_pwd',
            'new_pwd',
            'renew_pwd',
            ]

class ProfileForm(UserChangeForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'}))

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            ]