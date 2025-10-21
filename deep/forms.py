from django import forms
from .models import User, Poster

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'mobile', 'email', 'membership_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'membership_type': forms.Select(attrs={'class': 'form-control'}),
        }

class PosterForm(forms.ModelForm):
    class Meta:
        model = Poster
        fields = ['title', 'image', 'description', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }