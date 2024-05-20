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
    password1=forms.CharField(label="Password", widget=forms.PasswordInput(attrs={"placeholder": "Enter password"}))
    password2=forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={"placeholder": "Confirm password"}))
    
    class Meta:
        model=CustomUser
        fields=["email","password1","password2"]
    
    def clean_email(self):
        data=self.cleaned_data["email"]
        qs=CustomUser.objects.exclude(id=self.instance).filter(email=data)
        if qs.exists():
            raise forms.ValidationError("Email already in use")
        return data
    def clean_password2(self):
        cd=self.cleaned_data
        if cd['password']!= cd['password2']:
            raise forms.ValidationError("Passwords dont match")
        return cd['password2']