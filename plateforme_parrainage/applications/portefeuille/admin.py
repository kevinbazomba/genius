from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import TransactionPortefeuille


@admin.register(TransactionPortefeuille)
class TransactionPortefeuilleAdmin(admin.ModelAdmin):
    """Configuration de l'administration pour les transactions du portefeuille."""
    list_display = ("utilisateur", "type", "montant", "solde_apres", "reference", "cree_le")
    search_fields = ("utilisateur__email", "reference", "type")
    list_filter = ("type", "cree_le")
    ordering = ("-cree_le",)
    readonly_fields = ("cree_le",)

    def get_queryset(self, request):
        """Optimisation avec select_related pour l'utilisateur."""
        qs = super().get_queryset(request)
        return qs.select_related("utilisateur")
