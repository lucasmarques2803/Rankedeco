from django.shortcuts import render

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from ranking.models import Bandeco, Item, Nota, Comentario
from .serializers import BandecoSerializer, ItemSerializer, NotaSerializer, ComentarioSerializer


class BandecoList(generics.ListAPIView):
    queryset = Bandeco.objects.all()
    serializer_class = BandecoSerializer


class BandecoDetail(generics.RetrieveAPIView):
    queryset = Bandeco.objects.all()
    serializer_class = BandecoSerializer

class ItemList(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    
class ItemDetail(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class NotaList(generics.ListAPIView):
    queryset = Nota.objects.all()
    serializer_class = NotaSerializer

class NotaDetail(generics.RetrieveAPIView):
    queryset = Nota.objects.all()
    serializer_class = NotaSerializer

class ComentarioList(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer
    
class ComentarioDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer