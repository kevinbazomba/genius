from django.db import models
from django.conf import settings

class TransactionPortefeuille(models.Model):
    """Modèle pour les transactions du portefeuille."""
    TYPE_CHOIX = [
        ('depot', 'Dépôt'),
        ('retrait', 'Retrait'),
        ('gain_quotidien', 'Gain quotidien'),
        ('bonus_parrainage', 'Bonus parrainage'),
        ('achat', 'Achat marchandise'),
    ]

    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='transactions', verbose_name="Utilisateur")
    type = models.CharField(max_length=24, choices=TYPE_CHOIX, verbose_name="Type de transaction")
    montant = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Montant")
    reference = models.CharField(max_length=64, null=True, blank=True, verbose_name="Référence")
    cree_le = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    solde_apres = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Solde après transaction")

    def __str__(self):
        return f"{self.utilisateur.email} - {self.get_type_display()} - {self.montant} FC"
