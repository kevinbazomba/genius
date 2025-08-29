from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Order, PaymentMessage

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('reference_code_display', 'customer_name_display', 'amount_display', 'is_paid_display', 'created_at_display')
    list_filter = ('is_paid', 'created_at')
    search_fields = ('reference_code', 'customer_name')
    readonly_fields = ('created_at',)
    list_per_page = 20
    ordering = ('-created_at',)
    
    fieldsets = (
        (_('Informations de commande'), {
            'fields': ('customer_name', 'amount', 'reference_code', 'is_paid')
        }),
        (_('Dates'), {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def reference_code_display(self, obj):
        return obj.reference_code if obj.reference_code else _("—")
    reference_code_display.short_description = _("Code de référence")
    
    def customer_name_display(self, obj):
        return obj.customer_name if obj.customer_name else _("—")
    customer_name_display.short_description = _("Nom du client")
    
    def amount_display(self, obj):
        return f"{obj.amount} CDF"
    amount_display.short_description = _("Montant")
    
    def is_paid_display(self, obj):
        return _("Payée") if obj.is_paid else _("En attente")
    is_paid_display.short_description = _("Statut")
    
    def created_at_display(self, obj):
        return obj.created_at.strftime("%d/%m/%Y %H:%M")
    created_at_display.short_description = _("Date de création")

@admin.register(PaymentMessage)
class PaymentMessageAdmin(admin.ModelAdmin):
    list_display = ('reference_display', 'sender_display', 'amount_display', 'processed_display', 'received_at_display')
    list_filter = ('processed', 'received_at')
    search_fields = ('reference', 'sender', 'sms_text')
    readonly_fields = ('received_at', 'sms_text', 'sender', 'amount', 'reference', 'error')
    list_per_page = 20
    ordering = ('-received_at',)
    
    fieldsets = (
        (_('Contenu du SMS'), {
            'fields': ('sms_text', 'sender', 'received_at')
        }),
        (_('Données extraites'), {
            'fields': ('amount', 'reference')
        }),
        (_('Statut de traitement'), {
            'fields': ('processed', 'error')
        }),
    )
    
    def reference_display(self, obj):
        return obj.reference if obj.reference else _("—")
    reference_display.short_description = _("Référence")
    
    def sender_display(self, obj):
        return obj.sender if obj.sender else _("—")
    sender_display.short_description = _("Expéditeur")
    
    def amount_display(self, obj):
        return f"{obj.amount} CDF" if obj.amount else _("—")
    amount_display.short_description = _("Montant")
    
    def processed_display(self, obj):
        return _("Traité") if obj.processed else _("Non traité")
    processed_display.short_description = _("Traité")
    
    def received_at_display(self, obj):
        return obj.received_at.strftime("%d/%m/%Y %H:%M")
    received_at_display.short_description = _("Reçu le")
    
    def has_add_permission(self, request):
        # Empêcher l'ajout manuel de messages de paiement
        return False
    
    def has_change_permission(self, request, obj=None):
        # Permettre seulement de marquer comme traité ou d'ajouter une erreur
        return True
    
    def has_delete_permission(self, request, obj=None):
        return True