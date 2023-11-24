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


# class SelectCarTypeForm(forms.Form):
#     dealership_id = dealership_id
#
#     car_type = forms.ModelChoiceField(
#         queryset=models.CarType.objects.all(),
#         label='Select car type',
#         widget=forms.Select(attrs={'class': 'form-control'})
#     )
class SelectCarTypeForm(forms.Form):
    car_type = forms.ModelChoiceField(
        queryset=models.CarType.objects.none(),
        label='Select car type',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def __init__(self, *args, dealership_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        if dealership_id:
            # Фильтруем queryset на основе переданного dealership_id
            dealership = models.Dealership.objects.get(id=dealership_id)
            self.fields['car_type'].queryset = dealership.available_car_type.all()


