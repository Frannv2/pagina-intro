from django.contrib import admin
from .models import Perfil, Donacion

# Registra los modelos en el panel de administración
admin.site.register(Perfil)
admin.site.register(Donacion)
