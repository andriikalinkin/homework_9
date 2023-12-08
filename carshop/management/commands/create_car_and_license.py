from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker

from carshop.models import *

fake = Faker()


class Command(BaseCommand):
    help = "Creates the required car and license quantity * CarType.objects.count()"

    def add_arguments(self, parser):
        parser.add_argument("quantity", type=int, help="Quantity of cars and licenses")
        parser.add_argument("color", type=str, help="Color of cars and licenses")
        parser.add_argument("year", type=int, help="Year of cars manufactured")

    def handle(self, *args, **options):
        quantity = options["quantity"]
        color = options["color"]
        year = options["year"]

        try:
            with transaction.atomic():
                all_car_types = CarType.objects.all()

                for car_type in all_car_types:
                    for _ in range(quantity):
                        Car.objects.create(
                            car_type=car_type,
                            color=color,
                            year=year
                        )

                existing_license_numbers = [i.number for i in License.objects.all()]

                for _ in range(CarType.objects.count()):
                    for _ in range(quantity):
                        # Генерация уникального номера лицензии
                        unique_license_number = fake.unique.bothify("?? #### ??")

                        # Проверка на уникальность
                        while unique_license_number in existing_license_numbers:
                            unique_license_number = fake.unique.bothify("?? #### ??")

                        License.objects.create(
                            number=unique_license_number
                        )

                        existing_license_numbers.append(unique_license_number)

        except Exception as e:
            print(f"Error in transaction: {e}")
