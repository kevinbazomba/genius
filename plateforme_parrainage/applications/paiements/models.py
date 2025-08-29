from django.db import models
from django.conf import settings

from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid

class Depot(models.Model):
    STATUT_CHOIX = [
        ('en_attente', 'En attente'),
        ('confirme', 'Confirmé'),
        ('rejete', 'Rejeté'),
    ]

    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='depots')
    montant = models.DecimalField(max_digits=12, decimal_places=2)
    methode = models.CharField(max_length=32)
    statut = models.CharField(max_length=12, choices=STATUT_CHOIX, default='confirme')  # Statut par défaut : 'confirme'
    reference = models.CharField(max_length=64, unique=True, null=True, blank=True)
    cree_le = models.DateTimeField(auto_now_add=True)
    confirme_le = models.DateTimeField( null=True, blank=True)  # Date de confirmation automatique

    def save(self, *args, **kwargs):
        # Générer une référence unique si aucune n'est fournie
        if not self.reference:
            self.reference = str(uuid.uuid4())
        # Définir le statut à 'confirme' et la date de confirmation
        if self.statut == 'confirme' and not self.confirme_le:
            self.confirme_le = timezone.now()

        super().save(*args, **kwargs)
     

    def __str__(self):
        return f"Dépôt de {self.montant} FC par {self.utilisateur.email} ({self.get_statut_display()})"

class Retrait(models.Model):
    """Modèle pour les retraits."""
    STATUT_CHOIX = [
        ('demande', 'Demandé'),
        ('en_traitement', 'En traitement'),
        ('paye', 'Payé'),
        ('rejete', 'Rejeté'),
    ]

    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='retraits', verbose_name="Utilisateur")
    montant = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Montant")
    methode = models.CharField(max_length=32, verbose_name="Méthode de retrait")
    destination = models.CharField(max_length=128, verbose_name="Destination (numéro de compte/téléphone)")
    statut = models.CharField(max_length=13, choices=STATUT_CHOIX, default='demande', verbose_name="Statut")
    cree_le = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    traite_le = models.DateTimeField(null=True, blank=True, verbose_name="Date de traitement")

    def __str__(self):
        return f"Retrait de {self.montant} FC par {self.utilisateur.email} ({self.get_statut_display()})"
