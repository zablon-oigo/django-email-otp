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
    class Meta:
        model=CustomUser
        fields=["email","password1","password2"]
    
    def clean_email(self):
        data=self.cleaned_data["email"]
        if CustomUser.objects.filter(email=data).exists():
            raise forms.ValidationError("Email already in use")
        return data