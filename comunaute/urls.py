from django.urls import path
from django.conf.urls import url
from . import views
from django.views.generic import ListView
from .models import *

urlpatterns = [

    url("Accueil", views.Accueil,name="accueil"),
    url("Inscription",views.inscription,name="inscription"),
    url("Connexion",views.connexion,name="connexion"),
    url("Deconnexion",views.deconnexion,name="deconnexion"),
    url("Demande",views.demande,name="demande"),
    url("DemandeForm",views.FormulaireDemande,name="formdemande"),
    url("geo",views.FoliumView.as_view(),name="geo"),
    url("Valider",views.CommandeValider,name="commandevalider"),
    url("MesD",views.MesDemande,name="msd"),
    url("About",views.Apropos,name="apropos"),
    url("Contact",views.Contact,name="contact"),
    url("ProduitStat",views.ProduitStat,name="produitStat"),
    url("MonCompte",views.MonCompte,name="moncompte"),
    url("ListeD",views.ListeDemande,name="liste"),
    url("Stock",views.Stock,name="stock")



]
