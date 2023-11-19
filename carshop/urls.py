from django.urls import path

from . import views


urlpatterns = [
    path("clients/", views.clients, name="clients"),
    path("client/<int:client_id>/", views.client, name="client"),
]
