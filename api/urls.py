from django.urls import path
from .views import BandecoList, BandecoDetail, ItemList, ItemDetail, NotaList, NotaDetail, ComentarioList, ComentarioDetail

urlpatterns = [
    path('bandecos/', BandecoList.as_view()),
    path('bandecos/<int:pk>/', BandecoDetail.as_view()),
    path('itens/', ItemList.as_view()),
    path('itens/<int:pk>/', ItemDetail.as_view()),
    path('notas/', NotaList.as_view()),
    path('notas/<int:pk>/', NotaDetail.as_view()),
    path('comentarios/', ComentarioList.as_view()),
    path('comentarios/<int:pk>/', ComentarioDetail.as_view()),
]