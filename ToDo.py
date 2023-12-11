"""This is Django custom command creates 5 CarType objects with model, name, price, 3 Dealership objects with name
and adds all CarType objects to all Dealership objects. Ad it works with transaction.atomic()"""
from django.core.management.base import BaseCommand
from django.db import transaction
from carshop.models import *


class Command(BaseCommand):
    help = "Creates 5 CarType objects, 3 Dealership objects and adds all CarType objects to all Dealership objects"

    def handle(self, *args, **options):
        with transaction.atomic():
            ct_1 = CarType.objects.create(model="Model 3", brand="Tesla", price=28000)
            ct_2 = CarType.objects.create(model="Model Y", brand="Tesla", price=33000)
            ct_3 = CarType.objects.create(model="EX30", brand="Volvo", price=30000)
            ct_4 = CarType.objects.create(model="Outback", brand="Subaru", price=29000)
            ct_5 = CarType.objects.create(model="Enyaq", brand="Skoda", price=45000)
            dealer_1 = Dealership.objects.create(name="All USA")
            dealer_2 = Dealership.objects.create(name="All EU")
            dealer_3 = Dealership.objects.create(name="All Asia")

            for dealer in Dealership.objects.all():
                for car_type in CarType.objects.all():
                    dealer.available_car_type.add(car_type)
