from django import forms
from django.contrib.auth.forms import UserCreationForm , UserChangeForm
from .models import CustomUser


DISPLAY_CHOICES = (
    ("bfa", "Login with browser Fingerprinting"),
    ("otp", "Login with One Time Password")
)

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username','password','email','passwordbfa','passwordotp')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = '__all__'


class SignupForm(forms.Form):
    username  = forms.CharField(max_length=20)
    password = forms.CharField(max_length=10,min_length=3)
    email = forms.EmailField(max_length=30)

class LoginForm(forms.Form):
    login_type = forms.ChoiceField(widget=forms.RadioSelect,choices=DISPLAY_CHOICES)
       
class BfaForm(forms.Form):
    username = forms.CharField(max_length=10)
    password = forms.CharField(max_length=20 , widget=forms.PasswordInput())
class OtpForm(forms.Form):
    username = forms.CharField(max_length=10)
    OneTimePass = forms.CharField(max_length = 10 , widget= forms.PasswordInput())
