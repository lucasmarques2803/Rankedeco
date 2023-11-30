from django.shortcuts import render

from rest_framework import generics

from ranking.models import Bandeco, Item, Nota, Comentario
from .serializers import BandecoSerializer, ItemSerializer, NotaSerializer, ComentarioSerializer


class BandecoList(generics.ListCreateAPIView):
    queryset = Bandeco.objects.all()
    serializer_class = BandecoSerializer


class BandecoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bandeco.objects.all()
    serializer_class = BandecoSerializer

class ItemList(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    
class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class NotaList(generics.ListCreateAPIView):
    queryset = Nota.objects.all()
    serializer_class = NotaSerializer

class NotaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Nota.objects.all()
    serializer_class = NotaSerializer

class ComentarioList(generics.ListCreateAPIView):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer
    
class ComentarioDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer
# Create your views here.
