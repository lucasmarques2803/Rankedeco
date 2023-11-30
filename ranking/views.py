from multiprocessing import context
import time
from django.db.models import Avg, F
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, redirect
from django.urls import reverse
from django.views import generic
from .models import Bandeco, Item, Nota, Comentario
from .forms import ComentarioForm
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
    model=Bandeco
    template_name = "ranking/detail.html"

    def get(self, request, pk):
        bandeco = get_object_or_404(Bandeco, pk=pk)

        lunch_menu = get_api_data(bandeco.name)["lunch_menu"]
        lunch_itens = Item.objects.filter(bandeco=bandeco, name__in=lunch_menu)
        lunch_notas = Nota.objects.filter(bandeco=bandeco, item__in=lunch_itens)
        lunch_average = lunch_notas.aggregate(Avg("value"))

        dinner_menu = get_api_data(bandeco.name)["dinner_menu"]
        dinner_itens = Item.objects.filter(bandeco=bandeco, name__in=dinner_menu)
        dinner_notas = Nota.objects.filter(bandeco=bandeco, item__in=dinner_itens)
        dinner_average = dinner_notas.aggregate(Avg("value"))

        bandeco_data = {
            "lunch_menu": lunch_menu,
            "dinner_menu": dinner_menu,
            "lunch_nota": lunch_average["value__avg"],
            "dinner_nota": dinner_average["value__avg"],
        }

        context = {
            "bandeco": bandeco,
            "bandeco_data": bandeco_data,
            "comment_form": ComentarioForm(),
        }

        return render(request, self.template_name, context)
  
    def post(self, request, pk):
        bandeco = get_object_or_404(Bandeco, pk=pk)

        # Check if the form is submitted for comment creation
        if 'delete_comment_id' in request.POST:
            comment_id = request.POST.get('delete_comment_id')
            try:
                comment = Comentario.objects.get(pk=comment_id, bandeco=bandeco)
                comment.delete()
            except Comentario.DoesNotExist:
                # Handle the case where the comment does not exist
                pass

        return redirect('detail', pk=bandeco.pk)


def create_comentario(request, bandeco_id):
    bandeco = get_object_or_404(Bandeco, pk=bandeco_id)
    
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario_author = request.user
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
                item, created = Item.objects.get_or_create(name=menu_item)

                nota, created = Nota.objects.get_or_create(bandeco=bandeco, item=item)
                nota.value = (F('value') * F('count') + comentario_nota) / (F('count') + 1)
                nota.count = F('count') + 1
                nota.save()

            return HttpResponseRedirect(
                reverse('detail', args=(bandeco_id,))
            )

    form = ComentarioForm()
    context = {'form': form, 'bandeco': bandeco}
    return render(request, 'ranking/comment.html', context)