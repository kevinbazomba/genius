from django.urls import path
from . import views

urlpatterns = [
    path('', views.vue_accueil, name='accueil'),
    path('tableau-de-bord/', views.vue_tableau_de_bord, name='tableau_de_bord'),
    path('connexion/', views.vue_connexion, name='connexion'),
    path('deconnexion/', views.vue_deconnexion, name='deconnexion'),
]
