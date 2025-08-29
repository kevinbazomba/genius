from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import BonusParrainage


@admin.register(BonusParrainage)
class BonusParrainageAdmin(admin.ModelAdmin):
    """Configuration de l'administration pour les bonus de parrainage."""
    list_display = ("parrain", "filleul", "depot", "montant", "cree_le")
    search_fields = ("parrain__email", "filleul__email", "depot__reference")
    list_filter = ("cree_le",)
    ordering = ("-cree_le",)
    readonly_fields = ("cree_le",)

    def get_queryset(self, request):
        """Optimise les requêtes avec select_related."""
        qs = super().get_queryset(request)
        return qs.select_related("parrain", "filleul", "depot")
