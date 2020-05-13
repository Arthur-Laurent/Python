from django.db import models
from django.contrib.auth.models import UserManager, User
from django.utils import timezone
from address.models import AddressField

import random
import string


class Utilisateur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone = models.CharField(max_length=10, null=False, blank=False)
    adresse = AddressField(on_delete=models.CASCADE, default="1")


class Categorie(models.Model):
    description = models.CharField(max_length=300)
    nom = models.CharField(max_length=25, null=False)


class Produit(models.Model):

    nom = models.CharField(max_length=25, null=False)
    stock = models.IntegerField(null=False)
    date = models.DateTimeField()
    prix = models.FloatField(null=False)
    categorie = models.ForeignKey(Categorie,on_delete=models.CASCADE)
    image = models.ImageField()

class NatureDemande(models.Model):
    nature = models.CharField(max_length=30)

class Commande(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField()

class Panier(models.Model):
        idcommande = models.ForeignKey(Commande,on_delete=models.CASCADE)
        produits = models.ForeignKey(Produit,on_delete=models.CASCADE)
        quantite = models.IntegerField(null=False)
