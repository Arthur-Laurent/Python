from django import forms
from .models import *
from django.forms import ModelForm
from address.forms import AddressField
from django.contrib.auth.models import User


class ConnexionForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)


class InscriptionForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length="150", required=True, min_length="6")
    prenom = forms.CharField(label="Prénom", max_length="150", required=True, min_length="6")
    nom = forms.CharField(label='Nom', max_length="150", required=True, min_length="6")
    password = forms.CharField(label='Mot de passe', max_length="150", required=True, min_length="6",
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Mot de passe', max_length="150", required=True, min_length="6",
                                widget=forms.PasswordInput)
    addresse = AddressField(required=True)
    email = forms.EmailField(label="Adresse email", required=True)
    telephone = forms.CharField(label='Numéro de teléphone', min_length="10", required=True, max_length="10",
                                widget=forms.NumberInput)


class ModificationForm(forms.Form):
    addresse = AddressField(required=True)
    email = forms.EmailField(label="Adresse email", required=True)
    telephone = forms.CharField(label='Numéro de teléphone', min_length="10", required=True, max_length="10",
                                widget=forms.NumberInput)
