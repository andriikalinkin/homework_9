from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("create_client/", views.create_client, name="create_client"),
    path("select_client/", views.select_client, name="select_client"),
    path("view_client/<int:client_id>/", views.view_client, name="view_client"),
    path("select_dealership/", views.select_dealership, name="select_dealership"),
    path(
        "select_car_type/<int:dealership_id>/",
        views.select_car_type,
        name="select_car_type",
    ),
    path(
        "select_car_and_license/<int:car_type_id>/",
        views.select_car_and_license,
        name="select_car_and_license",
    ),
    path("select_order/", views.select_order, name="select_order"),
    path("view_order/<int:order_id>/", views.view_order, name="view_order"),
]
