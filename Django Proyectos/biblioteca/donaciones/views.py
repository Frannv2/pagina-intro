from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Donacion, Perfil
from .forms import DonacionForm, RegistroDonanteForm, RegistroAprobadorForm, CodigoAccesoForm
from django.contrib.auth import login

def login_view(request):
    if request.user.is_authenticated:
        perfil = request.user.perfil
        if (perfil.rol == 'aprobador'):
            return redirect('panel_aprobador')
        return redirect('inicio')

def registro_donante(request):
    if request.method == 'POST':
        form = RegistroDonanteForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('panel_donante')
    else:
        form = RegistroDonanteForm()
    return render(request, 'donaciones/registro_donante.html', {'form': form})

# Define el código de acceso correcto
CODIGO_APROBADOR = "1234"

def registro_aprobador(request):
    # Si el código ya se verificó, mostrar el formulario de registro
    if request.session.get("codigo_verificado", False):
        if request.method == 'POST':
            form = RegistroAprobadorForm(request.POST)
            if form.is_valid():
                usuario = form.save(commit=False)
                usuario.save()
                Perfil.objects.create(usuario=usuario, rol='aprobador')
                # Limpiar la sesión tras el registro
                del request.session["codigo_verificado"]
                return redirect('login')
        else:
            form = RegistroAprobadorForm()
        return render(request, 'donaciones/registro_aprobador.html', {'form': form})

    # Si el código no se ha verificado, mostrar el formulario de código
    if request.method == "POST":
        form = CodigoAccesoForm(request.POST)
        if form.is_valid():
            codigo = form.cleaned_data['codigo']
            if codigo == CODIGO_APROBADOR:
                request.session["codigo_verificado"] = True
                return redirect('registro_aprobador')
    else:
        form = CodigoAccesoForm()
    return render(request, 'donaciones/codigo_acceso.html', {'form': form})

def inicio(request):
    return render(request, 'donaciones/inicio.html')

# Vista para crear una nueva donación (Donante)
@login_required
def crear_donacion(request):
    if request.method == 'POST':
        form = DonacionForm(request.POST, request.FILES)
        if form.is_valid():
            # Establecer el estado como 'pendiente' y la fecha automáticamente
            donacion = form.save(commit=False)
            donacion.estado = 'pendiente'  # Estado por defecto
            donacion.fecha = timezone.now()  # Fecha por defecto
            donacion.usuario = request.user  # Asignar el usuario autenticado
            donacion.save()  # Guardar la donación
            return redirect('panel_donante')  # Redirigir al panel del donante después de crear la donación
    else:
        form = DonacionForm()

    return render(request, 'donaciones/crear_donacion.html', {'form': form})

# Vista para listar donaciones (Aprobador)
@login_required
def listar_donaciones(request):
    if not Perfil.objects.filter(usuario=request.user, rol='aprobador').exists():
        return redirect('inicio')  # Redirige si el usuario no es aprobador
    donaciones = Donacion.objects.all()
    return render(request, 'donaciones/listar_donaciones.html', {'donaciones': donaciones})

# Panel del donante para ver el estado de sus donaciones
@login_required
def panel_donante(request):
    donaciones = Donacion.objects.filter(usuario=request.user)  # Obtienen las donaciones del usuario
    return render(request, 'donaciones/panel_donante.html', {'donaciones': donaciones})

@login_required
def panel_aprobador(request):
    perfil = request.user.perfil
    if perfil.rol != 'aprobador':
        return redirect('inicio')

    estado = request.GET.get('estado', 'todas')
    if estado == 'todas':
        donaciones = Donacion.objects.all()
    else:
        donaciones = Donacion.objects.filter(estado=estado)
    
    return render(request, 'donaciones/panel_aprobador.html', {'donaciones': donaciones})

@login_required
def cambiar_estado_donacion(request, donacion_id, nuevo_estado):
    perfil = request.user.perfil
    if perfil.rol != 'aprobador':
        return redirect('inicio')
    
    donacion = Donacion.objects.get(id=donacion_id)
    donacion.estado = nuevo_estado
    donacion.save()
    
    return redirect('panel_aprobador')