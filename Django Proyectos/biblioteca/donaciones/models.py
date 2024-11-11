from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

# Definimos los roles de usuario
class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.usuario.username} - {self.rol}"

# Modelo de Donación
class Donacion(models.Model):
    TIPO_CHOICES = [
        ('imagen', 'Imagen'),
        ('video', 'Video'),
        ('documento', 'Documento'),
        ('audio', 'Audio'),
    ]
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, default=1)  # Asignamos un valor por defecto
    tipo_donacion = models.CharField(max_length=20, choices=TIPO_CHOICES)
    descripcion = models.TextField()
    archivo = models.FileField(upload_to='donaciones/', null=True, blank=True)
    estado = models.CharField(max_length=10, default='pendiente')
    fecha = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.tipo_donacion} - {self.descripcion[:20]}'
