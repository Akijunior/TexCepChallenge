"""TexCepChallenge URL Configuration."""

# Importações externas
from django.contrib import admin
from django.urls import path
from django.conf.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/pessoas/', include('pessoa.urls')),
    path('api/enderecos/', include('cep.urls')),
]
