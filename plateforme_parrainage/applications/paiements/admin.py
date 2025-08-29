from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Depot, Retrait


@admin.register(Depot)
class DepotAdmin(admin.ModelAdmin):
    """Configuration de l'administration pour le modèle Dépôt."""
    list_display = ("utilisateur", "montant", "methode", "statut", "reference", "cree_le", "confirme_le")
    search_fields = ("utilisateur__email", "reference", "methode")
    list_filter = ("statut", "methode", "cree_le")
    ordering = ("-cree_le",)
    readonly_fields = ("reference", "statut", "cree_le", "confirme_le")

    def get_readonly_fields(self, request, obj=None):
        """Empêcher la modification du statut après création."""
        if obj:  # si l'objet existe déjà
            return self.readonly_fields + ("montant", "utilisateur", "methode")
        return self.readonly_fields


@admin.register(Retrait)
class RetraitAdmin(admin.ModelAdmin):
    """Configuration de l'administration pour le modèle Retrait."""
    list_display = ("utilisateur", "montant", "methode", "destination", "statut", "cree_le", "traite_le")
    search_fields = ("utilisateur__email", "destination", "methode")
    list_filter = ("statut", "methode", "cree_le")
    ordering = ("-cree_le",)
    readonly_fields = ("cree_le",)

    def save_model(self, request, obj, form, change):
        """Met à jour automatiquement la date de traitement quand le statut change."""
        if change and obj.statut in ["paye", "rejete", "en_traitement"] and obj.traite_le is None:
            from django.utils import timezone
            obj.traite_le = timezone.now()
        super().save_model(request, obj, form, change)
