from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.db.models import Q
from .models import Categoria, Producto, TipoAnimal, Mascota, Cita
from .forms import ProductoForm, MascotaForm, CitaForm
from django.db.models import Sum, Count, Q

# Vista principal - Home con categorías
def home(request):
    """
    Vista principal que muestra todas las categorías activas.
    Cada categoría se muestra en un card de Bootstrap.
    """
    categorias = Categoria.objects.filter(activo=True).order_by('nombre')
    context = {
        'categorias': categorias,
        'titulo': 'Sistema de Gestión Veterinaria',
    }
    return render(request, 'veterinaria/home.html', context)

# Vista de productos por categoría
def productos_por_categoria(request, categoria_id):
    """
    Vista que muestra todos los productos de una categoría específica.
    Incluye funcionalidad de búsqueda por nombre de producto.
    """
    categoria = get_object_or_404(Categoria, id=categoria_id, activo=True)
    productos = Producto.objects.filter(categoria=categoria, activo=True)
    
    # Funcionalidad de búsqueda
    query = request.GET.get('buscar')
    if query:
        productos = productos.filter(
            Q(nombre__icontains=query) | 
            Q(descripcion__icontains=query) |
            Q(codigo__icontains=query)
        )
    
    context = {
        'categoria': categoria,
        'productos': productos,
        'query': query,
        'titulo': f'Productos - {categoria.nombre}',
    }
    return render(request, 'veterinaria/productos_categoria.html', context)

# Vistas CRUD para Productos
class ProductoListView(ListView):
    """Lista todos los productos"""
    model = Producto
    template_name = 'veterinaria/producto_list.html'
    context_object_name = 'productos'
    paginate_by = 10
    
    def get_queryset(self):
        return Producto.objects.filter(activo=True).order_by('-fecha_creacion')

class ProductoDetailView(DetailView):
    """Detalle de un producto específico"""
    model = Producto
    template_name = 'veterinaria/producto_detail.html'
    context_object_name = 'producto'

