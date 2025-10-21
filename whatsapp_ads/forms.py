from django import forms
from .models import WhatsAppUser

class WhatsAppUserForm(forms.ModelForm):
    class Meta:
        model = WhatsAppUser
        fields = ['name', 'mobile', 'email', 'membership_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full name'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}),
            'membership_type': forms.Select(attrs={'class': 'form-select'}),
        }
