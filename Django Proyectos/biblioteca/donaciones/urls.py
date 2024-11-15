from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView 

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('registro_donante/', views.registro_donante, name='registro_donante'),
    path('registro_aprobador/', views.registro_aprobador, name='registro_aprobador'),
    path('crear_donacion/', views.crear_donacion, name='crear_donacion'),
    path('listar_donaciones/', views.listar_donaciones, name='listar_donaciones'),
    path('panel_donante/', views.panel_donante, name='panel_donante'),
    path('panel_aprobador/', views.panel_aprobador, name='panel_aprobador'),
    path('cambiar_estado_donacion/<int:donacion_id>/<str:nuevo_estado>/', views.cambiar_estado_donacion, name='cambiar_estado_donacion'),
]
