from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class RegisterForm(UserCreationForm):
    university_email = forms.EmailField(
        label='University Email (.edu)',
        help_text='Must be a valid .edu email address'
    )

    class Meta:
        model  = CustomUser
        fields = ['username', 'university_email', 'password1', 'password2']

    def clean_university_email(self):
        email = self.cleaned_data.get('university_email')
        if not email.endswith('.edu'):
            raise forms.ValidationError('Only .edu university emails are allowed!')
        if CustomUser.objects.filter(university_email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )