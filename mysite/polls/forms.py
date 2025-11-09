from django.forms import ModelForm
from .models import Voter
from django import forms

class VoterForm(ModelForm):
    class Meta:
        model = Voter
        fields = ['voter_name', 'voter_email']
        widgets = {
            'voter_name': forms.TextInput(attrs={'class': 'form-control'}),
            'voter_email': forms.TextInput(attrs={'class': 'form-control'}),
        }