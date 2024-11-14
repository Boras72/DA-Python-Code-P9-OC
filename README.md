# BooksReview

BooksReview est une application web Django permettant aux utilisateurs de créer, éditer et supprimer des critiques de livres. Les utilisateurs peuvent également suivre d'autres utilisateurs et voir leurs critiques dans un flux personnalisé.


## Prérequis

- Python 3.x
- Django 3.x
- SQLite (ou tout autre SGBD compatible avec Django)


## Installation

    1.  Clonez le dépôt :

    ```
    git clone https://github.com/Boras72/DA-Python-Code-P9-OC.git
    cd BooksReview
    ```

    2.  Créez et activez un environnement virtuel :

    ```
    python -m venv env
    source env/bin/activate            # Sur Windows, utilisez `env\Scripts\activate`
    ```

    3.  Installez les dépendances :

    ```
    pip install -r requirements.txt
    ```

    4. Créer et appliquer les fichiers de migration basés sur les modèles de l'application afin d'initialiser de la base de données
    ```
    python manage.py migrate
    python manage.py makemigrations
    ```

    5.  Créez un superutilisateur pour accéder à l'interface d'administration :

    ```
    python manage.py createsuperuser
    ```


## Utilisation

Pour lancer le serveur de développement, assurez-vous que l'environnement virtuel est activé, puis exécutez la commande suivante dans votre terminal :
```
python manage.py runserver
```
Puis accédez à l'application dans votre navigateur en cliquant sur l'adresse (Ctrl+C) :
```
`http://127.0.0.1:8000/`
```


### Fonctionnalités principales

- **Créer une critique** : Les utilisateurs peuvent créer des critiques pour des livres.
- **Éditer une critique** : Les utilisateurs peuvent éditer leurs propres critiques.
- **Supprimer une critique** : Les utilisateurs peuvent supprimer leurs propres critiques.
- **Suivre des utilisateurs** : Les utilisateurs peuvent suivre d'autres utilisateurs pour voir leurs critiques dans un flux personnalisé.
- **Voir le flux** : Les utilisateurs peuvent voir les critiques des utilisateurs qu'ils suivent.


### Routes principales

- `/feed/` : Affiche le flux des critiques des utilisateurs suivis.
- `/posts/` : Affiche les critiques de l'utilisateur connecté.
- `/subscriptions/` : Affiche les abonnements de l'utilisateur connecté.
- `/follow/<int:user_id>/` : Permet de suivre un utilisateur.
- `/unfollow/<int:user_id>/` : Permet de ne plus suivre un utilisateur.
- `/ticket/create/` : Permet de créer un ticket de critique.
- `/ticket/edit/<int:ticket_id>/` : Permet d'éditer un ticket de critique.
- `/ticket/delete/<int:ticket_id>/` : Permet de supprimer un ticket de critique.
- `/review/create/<int:ticket_id>/` : Permet de créer une critique pour un ticket existant.
- `/review/create/` : Permet de créer une critique indépendante.
- `/ticket-review/create/` : Permet de créer un ticket et une critique en même temps.


## Tests

Pour exécuter les tests, utilisez la commande suivante :
```
python manage.py test
 ```

## Contribuer

Les contributions sont les bienvenues ! Pour contribuer :
    1. Forkez le projet.
    2. Créez une branche pour votre fonctionnalité (git checkout -b feature/ma-fonctionnalite).
    3. Commitez vos modifications (git commit -am 'Ajoute une nouvelle fonctionnalité').
    4. Poussez votre branche (git push origin feature/ma-fonctionnalite).
    5. Ouvrez une Pull Request.


## Licence

Ce projet est sous licence Opensource. Veuillez consulter le fichier LICENSE pour plus d'informations.


## Auteurs

    • Boras72 : https://github.com/Boras72



