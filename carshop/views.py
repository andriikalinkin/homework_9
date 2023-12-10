from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
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
    # user_session = {"client_id": client_id}
    # request.session["user_session"] = user_session
    request.session["client_id"] = client_id
    request.session.modified = True

    orders = models.Order.objects.filter(client=client_id, is_paid=False).values(
        "id",
        "dealership__name",
        "reserved_cars__car_type__brand",
        "reserved_cars__car_type__model",
        "reserved_cars__color",
        "reserved_cars__year",
        "reserved_cars__license__number",
        "reserved_cars__car_type__price",
        "is_paid",
    )

    purchased_cars = models.Car.objects.filter(owner=client_id).values(
        "car_type__brand",
        "car_type__model",
        "color",
        "year",
        "license__number",
        "car_type__price",
    )

    context = {
        "client": models.Client.objects.get(id=client_id),
        "purchased_cars": purchased_cars,
        "orders": orders,
    }

    return render(request, "view_client.html", {"context": context})


def select_dealership(request):
    # user_session = request.session.get("user_session", {})
    # client_id = user_session["client_id"]
    client_id = request.session.get("client_id", None)

    if request.method == "POST":
        form = forms.SelectDealershipForm(request.POST)
        if form.is_valid():
            # user_session["client_id"] = form.cleaned_data["client"].id
            # user_session["dealership_id"] = form.cleaned_data["dealership"].id
            request.session["client_id"] = form.cleaned_data["client"].id
            request.session["dealership_id"] = form.cleaned_data["dealership"].id
            request.session.modified = True

            return redirect("select_car_type")

    form = forms.SelectDealershipForm(client_id=client_id)

    return render(request, "select_dealership.html", {"form": form})


def select_car_type(request):
    # user_session = request.session.get("user_session", {})
    # dealership_id = user_session["dealership_id"]
    dealership_id = request.session.get("dealership_id", None)

    if request.method == "POST":
        form = forms.SelectCarTypeForm(request.POST, dealership_id=dealership_id)
        if form.is_valid():
            # user_session["car_type_id"] = form.cleaned_data["car_type"].id
            request.session["car_type_id"] = form.cleaned_data["car_type"].id
            request.session.modified = True

            return redirect("select_car_and_license")

    form = forms.SelectCarTypeForm(dealership_id=dealership_id)

    return render(request, "select_car_type.html", {"form": form})


def select_car_and_license(request):
    # user_session = request.session.get("user_session", {})
    # client_id = user_session["client_id"]
    # dealership_id = user_session["dealership_id"]
    # car_type_id = user_session["car_type_id"]
    client_id = request.session.get("client_id", None)
    dealership_id = request.session.get("dealership_id", None)
    car_type_id = request.session.get("car_type_id", None)

    if request.method == "POST":
        form = forms.SelectCarAndLicenseForm(request.POST, car_type_id=car_type_id)
        if form.is_valid():
            client = models.Client.objects.get(id=client_id)
            dealership = models.Dealership.objects.get(id=dealership_id)

            try:
                with transaction.atomic():
                    # Create order.
                    order = models.Order.objects.create(
                        client=client, dealership=dealership, is_paid=False
                    )

                    # Add car to a license.
                    license = get_object_or_404(
                        models.License,
                        number=form.cleaned_data["license_number"].number,
                    )
                    license.car = form.cleaned_data["car"]
                    license.save()

                    # Add order, client to a car.
                    car = get_object_or_404(models.Car, id=form.cleaned_data["car"].id)
                    car.blocked_by_order = order
                    car.save()

            except Exception as e:
                print(f"Error in transaction: {e}")

            else:
                return redirect("view_order", order_id=order.id)

    form = forms.SelectCarAndLicenseForm(car_type_id=car_type_id)

    return render(request, "select_car_and_license.html", {"form": form})


def select_order(request):
    if request.method == "POST":
        form = forms.SelectOrderForm(request.POST)
        if form.is_valid():
            order_id = form.cleaned_data["order"].id
            return redirect("view_order", order_id=order_id)

    form = forms.SelectOrderForm()

    return render(request, "select_order.html", {"form": form})


def view_order(request, order_id: int):
    # user_session = request.session.get("user_session", {})
    # client_id = user_session["client_id"]
    client_id = request.session.get("client_id", None)

    order = models.Order.objects.get(id=order_id)

    context = {
        "order_id": order_id,
        "client_name": order.client.name,
        "dealership_name": order.dealership.name,
        "car_brand": order.reserved_cars.first().car_type.brand,
        "car_model": order.reserved_cars.first().car_type.model,
        "car_year": order.reserved_cars.first().year,
        "car_color": order.reserved_cars.first().color,
        "license": order.reserved_cars.first().license.number,
    }

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "delete":
            try:
                with transaction.atomic():
                    license_object = order.reserved_cars.first().license
                    license_object.car = None
                    license_object.save()
                    order.delete()

            except Exception as e:
                print(f"Error in transaction: {e}")
        elif action == "purchase":
            try:
                with transaction.atomic():
                    order.is_paid = True
                    order.save()

                    car = models.Car.objects.get(blocked_by_order=order.id)
                    car.owner = models.Client.objects.get(id=client_id)
                    car.save()
            except Exception as e:
                print(f"Error in transaction: {e}")

        return redirect("view_client", client_id)

    return render(request, "view_order.html", {"context": context})
