from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def accueil_view(request):
    # Vous pouvez ajouter ici toute logique nécessaire pour la page d'accueil, par exemple, récupérer des données à afficher sur la page

    context = {
        'titre': 'Bienvenue sur LITReviews',
        'message': 'Découvrez et partagez des critiques littéraires passionnantes !',
    }
    return render(request, 'accueil.html', context)

