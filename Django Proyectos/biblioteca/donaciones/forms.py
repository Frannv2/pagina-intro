from django import forms
from .models import Donacion
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Perfil

class DonacionForm(forms.ModelForm):
    class Meta:
        model = Donacion
        fields = ['tipo_donacion', 'descripcion', 'archivo']

class CodigoAccesoForm(forms.Form):
    codigo = forms.CharField(label="Código de acceso", max_length=50)

class RegistroDonanteForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    # Modificando el campo de la contraseña para usar un widget adecuado
    password = forms.CharField(widget=forms.PasswordInput)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Usar el set_password para asegurar que la contraseña sea cifrada
        if commit:
            user.save()
            # Crear el perfil de donante
            Perfil.objects.create(usuario=user, rol='donante')
        return user

class RegistroAprobadorForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    # Modificando el campo de la contraseña para usar un widget adecuado
    password = forms.CharField(widget=forms.PasswordInput)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            Perfil.objects.create(usuario=user, rol='aprobador')
        return user