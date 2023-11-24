from django import forms
from . import models


class CreateClientForm(forms.ModelForm):
    class Meta:
        model = models.Client
        fields = ["name", "email", "phone"]


class SelectClientForm(forms.Form):
    client = forms.ModelChoiceField(
        queryset=models.Client.objects.all(),
        label='Available clients',
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class SelectDealershipForm(forms.Form):
    dealership = forms.ModelChoiceField(
        queryset=models.Dealership.objects.all(),
        label='Select dealership',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
