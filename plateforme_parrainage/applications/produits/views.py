from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Produit, Achat
from django.contrib import messages
from datetime import timedelta
from django.utils import timezone
from applications.portefeuille.models import TransactionPortefeuille
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Produit, Achat
from applications.portefeuille.models import TransactionPortefeuille
from decimal import Decimal
from django.utils import timezone


@login_required
def vue_liste_produits(request):
    """Vue pour lister les produits disponibles."""
    produits = Produit.objects.filter(est_actif=True)
    return render(request, 'produits/liste.html', {'produits': produits})



@login_required
def vue_achat(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    gain_a = float(produit.prix) * float(produit.taux_quotidien)
    gain = int(gain_a)
    gain_total_b = float(produit.prix) * float(produit.taux_quotidien) * float(produit.duree_jours)
    gain_total = int(gain_total_b)
    solde = request.user.profil.get_solde()

    if request.method == 'POST':
        # Vérifier que le solde est suffisant
        if solde < produit.prix:
            messages.error(request, f"Solde insuffisant pour effectuer cet achat. {solde} FC")
            #return redirect('liste_produits')
            return render(request, 'produits/achat.html', {'produit': produit, 'solde': solde, 'gain':gain, 'gain_total':gain_total})

        # Vérifier que le prix est supérieur à 0
        if produit.prix <= 0:
            messages.error(request, "Le prix de cette marchandise est invalide.")
            #return redirect('liste_produits')
            return render(request, 'produits/achat.html', {'produit': produit, 'solde': solde, 'gain':gain, 'gain_total':gain_total})

        # Créer l'achat
        achat = Achat.objects.create(
            utilisateur=request.user,
            produit=produit,
            prix_au_moment_achat=produit.prix,
            date_fin=timezone.now().date() + timezone.timedelta(days=produit.duree_jours)
        )

        # Créer une transaction pour déduire le montant du solde
        nouveau_solde = solde - produit.prix
        TransactionPortefeuille.objects.create(
            utilisateur=request.user,
            type='achat',
            montant=-produit.prix,  # Montant négatif pour indiquer une sortie
            reference=f"Achat de {produit.nom} (ID: {achat.id})",
            solde_apres=nouveau_solde
        )

        messages.success(request, f"Achat de {produit.nom} effectué avec succès !")
        return redirect('mes_investissements')

    return render(request, 'produits/achat.html', {'produit': produit, 'solde': solde, 'gain':gain, 'gain_total':gain_total})



@login_required
def mes_investissements(request):
    """Affiche les produits achetés et les bénéfices générés."""
    achats = Achat.objects.filter(utilisateur=request.user).order_by('-date_debut')

    investissements = []
    for achat in achats:
        # Calculer le total des gains quotidiens pour cet achat spécifique
        total_gains = sum(gain.montant for gain in achat.gains_quotidiens.all())

        # Calculer le bénéfice net pour cet achat
        benefice_net = total_gains - achat.prix_au_moment_achat

        # Calculer les jours restants pour cet achat
        jours_restants = (achat.date_fin - timezone.now().date()).days if achat.statut == 'actif' else 0

        investissements.append({
            'achat': achat,
            'total_gains': total_gains,
            'benefice_net': benefice_net,
            'jours_restants': jours_restants,
            'taux_quotidien': achat.produit.taux_quotidien,
        })

    total_investi = sum(Decimal(achat.prix_au_moment_achat) for achat in achats)
    total_benefices = sum(inv['total_gains'] for inv in investissements)

    # Calculer le rendement en pourcentage
    rendement = 0
    if total_investi > 0:
        rendement = float(total_benefices) / float(total_investi) * 100

    context = {
        'investissements': investissements,
        'total_benefices': total_benefices,
        'total_investi': total_investi,
        'rendement': rendement,
    }
    return render(request, 'produits/mes_investissements.html', context)



"""
/* Media Query spécifique pour 1792×828 */
        @media screen and (min-width: 800px) and (max-width: 900px) and (min-height: 800px) and (max-height: 900px) {
            .container {
                padding: 0 40px;
                max-width: 800px;
            }
            
            .hero h1 {
                font-size: 1.9rem;
            }
            
            .product-section {
                flex-direction: row;
                align-items: flex-start;
            }
            
            .product-image {
                width: 45%;
                height: 380px;
            }
            
            .product-details {
                width: 55%;
                padding-left: 30px;
            }
            
            .benefits-grid {
                flex-direction: row;
                flex-wrap: wrap;
            }
            
            .benefit-card {
                flex: 1;
                min-width: 280px;
            }
        }
        
        /* Styles pour les très petits écrans */
        @media screen and (max-width: 360px) {
            .container {
                padding: 0 16px;
            }
            
            .hero h1 {
                font-size: 1.5rem;
            }
            
            .product-image {
                height: 280px;
            }
        }
"""