from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Utilisateur, ProfilUtilisateur
from django.contrib import messages


@require_http_methods(["GET", "POST"])
def vue_inscription(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        telephone = request.POST.get('telephone')
        mot_de_passe = request.POST.get('mot_de_passe')
        code_parrain = request.POST.get('code_parrain', '')

        if Utilisateur.objects.filter(email=email).exists():
            messages.error(request, "Cet nom est déjà utilisé.")
            return redirect('inscription')

        if Utilisateur.objects.filter(telephone=telephone).exists():
            messages.error(request, "Ce numéro de téléphone est déjà utilisé.")
            return redirect('inscription')
        try:
                # Création de l'utilisateur
                utilisateur = Utilisateur.objects.create_user(
                    email=email,
                    telephone=telephone,
                    password=mot_de_passe,
                    username=email
                )

                # Création du profil utilisateur (seulement si nécessaire)
                ProfilUtilisateur.objects.get_or_create(utilisateur=utilisateur)

                # Association avec un parrain si un code est fourni
                if code_parrain:
                    try:
                        parrain_profil = ProfilUtilisateur.objects.get(code_parrainage=code_parrain)
                        utilisateur.profil.parrain = parrain_profil.utilisateur
                        utilisateur.profil.save()
                    except ProfilUtilisateur.DoesNotExist:
                        messages.error(request, "Code de parrain invalide.")
                        return render(request, 'comptes/inscription.html')

                # Connexion automatique après inscription
                utilisateur = authenticate(request, username=email, password=mot_de_passe)
                if utilisateur is not None:
                    login(request, utilisateur)
                    return redirect('tableau_de_bord')
        except :
            messages.error(request, "Le nom existe déjà ajoute un symbole.")
            return render(request, 'comptes/inscription.html')

    return render(request, 'comptes/inscription.html')


@login_required
def vue_ajouter_code_parrain(request):
    """Vue pour ajouter un code de parrain dans les 24h."""
    if request.method == 'POST':
        code_parrain = request.POST.get('code_parrain')
        try:
            parrain = ProfilUtilisateur.objects.get(code_parrainage=code_parrain)
            if not request.user.profil.verrouillage_parrainage_le:
                request.user.profil.parrain = parrain.utilisateur
                request.user.profil.save()
                messages.success(request, "Code de parrain ajouté avec succès !")
            else:
                messages.error(request, "Vous ne pouvez plus ajouter de code de parrain.")
        except ProfilUtilisateur.DoesNotExist:
            messages.error(request, "Code de parrain invalide.")

    return render(request, 'comptes/ajouter_code_parrain.html')




