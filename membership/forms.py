from django import forms
from django.contrib.auth import get_user_model
from .models import Membership

User = get_user_model()

class MembershipForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Membership
        fields = ['user', 'membership_type']
        widgets = {
            'membership_type': forms.Select(attrs={'class': 'form-select'}),
        }
