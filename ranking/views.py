from multiprocessing import context
import time
from django.db.models import Avg
from django.views import generic
from .models import Bandeco, Item, Nota, Comentario
import requests


# Variáveis globais
url = 'https://uspdigital.usp.br/rucard/servicos/menu/'
hash = '596df9effde6f877717b4e81fdb2ca9f'
restaurant_ids = {"Central": 6, "Prefeitura": 7, "Fisica": 8, "Quimica": 9}


# Função utilitária para pegar o cardápio de um restaurante
def get_api_data(restaurant: str) -> dict:
    restaurant_request = {restaurant: requests.post(f"{url}{restaurant_ids[restaurant]}", data={"hash": hash})}
    
    lunch_menu = restaurant_request[restaurant].json()["meals"][0]["lunch"]["menu"].split("\n")
    dinner_menu = restaurant_request[restaurant].json()["meals"][0]["dinner"]["menu"].split("\n")

    context = {
        "bandeco": restaurant,
        "lunch_menu": lunch_menu,
        "dinner_menu": dinner_menu,
    }

    return context


class BandecoListView(generic.ListView):
    model = Bandeco
    template_name = "ranking/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        bandecos = Bandeco.objects.all()
        context["bandeco_data"] = []

        for bandeco in bandecos:
            if time.localtime().tm_hour < 15:
                menu = get_api_data(bandeco.name)["lunch_menu"]
            else:
                menu = get_api_data(bandeco.name)["dinner_menu"]

            itens = Item.objects.filter(bandeco=bandeco, name__in=menu)
            notas = Nota.objects.filter(bandeco=bandeco, item__in=itens)
            average = notas.aggregate(Avg("value"))

            bandeco_data = {
                "bandeco": bandeco,
                "menu": menu,
                "itens": itens,
                "average_nota": average["value__avg"],
            }

            context["bandeco_data"].append(bandeco_data)

        return context


class BandecoDetailView(generic.DetailView):
    model = Bandeco
    template_name = "ranking/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        lunch_menu = get_api_data(self.object.name)["lunch_menu"]
        lunch_itens = Item.objects.filter(bandeco=self.object, name__in=lunch_menu)
        lunch_notas = Nota.objects.filter(bandeco=self.object, item__in=lunch_itens)
        lunch_average = lunch_notas.aggregate(Avg("value"))

        dinner_menu = get_api_data(self.object.name)["dinner_menu"]
        dinner_itens = Item.objects.filter(bandeco=self.object, name__in=dinner_menu)
        dinner_notas = Nota.objects.filter(bandeco=self.object, item__in=dinner_itens)
        dinner_average = dinner_notas.aggregate(Avg("value"))

        bandeco_data = {
            "lunch_menu": lunch_menu,
            "dinner_menu": dinner_menu,
            "lunch_nota": lunch_average["value__avg"],
            "dinner_nota": dinner_average["value__avg"],
        }

        context["bandeco_data"] = bandeco_data

        return context
