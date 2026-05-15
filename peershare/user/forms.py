from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model  = Profile
        fields = [
            'bio', 'profile_pic',
            'university', 'phone', 'location'
        ]

        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Tell others about yourself...'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'e.g. 01XXXXXXXXX'
            }),
            'location': forms.TextInput(attrs={
                'placeholder': 'e.g. Mirpur, Dhaka'
            }),
        }