from django.urls import path

from . import views

urlpatterns = [
    path('', views.BandecoListView.as_view(), name='index'),
    path('<int:pk>/', views.BandecoDetailView.as_view(), name='detail'),
    path('<int:bandeco_id>/create_comment/', views.create_comentario, name='create_comment'),
]