class ProductoCreateView(CreateView):
    """Crear nuevo producto"""
    model = Producto
    form_class = ProductoForm
    template_name = 'veterinaria/producto_form.html'
    
    def get_success_url(self):
        next_url = self.request.POST.get('next') or self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('producto_list')

    def form_valid(self, form):
        messages.success(self.request, 'Producto creado exitosamente.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Agregar Producto'
        context['accion'] = 'Crear'
        context['next'] = self.request.GET.get('next', self.request.META.get('HTTP_REFERER', ''))
        return context

class ProductoUpdateView(UpdateView):
    """Actualizar producto existente"""
    model = Producto
    form_class = ProductoForm
    template_name = 'veterinaria/producto_form.html'
    
    def get_success_url(self):
        next_url = self.request.POST.get('next') or self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('producto_list')

    def form_valid(self, form):
        messages.success(self.request, 'Producto actualizado exitosamente.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Producto'
        context['accion'] = 'Actualizar'
        context['next'] = self.request.GET.get('next', self.request.META.get('HTTP_REFERER', ''))
        return context
class ProductoDeleteView(DeleteView):
    """Eliminar producto (soft delete - marcarlo como inactivo)"""
    model = Producto
    template_name = 'veterinaria/producto_confirm_delete.html'
    success_url = reverse_lazy('producto_list')
    
    def delete(self, request, *args, **kwargs):
        # Soft delete - marcar como inactivo en lugar de eliminar
        self.object = self.get_object()
        self.object.activo = False
        self.object.save()
        messages.success(request, 'Producto eliminado exitosamente.')
        return redirect(self.success_url)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Producto'
        return context

# Vista de mantenedor de productos
def mantenedor_productos(request, categoria_id):
    """
    Vista del mantenedor de productos para una categoría específica.
    Desde aquí se pueden agregar, modificar y eliminar productos.
    """
    categoria = get_object_or_404(Categoria, id=categoria_id, activo=True)
    productos = Producto.objects.filter(categoria=categoria, activo=True).order_by('nombre')
    
    total_valor = productos.aggregate(Sum('precio'))['precio__sum'] or 0
    stock_bajo = productos.filter(stock__lte=5, stock__gt=0).count()
    activos_con_stock = productos.filter(stock__gt=0).count()  #  solo los que tienen stock > 0

    context = {
        'categoria': categoria,
        'productos': productos,
        'total_valor': total_valor,
        'stock_bajo': stock_bajo,
        'activos_con_stock': activos_con_stock, 
        'titulo': f'Mantenedor - {categoria.nombre}',
    }
    return render(request, 'veterinaria/mantenedor_productos.html', context)


# Vistas CRUD para Mascotas
class MascotaListView(ListView):
    """Lista todas las mascotas"""
    model = Mascota
    template_name = 'veterinaria/mascota_list.html'
    context_object_name = 'mascotas'
    paginate_by = 10
    
    def get_queryset(self):
        return Mascota.objects.filter(activo=True).order_by('-fecha_registro')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Mascotas'
        return context

class MascotaDetailView(DetailView):
    """Detalle de una mascota específica"""
    model = Mascota
    template_name = 'veterinaria/mascota_detail.html'
    context_object_name = 'mascota'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Detalle - {self.object.nombre}'
        return context

class MascotaCreateView(CreateView):
    """Crear nueva mascota"""
    model = Mascota
    form_class = MascotaForm
    template_name = 'veterinaria/mascota_form.html'
    success_url = reverse_lazy('mascota_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Mascota registrada exitosamente.')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Registrar Mascota'
        context['accion'] = 'Crear'
        return context

class MascotaUpdateView(UpdateView):
    """Actualizar mascota existente"""
    model = Mascota
    form_class = MascotaForm
    template_name = 'veterinaria/mascota_form.html'
    success_url = reverse_lazy('mascota_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Información de mascota actualizada exitosamente.')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar - {self.object.nombre}'
        context['accion'] = 'Actualizar'
        return context

class MascotaDeleteView(DeleteView):
    """Eliminar mascota (soft delete - marcarla como inactiva)"""
    model = Mascota
    template_name = 'veterinaria/mascota_confirm_delete.html'
    success_url = reverse_lazy('mascota_list')
    
    def delete(self, request, *args, **kwargs):
        # Soft delete - marcar como inactivo en lugar de eliminar
        self.object = self.get_object()
        self.object.activo = False
        self.object.save()
        messages.success(request, 'Mascota eliminada del sistema exitosamente.')
        return redirect(self.success_url)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Eliminar - {self.object.nombre}'
        return context


# ============================================================================
# VISTAS CRUD PARA CITAS
# ============================================================================

class CitaListView(ListView):
    """Listar todas las citas con funcionalidad de búsqueda y filtrado"""
    model = Cita
    template_name = 'veterinaria/cita_list.html'
    context_object_name = 'citas'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Cita.objects.select_related('mascota', 'mascota__tipo_animal').order_by('-fecha_hora')
        
        # Filtrar por búsqueda
        query = self.request.GET.get('buscar')
        if query:
            queryset = queryset.filter(
                Q(mascota__nombre__icontains=query) |
                Q(mascota__propietario_nombre__icontains=query) |
                Q(motivo__icontains=query) |
                Q(veterinario__icontains=query)
            )
        
        # Filtrar por estado
        estado = self.request.GET.get('estado')
        if estado:
            queryset = queryset.filter(estado=estado)
        
        # Filtrar por fecha
        fecha = self.request.GET.get('fecha')
        if fecha:
            queryset = queryset.filter(fecha_hora__date=fecha)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Gestión de Citas'
        context['query'] = self.request.GET.get('buscar', '')
        context['estado_seleccionado'] = self.request.GET.get('estado', '')
        context['fecha_seleccionada'] = self.request.GET.get('fecha', '')
        context['estados'] = Cita.ESTADO_CHOICES
        return context

class CitaDetailView(DetailView):
    """Vista detallada de una cita específica"""
    model = Cita
    template_name = 'veterinaria/cita_detail.html'
    context_object_name = 'cita'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Cita - {self.object.mascota.nombre}'
        return context

class CitaCreateView(CreateView):
    """Crear nueva cita"""
    model = Cita
    form_class = CitaForm
    template_name = 'veterinaria/cita_form.html'
    success_url = reverse_lazy('cita_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Cita agendada exitosamente.')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Nueva Cita'
        context['accion'] = 'Agendar'
        return context

class CitaUpdateView(UpdateView):
    """Editar cita existente"""
    model = Cita
    form_class = CitaForm
    template_name = 'veterinaria/cita_form.html'
    success_url = reverse_lazy('cita_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Cita actualizada exitosamente.')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar Cita - {self.object.mascota.nombre}'
        context['accion'] = 'Actualizar'
        return context
    
    def dispatch(self, request, *args, **kwargs):
        """Verificar si la cita puede modificarse"""
        cita = self.get_object()
        if not cita.puede_modificarse:
            messages.error(request, 'Esta cita no puede modificarse (ya está completada, cancelada o la fecha ya pasó).')
            return redirect('cita_detail', pk=cita.pk)
        return super().dispatch(request, *args, **kwargs)

class CitaDeleteView(DeleteView):
    """Cancelar cita (cambiar estado a cancelada)"""
    model = Cita
    template_name = 'veterinaria/cita_confirm_delete.html'
    success_url = reverse_lazy('cita_list')
    
    def delete(self, request, *args, **kwargs):
        # En lugar de eliminar, cambiar estado a cancelada
        self.object = self.get_object()
        self.object.estado = 'cancelada'
        self.object.save()
        messages.success(request, 'Cita cancelada exitosamente.')
        return redirect(self.success_url)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Cancelar Cita - {self.object.mascota.nombre}'
        return context

