from django.urls import path
from .views import BandecoList, BandecoDetail, ItemList, ItemDetail, NotaList, NotaDetail, ComentarioList, ComentarioDetail

urlpatterns = [
    path('bandeco/<int:pk>/', BandecoDetail.as_view()),
    path('bandeco/', BandecoList.as_view()),
    path('item/<int:pk>/', ItemDetail.as_view()),
    path('item/', ItemList.as_view()),
    path('nota/<int:pk>/', NotaDetail.as_view()),
    path('nota/', NotaList.as_view()),
    path('comentario/<int:pk>/', ComentarioDetail.as_view()),
    path('comentario/', ComentarioList.as_view()),
]