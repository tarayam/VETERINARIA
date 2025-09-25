from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _
from django import forms
from .models import Categoria

from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _
from django import forms
from .models import Categoria, TipoAnimal, Cita, Mascota

# Parchear el validador de username en el modelo User
def validador_flexible(self):
    """Validador flexible que permite espacios y cualquier carácter"""
    pass  # No hacer ninguna validación

# Sobrescribir la validación del modelo User
User.username.field.validators = []

# Formulario completamente personalizado sin validadores de Django
class UsuarioCreacionForm(forms.ModelForm):
    username = forms.CharField(
        label="Nombre de usuario",
        max_length=150,
        help_text="Puede contener letras, números, espacios y los caracteres @/./+/-/_",
        widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'})
    )
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}),
        help_text="Mínimo 4 caracteres. Puede contener letras y números."
    )
    password2 = forms.CharField(
        label="Confirmación de contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'new-password'}),
        help_text="Ingrese la misma contraseña para verificación."
    )
    
    class Meta:
        model = User
        fields = ('username',)
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise forms.ValidationError("Este campo es obligatorio.")
        if len(username) > 150:
            raise forms.ValidationError("El nombre de usuario no puede tener más de 150 caracteres.")
        # Verificar que no exista otro usuario con el mismo nombre
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Ya existe un usuario con este nombre.")
        return username
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        if password1 and len(password1) < 4:
            raise forms.ValidationError("La contraseña debe tener al menos 4 caracteres.")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

# Personalizar el admin de usuarios
class UsuarioAdmin(UserAdmin):
    add_form = UsuarioCreacionForm
    
    # Personalizar los fieldsets para el formulario de creación
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    
    # Fieldsets para la edición de usuarios existentes
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información personal', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permisos', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Campos mostrados en la lista
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)
    
    # Permitir edición y eliminación
    list_editable = ('is_active', 'is_staff')
    actions = ['make_active', 'make_inactive', 'delete_selected']
    
    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            # Para nuevos usuarios, usar nuestro formulario personalizado
            kwargs['form'] = self.add_form
        return super().get_form(request, obj, **kwargs)
    
    def make_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f"Se activaron {queryset.count()} usuarios.")
    make_active.short_description = "Activar usuarios seleccionados"
    
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f"Se desactivaron {queryset.count()} usuarios.")
    make_inactive.short_description = "Desactivar usuarios seleccionados"

# Desregistrar el admin por defecto y registrar el personalizado
admin.site.unregister(User)
admin.site.register(User, UsuarioAdmin)

# Personalización del sitio admin
admin.site.site_header = "Administración Veterinaria"
admin.site.site_title = "Admin Veterinaria"
admin.site.index_title = "Panel de Administración Veterinaria"

# Personalizar más textos del admin
admin.site.empty_value_display = '(Vacío)'

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    """
    Configuración del admin para Categorías.
    Solo las categorías se gestionan desde el Django Admin.
    """
    list_display = ['nombre', 'activo', 'fecha_creacion']
    list_filter = ['activo', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion']
    list_editable = ['activo']
    readonly_fields = ['fecha_creacion']
    
    # Textos personalizados
    verbose_name = "Categoría"
    verbose_name_plural = "Categorías"
    
    fieldsets = (
        ('Información básica', {
            'fields': ('nombre', 'descripcion', 'imagen')
        }),
        ('Estado', {
            'fields': ('activo', 'fecha_creacion')
        })
    )

# Nota: El modelo Producto NO se registra aquí

@admin.register(TipoAnimal)
class TipoAnimalAdmin(admin.ModelAdmin):
    """
    Configuración del admin para Tipos de Animales.
    Solo los tipos de animales se gestionan desde el Django Admin.
    """
    list_display = ['nombre', 'activo', 'fecha_creacion']
    list_filter = ['activo', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion']
    list_editable = ['activo']
    readonly_fields = ['fecha_creacion']
    
    fieldsets = (
        ('Información básica', {
            'fields': ('nombre', 'descripcion', 'imagen')
        }),
        ('Estado', {
            'fields': ('activo', 'fecha_creacion')
        })
    )

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    """
    Administración de citas desde Django Admin.
    Permite gestionar citas con filtros y búsqueda avanzada.
    """
    list_display = ('mascota', 'fecha_hora', 'tipo_cita', 'estado', 'veterinario', 'propietario_mascota')
    list_filter = ('estado', 'tipo_cita', 'fecha_hora', 'mascota__tipo_animal')
    search_fields = ('mascota__nombre', 'mascota__propietario_nombre', 'motivo', 'veterinario')
    date_hierarchy = 'fecha_hora'
    ordering = ('-fecha_hora',)
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('mascota', 'fecha_hora', 'tipo_cita', 'estado')
        }),
        ('Detalles de la Cita', {
            'fields': ('motivo', 'observaciones', 'veterinario', 'precio_estimado')
        }),
        ('Información de Control', {
            'fields': ('fecha_creacion', 'fecha_modificacion'),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ('fecha_creacion', 'fecha_modificacion')
    
    def propietario_mascota(self, obj):
        """Mostrar el nombre del propietario de la mascota"""
        return obj.mascota.propietario_nombre
    propietario_mascota.short_description = 'Propietario'

# Nota: El modelo Mascota NO se registra aquí - se gestiona por formularios web

# Personalizar el admin para mostrar texto en español
class VeterinariaAdminSite(AdminSite):
    site_header = "Sistema de Gestión Veterinaria"
    site_title = "Veterinaria Admin"
    index_title = "Bienvenido al Panel de Administración Veterinaria"

# Crear una instancia personalizada del admin
veterinaria_admin_site = VeterinariaAdminSite(name='veterinaria_admin')
# Las mascotas se gestionan únicamente a través de formularios CRUD en la web
