from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from applications.comptes.models import ProfilUtilisateur
from .models import BonusParrainage

@login_required
def afficher_code_parrainage(request):
    """Affiche le code de parrainage de l'utilisateur connecté."""
    code_parrainage = request.user.profil.code_parrainage
    lien_parrainage = f"{request.scheme}://{request.get_host()}/comptes/inscription/?code_parrain={code_parrainage}"
    return render(request, 'parrainages/mon_code.html', {
        'code_parrainage': code_parrainage,
        'lien_parrainage': lien_parrainage
    })

@login_required
def liste_filleuls(request):
    """Affiche la liste des filleuls de l'utilisateur connecté."""
    # On filtre les Bonus où l'utilisateur est parrain
    filleuls = (
        BonusParrainage.objects
        .filter(parrain=request.user)
        .select_related("filleul")  # optimisation
    )

    # On récupère directement les Users (filleuls)
    users_filleuls = [bonus.filleul for bonus in filleuls]

    return render(request, 'parrainages/mes_invites.html', {'filleuls': users_filleuls})



@login_required
def liste_bonus_parrainage(request):
    """Affiche la liste des bonus de parrainage reçus."""
    bonus = BonusParrainage.objects.filter(parrain=request.user).order_by('-cree_le')
    total_bonus = sum(bonus.montant for bonus in bonus)
    return render(request, 'parrainages/bonus.html', {'bonus': bonus, 'total_bonus':total_bonus})
