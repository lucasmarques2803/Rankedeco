from django.urls import path

from . import views

urlpatterns = [
    path('', views.BandecoListView.as_view(), name='index'),
    path('<str:bandeco>/', views.detail_bandeco, name='detail'),
]
