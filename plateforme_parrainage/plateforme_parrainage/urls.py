from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('administration/', include('applications.noyau.admin_urls')),
    path('', include('applications.noyau.urls')),
    path('comptes/', include('applications.comptes.urls')),
    path('portefeuille/', include('applications.portefeuille.urls')),
    
    path('paiements/', include('applications.paiements.urls')),
    path('produits/', include('applications.produits.urls')),
    path('parrainages/', include('applications.parrainages.urls')),
    path('shop/', include('applications.shop.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin

admin.site.site_header = "Administration de Genius Africa"      # Titre en haut
admin.site.site_title = "Console Genius Africa"                 # Titre de l'onglet navigateur
admin.site.index_title = "Bienvenue dans l’administration G.A"   # Texte d’accueil sur la page d’index
