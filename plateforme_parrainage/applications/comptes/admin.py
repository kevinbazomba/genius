from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Utilisateur, ProfilUtilisateur


@admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):
    """Configuration de l'administration pour le modèle Utilisateur."""
    list_display = ("username", "email", "telephone", "is_active", "is_staff", "date_joined")
    search_fields = ("username", "email", "telephone")
    list_filter = ("is_active", "is_staff", "is_superuser", "date_joined")
    ordering = ("-date_joined",)


@admin.register(ProfilUtilisateur)
class ProfilUtilisateurAdmin(admin.ModelAdmin):
    """Configuration de l'administration pour le modèle ProfilUtilisateur."""
    list_display = ("utilisateur", "code_parrainage", "parrain", "niveau_kyc", "double_authentification_active", "get_solde")
    search_fields = ("utilisateur__email", "utilisateur__telephone", "code_parrainage")
    list_filter = ("niveau_kyc", "double_authentification_active")
    readonly_fields = ("code_parrainage", "get_solde", "verrouillage_parrainage_le")

    def get_solde(self, obj):
        return f"{obj.get_solde()} FCFA"
    get_solde.short_description = "Solde actuel"
