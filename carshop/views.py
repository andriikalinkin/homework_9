from django.shortcuts import render, get_object_or_404
from . import models


# Create your views here.
def clients(request):
    all_clients = models.Client.objects.all()
    return render(request, "clients.html", {"all_clients": all_clients})


def client(request, client_id: int):
    one_client = get_object_or_404(models.Client, id=client_id)
    client_orders = models.Order.objects.filter(client=one_client)

    context = {
        "one_client": one_client,
        "client_orders": client_orders,
    }

    return render(request, "client.html", {"context": context})
