from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from applications.shop.models import Order
from .models import Depot, Retrait
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Depot
from applications.portefeuille.models import TransactionPortefeuille
from django.contrib import messages
from django.db import IntegrityError
import uuid

"""@login_required
def vue_depot(request):
    if request.method == 'POST':
        montant = Decimal(request.POST.get('montant'))
        methode = request.POST.get('methode')
        reference = request.POST.get('reference', '')

        try:
            # Créer le dépôt (il sera automatiquement validé grâce au modèle)
            depot = Depot.objects.create(
                utilisateur=request.user,
                montant=montant,
                methode=methode,
                reference=reference
            )

            # Créditer le portefeuille de l'utilisateur
            TransactionPortefeuille.objects.create(
                utilisateur=request.user,
                type='depot',
                montant=montant,
                reference=f"Dépôt {depot.reference}",
                solde_apres=request.user.profil.get_solde() + montant
            )

            messages.success(request, "Dépôt effectué avec succès ! Votre compte a été crédité.")
            return redirect('liste_depots')
        except IntegrityError:
            messages.error(request, "Une erreur est survenue. Veuillez réessayer.")
            return redirect('depot')
    return render(request, 'paiements/depot.html')"""

"""
@login_required
def vue_retrait(request):
    Vue pour créer une demande de retrait.
    if request.method == 'POST':
        montant = request.POST.get('montant')
        methode = request.POST.get('methode')
        destination = request.POST.get('destination')

        Retrait.objects.create(
            utilisateur=request.user,
            montant=montant,
            methode=methode,
            destination=destination
        )
        messages.success(request, "Demande de retrait envoyée avec succès !")
        return redirect('liste_retraits')

    return render(request, 'paiements/retrait.html')"""

# applications/paiements/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def vue_retrait(request):
    """Vue pour créer une demande de retrait."""
    solde = request.user.profil.get_solde()

    if request.method == 'POST':
        try:
            montant = Decimal(request.POST.get('montant', 0))
            methode = request.POST.get('methode')
            destination = request.POST.get('destination')

            if montant <= 0:
                messages.error(request, f"Le montant doit être supérieur à zéro.\nsolde:{solde} CDF")
                return redirect('retrait')

            if montant < 5000:
                messages.error(request, f"Le montant minimum pour un retrait est de 5000 FC.\nsolde:{solde} CDF")
                return redirect('retrait')

            if solde < montant:
                messages.error(request, f"Solde insuffisant pour effectuer ce retrait.\nsolde:{solde} CDF")
                return redirect('retrait')

            if request.method == 'POST':
                    montant = request.POST.get('montant')
                    methode = request.POST.get('methode')
                    destination = request.POST.get('destination')

                    Retrait.objects.create(
                        utilisateur=request.user,
                        montant=montant,
                        methode=methode,
                        destination=destination
                    )
    
            messages.success(request, "Demande de retrait envoyée avec succès !")
            return redirect('liste_retraits')

        except ValueError:
            messages.error(request, "Montant invalide. Veuillez entrer un montant valide.")
            return redirect('retrait')

    return render(request, 'paiements/retrait.html', {'solde': solde})



@login_required
def liste_depots(request):
    """Affiche la liste des dépôts de l'utilisateur connecté."""
    depots = Depot.objects.filter(utilisateur=request.user).order_by('-cree_le')
    return render(request, 'paiements/liste_depots.html', {'depots': depots})


@login_required
def liste_retraits(request):
    retraits = Retrait.objects.filter(utilisateur=request.user).order_by('-cree_le')
    return render(request, 'paiements/liste_retraits.html', {'retraits': retraits})
