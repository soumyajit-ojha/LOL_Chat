from django import forms
from django.contrib.auth.forms import UserCreationForm
from account.models import Account

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text="Required. Add a valid email address.")

    class Meta:
        model   = Account
        fields  = ("email", "username", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.get(email=email)
        except Account.DoesNotExist:
            return email  
        raise forms.ValidationError(f"Email {email} is already in use.")  

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        try:
            account = Account.objects.get(username=username)
        except Account.DoesNotExist:
            return username  
        raise forms.ValidationError(f"Username {username} is already in use.")  

        
class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
        required=True
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
        required=True
    )