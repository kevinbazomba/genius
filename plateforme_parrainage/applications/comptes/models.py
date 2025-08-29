from decimal import Decimal
from django.contrib.auth.models import AbstractUser
from django.db import models
import random
import string
    
from django.db import models
from applications.portefeuille.models import TransactionPortefeuille

def generer_code_parrainage():
    """Génère un code de parrainage aléatoire unique."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

class Utilisateur(AbstractUser):
    """Modèle Utilisateur personnalisé avec champ téléphone."""
    telephone = models.CharField(max_length=20, unique=True, verbose_name="Numéro de téléphone")

    def __str__(self):
        return self.email

class ProfilUtilisateur(models.Model):
    """Profil utilisateur avec code de parrainage et parrain."""
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name='profil', verbose_name="Utilisateur")
    code_parrainage = models.CharField(max_length=12, unique=True, default=generer_code_parrainage, verbose_name="Code de parrainage")
    parrain = models.ForeignKey(Utilisateur, null=True, blank=True, on_delete=models.SET_NULL, related_name='filleuls', verbose_name="Parrain")
    verrouillage_parrainage_le = models.DateTimeField(null=True, blank=True, verbose_name="Date de verrouillage du parrainage")
    niveau_kyc = models.IntegerField(default=0, verbose_name="Niveau KYC")
    double_authentification_active = models.BooleanField(default=False, verbose_name="Double authentification activée")



   
    def get_solde(self):
        """Calcule et retourne le solde actuel de l'utilisateur."""
        depots = sum(Decimal(t.montant) for t in TransactionPortefeuille.objects.filter(utilisateur=self.utilisateur, type='depot'))
        gains = sum(Decimal(t.montant) for t in TransactionPortefeuille.objects.filter(utilisateur=self.utilisateur, type='gain_quotidien'))
        bonus = sum(Decimal(t.montant) for t in TransactionPortefeuille.objects.filter(utilisateur=self.utilisateur, type='bonus_parrainage'))
        retraits = sum(Decimal(t.montant) for t in TransactionPortefeuille.objects.filter(utilisateur=self.utilisateur, type='retrait'))
        achats = sum(Decimal(t.montant) for t in TransactionPortefeuille.objects.filter(utilisateur=self.utilisateur, type='achat'))

        solde = (depots + gains + bonus) - retraits - abs(achats)
        return solde


    
    def __str__(self):
        return f"Profil de {self.utilisateur.email}"



