from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("create_client/", views.create_client, name="create_client"),  # Create client
    path("select_client/", views.select_client, name="select_client"),  # Select client
    path("view_client/<int:client_id>/", views.view_client, name="view_client"),
    path(
        "select_dealership/", views.select_dealership, name="select_dealership"
    ),  # Create order
    path("select_car_type/", views.select_car_type, name="select_car_type"),
    path(
        "select_car_and_license/",
        views.select_car_and_license,
        name="select_car_and_license",
    ),
    path("select_order/", views.select_order, name="select_order"),  # Select order
    path("view_order/<int:order_id>/", views.view_order, name="view_order"),
]
