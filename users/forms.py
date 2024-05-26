from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import CustomUser
from django import forms
class CustomuserCreationForm(UserCreationForm):
    class Meta:
        model=CustomUser
        fields=("email",)
class CustomerUserChangeForm(UserChangeForm):
    class Meta:
        model=CustomUser
        fields=("email",)
class LoginForm(forms.Form):
    email=forms.EmailField()
    password=forms.CharField(max_length=65, widget=forms.PasswordInput)

class RegisterForm(UserCreationForm):
    email=forms.CharField(widget=forms.EmailInput(attrs={"placeholder": "Enter email-address"}))
    username=forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Enter username"}))
    password1=forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"placeholder": "Enter password"}))
    password2=forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={"placeholder": "Confirm password"}))
    
    class Meta:
        model=CustomUser
        fields=["email","username","password1","password2"]