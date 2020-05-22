from django.shortcuts import render
from .models import *
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User, UserManager
from address.forms import AddressField
from django.shortcuts import redirect, get_object_or_404, render
from .forms import *
from django.views.generic import CreateView, UpdateView
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from address.models import *
from django.db.models import Sum
import numpy as np
import matplotlib.pyplot as plt
from django.db.utils import IntegrityError
import folium


def Stock(request):
    produits = Produit.objects.all()
    return render(request, 'stock.html', locals())


def Accueil(request):
    return render(request, 'index.html', locals())


@login_required
def demande(request):
    if request.method == "POST":
        return FormulaireDemande(request)
    else:
        natures = NatureDemande.objects.all()

    return render(request, "demande.html", locals())


@login_required
def FormulaireDemande(request):
    produits = Produit.objects.all()

    if request.method == "POST":
        prix = 0
        if 'nature_select' in request.POST.keys():
            commande = Commande.objects.create(date=timezone.now(), user=request.user)
            idcommande = commande.id
            commande.save()
        else:
            idcommande = request.POST['idcommande']
            quantite = request.POST['quantity']
            idproduit = request.POST['idproduit']
            panier = Panier.objects.create(idcommande=Commande.objects.get(pk=idcommande), quantite=quantite,
                                           produits=Produit.objects.get(pk=idproduit))
            panier.save()
            paniers = Panier.objects.filter(idcommande=Commande.objects.get(pk=idcommande))

            if (paniers.count() >= 1):
                conti = True

                for p in paniers:
                    prix += p.quantite * p.produits.prix
            else:

                conti = False

    else:
        pass

    return render(request, "FormDemande.html", locals())


@login_required
def ProduitStat(request):
    # Récupération des données

    maxi = 5
    produit_quantites = Panier.objects.values('produits').annotate(total=Sum('quantite')).order_by(
        'total')  # Somme les quantités parmi les commandes abouties, 0 sinon
    produits = []
    quantites = []
    for produit_quantite in produit_quantites:
        id = produit_quantite['produits']
        produits.append(
            Produit.objects.get(pk=id).nom)  # Récupération de la liste des produits listés dans produit_quantites
        quantites.append(
            produit_quantite['total'])  # Récupération de la liste des quantités listées dans produit_quantites
    # Récupération du graphique
    y_pos = np.arange(len(produit_quantites))
    plt.grid()
    plt.barh(y_pos[0:maxi], quantites[0:maxi])  # Pour les positions de 0 à maxi, on entre les valeurs de quantité
    plt.yticks(y_pos[0:maxi], produits[0:maxi])
    plt.xlabel('Quantité')
    plt.title('Produits les plus populaires')

    plt.savefig("static/img/popularite_des_produits.png")
    return render(request, "ProduitStat.html", locals())


def Apropos(request):
    return render(request, "about.html", locals())


def Contact(request):
    return render(request, 'contact.html', locals())


@login_required
def MonCompte(request):
    utilisateur = Utilisateur.objects.get(user=request.user)
    error = False
    valider = False
    if request.method == "POST":
        form = ModificationForm(request.POST)
        if form.is_valid():
            addresse = form.cleaned_data["addresse"]
            email = form.cleaned_data["email"]
            telephone = form.cleaned_data["telephone"]
            u = request.user
            u.email = email
            u.save()
            utilisateur = Utilisateur.objects.get(user=u)
            utilisateur.telephone = telephone
            utilisateur.adresse = addresse
            utilisateur.save()
            valider = True

    else:
        form = ModificationForm(request.user)

    return render(request, "MonCompte.html", locals())


@login_required
def MesDemande(request):
    commandes = Commande.objects.filter(user=request.user, complete=True)
    ListePanier = []
    ListePanierBis = []
    for commande in commandes:
        produits = Panier.objects.filter(idcommande=Commande.objects.get(pk=commande.id))
        utilisateur = Utilisateur.objects.get(user=commande.user)
        prix = 0
        for p in produits:
            prix += p.quantite * p.produits.prix
        a = {"user": utilisateur, "Paniers": produits, "prix": prix}

        if commande.enattente:
            ListePanierBis.append(a)

        ListePanier.append(a)

    return render(request, 'MesDemands.html', locals())


@login_required
def CommandeValider(request):
    if request.method == "POST":
        id = request.POST['idcommande']
        commande = Commande.objects.get(pk=id)
        commande.complete = True
        commande.save()

    else:
        pass
    return render(request, 'commandecomplete.html', locals())


class FoliumView(TemplateView):
    template_name = "geomap.html"

    def get_context_data(self, **kwargs):
        figure = folium.Figure()
        m = folium.Map(
            location=[48.88161719999999, 2.3033608],
            zoom_start=10,

        )
        m.add_to(figure)
        utilisateurs = Utilisateur.objects.all()
        for utilisateur in utilisateurs:
            adresse = utilisateur.adresse
            coordonnees = [adresse.latitude, adresse.longitude]
            nombredecommande = Commande.objects.filter(user=utilisateur.user).count()
            if nombredecommande >= 10:
                color = "red"
            elif nombredecommande >= 2:
                color = "orange"
            else:
                color = "green"

            folium.Marker(
                location=coordonnees,
                popup=utilisateur.user.first_name,
                icon=folium.Icon(icon='user', color=color)

            ).add_to(m)

        figure.render()
        return {"map": figure}


@login_required
def ListeDemande(request):
    if request.method == "POST":
        commande = Commande.objects.get(pk=request.POST['idcommande'])
        commande.enattente = False
        commande.save()
    commandes = Commande.objects.filter(complete=True, enattente=True)
    ListePanier = []
    for commande in commandes:
        utilisateur = Utilisateur.objects.get(user=commande.user)
        ListePanier.append(
            {"user": utilisateur, "Paniers": Panier.objects.filter(idcommande=Commande.objects.get(pk=commande.id))})

    return render(request, 'listedemande.html', locals())


def inscription(request):
    error = False
    valider = False
    if request.method == "POST":
        form = InscriptionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            prenom = form.cleaned_data["prenom"]
            nom = form.cleaned_data["nom"]
            password = form.cleaned_data["password"]
            password2 = form.cleaned_data["password2"]
            addresse = form.cleaned_data["addresse"]
            email = form.cleaned_data["email"]
            telephone = form.cleaned_data["telephone"]
            if password != password2:
                errormdp = True
            else:
                try:
                    t = Utilisateur.objects.get(adresseip=request.META.get('REMOTE_ADDR'))
                    errorip = True

                except:
                    u = User.objects.create_user(username, email, password, first_name=prenom, last_name=nom)
                    u.save()
                    utilisateur = Utilisateur(telephone=telephone, adresse=addresse, user=u,
                                              adresseip=request.META.get('REMOTE_ADDR'))
                    utilisateur.save()
                    valider = True

    else:
        form = InscriptionForm()

    return render(request, 'signup.html', locals())


def connexion(request):
    error = False

    if request.method == "POST":
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes
            if user:  # Si l'objet renvoyé n'est pas None
                login(request, user)  # nous connectons l'utilisateur
            else:  # sinon une erreur sera affichée
                error = True
    else:
        form = ConnexionForm()

    return render(request, 'signin.html', locals())


@login_required
def deconnexion(request):
    logout(request)
    return redirect(Accueil)
