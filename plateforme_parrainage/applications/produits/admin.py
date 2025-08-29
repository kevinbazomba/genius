from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Produit, Achat, GainQuotidien


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    """Configuration de l'administration pour les produits."""
    list_display = ("nom", "prix", "duree_jours", "taux_quotidien", "est_actif")
    search_fields = ("nom", "description")
    list_filter = ("est_actif",)
    ordering = ("nom",)


@admin.register(Achat)
class AchatAdmin(admin.ModelAdmin):
    """Configuration de l'administration pour les achats."""
    list_display = ("utilisateur", "produit", "prix_au_moment_achat", "date_debut", "date_fin", "jours_payes", "statut")
    search_fields = ("utilisateur__email", "produit__nom")
    list_filter = ("statut", "produit", "date_debut")
    ordering = ("-date_debut",)
    readonly_fields = ("date_debut",)

    def get_queryset(self, request):
        """Optimisation avec select_related."""
        qs = super().get_queryset(request)
        return qs.select_related("utilisateur", "produit")


@admin.register(GainQuotidien)
class GainQuotidienAdmin(admin.ModelAdmin):
    """Configuration de l'administration pour les gains quotidiens."""
    list_display = ("achat", "jour", "montant", "poste", "poste_le")
    search_fields = ("achat__utilisateur__email", "achat__produit__nom")
    list_filter = ("poste", "jour")
    ordering = ("-jour",)
    readonly_fields = ("poste_le",)

    def get_queryset(self, request):
        """Optimisation avec select_related."""
        qs = super().get_queryset(request)
        return qs.select_related("achat", "achat__produit", "achat__utilisateur")
