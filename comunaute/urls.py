from django.urls import path
from django.conf.urls import url
from . import views
from django.views.generic import ListView
from .models import *

urlpatterns = [

    url("t", views.Accueil,name="accueil"),
    url("g",views.inscription,name="inscription"),
    url("v",views.connexion,name="connexion"),
    url("h",views.deconnexion,name="deconnexion"),
    url("s",views.demande,name="demande"),
    url("b",views.FormulaireDemande,name="formdemande")


]
