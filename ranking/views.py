from multiprocessing import context
import time
from typing import Any
from django.db.models import Avg
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Bandeco, Item, Nota, Comentario
from .forms import ComentarioForm
import requests


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
            print(average)
            print(itens)
            print(menu)

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
        context["lunch_menu"] = get_api_data(self.object.name)["lunch_menu"]
        context["dinner_menu"] = get_api_data(self.object.name)["dinner_menu"]
        return context


def create_comentario(request, bandeco_id):
    bandeco = get_object_or_404(Bandeco, pk=bandeco_id)
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario_author = form.cleaned_data['author']
            comentario_text = form.cleaned_data['text']
            comentario_nota = form.cleaned_data['nota']
            comentario = Comentario(author=comentario_author,
                                    text=comentario_text,
                                    nota=comentario_nota,
                                    bandeco=bandeco)
            comentario.save()

            if time.localtime().tm_hour < 15:
                menu = get_api_data(bandeco.name)["lunch_menu"]
            else:
                menu = get_api_data(bandeco.name)["dinner_menu"]
            for menu_item in menu:
                instancia = Item.Objects.filter(bandeco=bandeco, name=menu_item)
                if instancia:
                    nota = Nota.Objects.filter(bandeco=bandeco, item=instancia)
                    nota.value = (nota.value*nota.count + comentario_nota) / (nota.count + 1)
                    nota.count += 1
                    nota.save()
                else:
                    item = Item(name=menu_item, bandeco=bandeco)
                    item.save()
                    nota = Nota(bandeco=bandeco, item=item, value=comentario_nota, count=1)

            return HttpResponseRedirect(
                reverse('detail', 
                        args=(bandeco_id, ))
                )
    
    form = ComentarioForm()
    context = {'form': form, 'bandeco': bandeco}
    return render(request, 'ranking/comments.html', context)
