from django import forms
from . import models


class CreateClientForm(forms.ModelForm):
    class Meta:
        model = models.Client
        fields = ["name", "email", "phone"]


class SelectClientForm(forms.Form):
    client = forms.ModelChoiceField(
        queryset=models.Client.objects.all(),
        label="Available clients",
        widget=forms.Select(attrs={"class": "form-control"}),
    )


class SelectDealershipForm(forms.Form):
    client = forms.ModelChoiceField(
        queryset=models.Client.objects.all(),
        label="Select client",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    dealership = forms.ModelChoiceField(
        queryset=models.Dealership.objects.all(),
        label="Select dealership",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    def __init__(self, *args, **kwargs):
        client_id = kwargs.pop("client_id", None)
        super(SelectDealershipForm, self).__init__(*args, **kwargs)
        if client_id:
            self.fields["client"].initial = client_id


class SelectCarTypeForm(forms.Form):
    car_type = forms.ModelChoiceField(
        queryset=models.CarType.objects.none(),
        label="Select car type",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    def __init__(self, *args, dealership_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        if dealership_id:
            dealership = models.Dealership.objects.get(id=dealership_id)
            self.fields["car_type"].queryset = dealership.available_car_type.all()


class SelectCarAndLicenseForm(forms.Form):
    car = forms.ModelChoiceField(
        queryset=models.Car.objects.none(),
        label="Select car year and color",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    license_number = forms.ModelChoiceField(
        queryset=models.License.objects.filter(car=None),
        label="Select license number",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    def __init__(self, *args, car_type_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        if car_type_id:
            self.fields["car"].queryset = models.Car.objects.filter(
                car_type_id=car_type_id, blocked_by_order=None, owner=None
            )


class SelectOrderForm(forms.Form):
    order = forms.ModelChoiceField(
        queryset=models.Order.objects.filter(is_paid=False),
        label="Available orders",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
