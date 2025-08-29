from django.db import models
from django.conf import settings

class BonusParrainage(models.Model):
    """Modèle pour les bonus de parrainage."""
    parrain = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bonus_parrainages', verbose_name="Parrain")
    filleul = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bonus_parrain', verbose_name="Filleul")
    depot = models.OneToOneField('paiements.Depot', on_delete=models.CASCADE, verbose_name="Dépôt associé")
    montant = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Montant du bonus")
    cree_le = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    def __str__(self):
        return f"Bonus de {self.montant} FC pour {self.parrain.email} (filleul: {self.filleul.email})"
