from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from . import models
from . import forms


def index(request):
    return render(request, "base.html")


def create_client(request):
    if request.method == "POST":
        form = forms.CreateClientForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            phone = form.cleaned_data["phone"]
            client = models.Client.objects.create(name=name, email=email, phone=phone)

            return redirect("view_client", client_id=client.id)

    form = forms.CreateClientForm()

    return render(request, "create_client.html", {"form": form})


def select_client(request):
    if request.method == "POST":
        form = forms.SelectClientForm(request.POST)
        if form.is_valid():
            client_id = form.cleaned_data["client"].id
            return redirect("view_client", client_id=client_id)

    form = forms.SelectClientForm()

    return render(request, "select_client.html", {"form": form})


def view_client(request, client_id: int):
    purchased_cars = models.Car.objects.filter(owner=client_id).values(
        "car_type__brand",
        "car_type__model",
        "color",
        "year",
        "car_type__price",
        "license__number",
    )

    orders = models.Order.objects.filter(client=client_id).values(
        "id",
        "car_types__car_type__brand",
        "car_types__car_type__model",
        "car_types__quantity",
        "dealership",
        "is_paid",
    )

    context = {
        "client": models.Client.objects.get(id=client_id),
        "purchased_cars": purchased_cars,
        "orders": orders,
    }

    return render(request, "view_client.html", {"context": context})


def select_dealership(request):
    if request.method == "POST":
        form = forms.SelectDealershipForm(request.POST)
        if form.is_valid():
            dealership_id = form.cleaned_data["dealership"].id

            return redirect("select_car_type", dealership_id=dealership_id)

    form = forms.SelectDealershipForm()

    return render(request, "select_dealership.html", {"form": form})


def select_car_type(request, dealership_id: int):
    if request.method == "POST":
        form = forms.SelectCarTypeForm(request.POST, dealership_id=dealership_id)
        if form.is_valid():
            car_type_id = form.cleaned_data["car_type"].id

            return redirect("select_car_and_license", car_type_id=car_type_id)

    form = forms.SelectCarTypeForm(dealership_id=dealership_id)

    return render(request, "select_car_type.html", {"form": form, "dealership_id": dealership_id})


def select_car_and_license(request, car_type_id: int):
    pass


def select_order(request):
    pass


def view_order(request, order_id: int):
    pass
