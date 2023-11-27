from multiprocessing import context
from typing import Any
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from .models import Bandeco, Item, Nota, Comentario
import requests
# from .forms import ProjectForm, CommentForm


# Variáveis globais
url = 'https://uspdigital.usp.br/rucard/servicos/menu/'
hash = '596df9effde6f877717b4e81fdb2ca9f'
restaurant_ids = {"Central": 6, "Prefeitura": 7, "Fisica": 8, "Quimica": 9}
meal_components = {"Proteina": 1, "Alternativa": 2, "Acompanhamento": 3, "Salada": 4, "Sobremesa": 5}


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


def detail_bandeco(requests, bandeco):
    context = get_api_data(bandeco)
    return render(requests, "ranking/detail.html", context)
