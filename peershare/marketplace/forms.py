from django import forms
from .models import Item, Review, Booking


class ItemForm(forms.ModelForm):
    class Meta:
        model  = Item
        fields = ['title', 'description', 'price', 'category', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'e.g. Scientific Calculator'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Describe your item in detail...'
            }),
            'price': forms.NumberInput(attrs={
                'placeholder': 'Enter price in ৳',
                'min': 1,
            }),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model  = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Share your experience...'
            }),
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model  = Booking
        fields = ['days']
        widgets = {
            'days': forms.NumberInput(attrs={
                'placeholder': 'How many days?',
                'min': 1,
                'max': 365,
            }),
        }


class ChatForm(forms.Form):
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 2,
            'placeholder': 'Type your message...'
        })
    )


# ── CARD PAYMENT FORM ─────────────────────────────────────
class CardPaymentForm(forms.Form):
    card_name = forms.CharField(
        label='Cardholder Name',
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g. Arafat Rahman',
        })
    )
    card_number = forms.CharField(
        label='Card Number',
        max_length=19,
        widget=forms.TextInput(attrs={
            'placeholder': '1234 5678 9012 3456',
            'inputmode': 'numeric',
            'maxlength': '19',
        })
    )
    expiry = forms.CharField(
        label='Expiry Date',
        max_length=5,
        widget=forms.TextInput(attrs={
            'placeholder': 'MM/YY',
            'maxlength': '5',
        })
    )
    cvv = forms.CharField(
        label='CVV',
        max_length=4,
        widget=forms.TextInput(attrs={
            'placeholder': '123',
            'maxlength': '4',
            'inputmode': 'numeric',
        })
    )

    def clean_card_number(self):
        number = self.cleaned_data.get(
            'card_number', ''
        ).replace(' ', '')
        if not number.isdigit():
            raise forms.ValidationError(
                'Card number must contain only digits.'
            )
        if len(number) < 13 or len(number) > 16:
            raise forms.ValidationError(
                'Card number must be 13–16 digits.'
            )
        return number

    def clean_cvv(self):
        cvv = self.cleaned_data.get('cvv', '')
        if not cvv.isdigit():
            raise forms.ValidationError('CVV must be digits only.')
        if len(cvv) < 3:
            raise forms.ValidationError('CVV must be 3–4 digits.')
        return cvv

    def clean_expiry(self):
        expiry = self.cleaned_data.get('expiry', '')
        if '/' not in expiry:
            raise forms.ValidationError('Format must be MM/YY.')
        parts = expiry.split('/')
        if len(parts) != 2 or not all(
            p.isdigit() for p in parts
        ):
            raise forms.ValidationError('Format must be MM/YY.')
        return expiry


# ── BKASH PAYMENT FORM ────────────────────────────────────
class BkashPaymentForm(forms.Form):
    bkash_number = forms.CharField(
        label='bKash Account Number',
        max_length=14,
        widget=forms.TextInput(attrs={
            'placeholder': '01XXXXXXXXX',
            'inputmode': 'numeric',
        })
    )
    bkash_txn_id = forms.CharField(
        label='Transaction ID (TrxID)',
        max_length=20,
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g. 8F3K2L9P1A',
        })
    )

    def clean_bkash_number(self):
        number = self.cleaned_data.get('bkash_number', '')
        number = number.replace(' ', '').replace('-', '')
        if not number.isdigit():
            raise forms.ValidationError(
                'Phone number must contain only digits.'
            )
        if len(number) != 11:
            raise forms.ValidationError(
                'bKash number must be 11 digits.'
            )
        if not number.startswith('01'):
            raise forms.ValidationError(
                'Must be a valid Bangladeshi number (01...).'
            )
        return number

    def clean_bkash_txn_id(self):
        txn = self.cleaned_data.get('bkash_txn_id', '').strip()
        if len(txn) < 6:
            raise forms.ValidationError(
                'Transaction ID must be at least 6 characters.'
            )
        return txn