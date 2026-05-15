from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import CustomUser


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your username',
            'autofocus': True,
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter your password',
        })
    )


class RegisterForm(UserCreationForm):
    university_email = forms.EmailField(
        label='University Email (.edu)',
        widget=forms.EmailInput(attrs={
            'placeholder': 'yourname@university.edu'
        })
    )
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Create a strong password'
        })
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password'
        })
    )

    class Meta:
        model  = CustomUser
        fields = [
            'username', 'university_email',
            'password1', 'password2'
        ]
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Choose a username'
            }),
        }

    def clean_university_email(self):
        email = self.cleaned_data.get('university_email')
        if not email.endswith('.edu'):
            raise forms.ValidationError(
                'Only .edu university emails are allowed!'
            )
        if CustomUser.objects.filter(university_email=email).exists():
            raise forms.ValidationError(
                'This email is already registered.'
            )
        return email
