from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # Página principal
    path('', views.home, name='home'),
    
    # Productos por categoría
    path('categoria/<int:categoria_id>/', views.productos_por_categoria, name='productos_categoria'),
    
    # Mantenedor de productos
    path('mantenedor/<int:categoria_id>/', views.mantenedor_productos, name='mantenedor_productos'),
    
    # CRUD de productos
    path('productos/', views.ProductoListView.as_view(), name='producto_list'),
    path('producto/<int:pk>/', views.ProductoDetailView.as_view(), name='producto_detail'),
    path('producto/nuevo/', views.ProductoCreateView.as_view(), name='producto_create'),
    path('producto/<int:pk>/editar/', views.ProductoUpdateView.as_view(), name='producto_update'),
    path('producto/<int:pk>/eliminar/', views.ProductoDeleteView.as_view(), name='producto_delete'),
    
    # CRUD de mascotas
    path('mascotas/', views.MascotaListView.as_view(), name='mascota_list'),
    path('mascota/<int:pk>/', views.MascotaDetailView.as_view(), name='mascota_detail'),
    path('mascota/nueva/', views.MascotaCreateView.as_view(), name='mascota_create'),
    path('mascota/<int:pk>/editar/', views.MascotaUpdateView.as_view(), name='mascota_update'),
    path('mascota/<int:pk>/eliminar/', views.MascotaDeleteView.as_view(), name='mascota_delete'),
    
    # CRUD de citas
    path('citas/', views.CitaListView.as_view(), name='cita_list'),
    path('cita/<int:pk>/', views.CitaDetailView.as_view(), name='cita_detail'),
    path('cita/nueva/', views.CitaCreateView.as_view(), name='cita_create'),
    path('cita/<int:pk>/editar/', views.CitaUpdateView.as_view(), name='cita_update'),
    path('cita/<int:pk>/cancelar/', views.CitaDeleteView.as_view(), name='cita_delete'),
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
