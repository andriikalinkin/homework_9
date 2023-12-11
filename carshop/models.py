from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"ID {self.id} - {self.name}"


class CarType(models.Model):
    model = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    price = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.brand} - {self.model} - {self.price} USD"


class Car(models.Model):
    car_type = models.ForeignKey(CarType, on_delete=models.CASCADE)
    color = models.CharField(max_length=50)
    year = models.IntegerField()
    blocked_by_order = models.ForeignKey("Order", on_delete=models.SET_NULL, null=True, related_name="reserved_cars")
    owner = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, related_name="cars")

    def __str__(self):
        return f"{self.car_type.brand} - {self.car_type.model} - {self.car_type.price} USD - {self.year} - {self.color}"


class License(models.Model):
    car = models.OneToOneField(Car, on_delete=models.SET_NULL, null=True, related_name="license")
    number = models.CharField(max_length=50)

    def __str__(self):
        return f'ID {self.id} - "{self.number}"'


class Dealership(models.Model):
    name = models.CharField(max_length=50)
    available_car_type = models.ManyToManyField(CarType, related_name="dealerships")
    client = models.ManyToManyField(Client, related_name="dealerships")

    def __str__(self):
        return self.name


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="orders")
    dealership = models.ForeignKey(Dealership, on_delete=models.CASCADE, related_name="orders")
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order ID: {self.id} - Client name: {self.client.name}"
