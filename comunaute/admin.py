from django.contrib import admin
from .models import Categorie, Utilisateur,Produit,NatureDemande

admin.site.register(Categorie)
admin.site.register(Utilisateur)
admin.site.register(Produit)
admin.site.register(NatureDemande)


