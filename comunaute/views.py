from django.shortcuts import render
from .models import *
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User, UserManager
from address.forms import AddressField
from django.shortcuts import redirect, get_object_or_404, render
from .forms import ConnexionForm, InscriptionForm
from django.views.generic import CreateView, UpdateView
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone


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


    else:
        pass

    return render(request, "Test.html", locals())


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
            addresse = form.cleaned_data["addresse"]
            email = form.cleaned_data["email"]
            telephone = form.cleaned_data["telephone"]
            u = User.objects.create_user(username, email, password, first_name=prenom, last_name=nom)
            u.save()
            utilisateur = Utilisateur(telephone=telephone, adresse=addresse, user=u)
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

# Create your views here.
