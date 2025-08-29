from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from applications.portefeuille.models import TransactionPortefeuille
from applications.produits.models import Achat
from applications.paiements.models import Depot
from django.utils import timezone
from django.shortcuts import render

from applications.comptes.models import ProfilUtilisateur

def vue_accueil(request):
    """Vue pour la page d'accueil."""
    return render(request, 'noyau/accueil.html')

@login_required
def vue_tableau_de_bord(request):
    
    try:
            """Vue pour le tableau de bord utilisateur avec données dynamiques."""
            # Récupérer les transactions récentes
            transactions = TransactionPortefeuille.objects.filter(utilisateur=request.user).order_by('-cree_le')
            solde = request.user.profil.get_solde()
        
            # Calculer le solde (exemple simplifié)
            #solde = sum(t.montant for t in TransactionPortefeuille.objects.filter(utilisateur=request.user, type__in=['depot', 'gain_quotidien', 'bonus_parrainage'])) - sum(t.montant for t in TransactionPortefeuille.objects.filter(utilisateur=request.user, type='retrait'))

            # Calculer les gains d'aujourd'hui
            gains_aujourdhui = sum(t.montant for t in TransactionPortefeuille.objects.filter(utilisateur=request.user, type='gain_quotidien', cree_le__date=timezone.now().date()))

            # Calculer le total des dépôts
            total_depots = sum(d.montant for d in Depot.objects.filter(utilisateur=request.user, statut='confirme'))

            # Récupérer les achats actifs
            achats_actifs = Achat.objects.filter(utilisateur=request.user, statut='actif')

            return render(request, 'noyau/tableau_de_bord.html', {
                'transactions': transactions,
                'solde': solde,
                'gains_aujourdhui': gains_aujourdhui,
                'total_depots': total_depots,
                'achats_actifs': achats_actifs,
            })

        
    except ProfilUtilisateur.DoesNotExist:
        messages.error(request, "Votre profil n'existe pas. Il va être créé.")
        ProfilUtilisateur.objects.create(utilisateur=request.user)
        solde = 0

    return render(request, 'noyau/tableau_de_bord.html', {'solde': solde})




def vue_connexion(request):
    """Vue pour la connexion des utilisateurs."""
    if request.method == 'POST':
        email = request.POST.get('email')
        mot_de_passe = request.POST.get('mot_de_passe')
        utilisateur = authenticate(request, username=email, password=mot_de_passe)
        if utilisateur is not None:
            login(request, utilisateur)
            return redirect('tableau_de_bord')
        else:
            messages.error(request, "Nom ou mot de passe incorrect.")
    return render(request, 'noyau/connexion.html')

def vue_deconnexion(request):
    """Vue pour la déconnexion."""
    logout(request)
    return redirect('accueil')


