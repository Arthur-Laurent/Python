# Python


## Requis :

PIP , Annaconda

## Installation

* Dans la console annaconda effectuer `pip install -r requirements.txt` (le fichier requirements.txt est disponible dans le dossier)

* Se rendre dans `Python/sitepython/settings.py`

* Ligne 79 modifier les identifiants mysql et la base de donnée.

* Dans annaconda se rendre dans le repertoire ou se trouve manage.py 

* Taper `python manage.py makemigrations` ( va permettre de generer le code permettant de generer la base de donnée )

* Taper `python manage.py migrate` ( va creer la base de donnée ) 

* Taper `python manage.py createsuperuser` ( va permettre de creer un utilisateur pour acceder à l'interface d'administration du site )
via <localhost:8000/admin>

* Taper `python manage.py runserver` ( lance le site en local on peut y acceder par <localhost:8000/Site/Accueil> )


