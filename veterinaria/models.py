from django.db import models
from django.urls import reverse
from django.utils import timezone

class Veterinario(models.Model):
    """
    Modelo para los veterinarios de la clínica.
    Solo se gestiona desde Django Admin.
    """
    nombre = models.CharField(max_length=100, verbose_name="Nombre completo")
    especialidad = models.CharField(max_length=100, verbose_name="Especialidad", blank=True)
    telefono = models.CharField(max_length=20, verbose_name="Teléfono", blank=True)
    email = models.EmailField(verbose_name="Email", blank=True)
    numero_colegiado = models.CharField(max_length=50, verbose_name="Número de colegiado", blank=True)
    activo = models.BooleanField(default=True, verbose_name="Activo")
    fecha_ingreso = models.DateField(verbose_name="Fecha de ingreso", blank=True, null=True)
    
    class Meta:
        verbose_name = "Veterinario"
        verbose_name_plural = "Veterinarios"
        ordering = ['nombre']
    
    def __str__(self):
        especialidad_text = f" - {self.especialidad}" if self.especialidad else ""
        return f"Dr. {self.nombre}{especialidad_text}"

class Categoria(models.Model):
    """
    Modelo para las categorías de productos veterinarios.
    Solo se gestiona desde Django Admin.
    """
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la categoría")
    descripcion = models.TextField(verbose_name="Descripción")
    imagen = models.ImageField(upload_to='categorias/', verbose_name="Imagen representativa")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class TipoAnimal(models.Model):
    """
    Modelo para los tipos de animales (Perro, Gato, Ave, etc.).
    Solo se gestiona desde Django Admin.
    """
    nombre = models.CharField(max_length=50, verbose_name="Tipo de animal")
    descripcion = models.TextField(verbose_name="Descripción del tipo")
    imagen = models.ImageField(upload_to='tipos_animales/', verbose_name="Imagen del tipo", blank=True, null=True)
    activo = models.BooleanField(default=True, verbose_name="Activo")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    
    class Meta:
        verbose_name = "Tipo de Animal"
        verbose_name_plural = "Tipos de Animales"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class Mascota(models.Model):
    """
    Modelo para mascotas registradas en la veterinaria.
    Se gestiona a través de formularios CRUD en la aplicación web.
    """
    SEXO_CHOICES = [
        ('macho', 'Macho'),
        ('hembra', 'Hembra'),
    ]
    
    TAMAÑO_CHOICES = [
        ('pequeño', 'Pequeño'),
        ('mediano', 'Mediano'),
        ('grande', 'Grande'),
        ('gigante', 'Gigante'),
    ]
    
    tipo_animal = models.ForeignKey(TipoAnimal, on_delete=models.CASCADE, verbose_name="Tipo de animal")
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la mascota")
    raza = models.CharField(max_length=100, verbose_name="Raza", blank=True)
    edad = models.PositiveIntegerField(verbose_name="Edad (años)", blank=True, null=True)
    sexo = models.CharField(max_length=10, choices=SEXO_CHOICES, verbose_name="Sexo")
    tamaño = models.CharField(max_length=15, choices=TAMAÑO_CHOICES, verbose_name="Tamaño", blank=True)
    peso = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Peso (kg)", blank=True, null=True)
    color = models.CharField(max_length=100, verbose_name="Color/Coloración", blank=True)
    
    # Información del propietario
    propietario_nombre = models.CharField(max_length=200, verbose_name="Nombre del propietario")
    propietario_telefono = models.CharField(max_length=20, verbose_name="Teléfono del propietario", blank=True)
    propietario_email = models.EmailField(verbose_name="Email del propietario", blank=True)
    propietario_direccion = models.TextField(verbose_name="Dirección del propietario", blank=True)
    
    # Información médica
    veterinario_encargado = models.ForeignKey(Veterinario, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Veterinario encargado")
    numero_chip = models.CharField(max_length=50, unique=True, verbose_name="Número de microchip", blank=True, null=True)
    observaciones = models.TextField(verbose_name="Observaciones médicas", blank=True)
    imagen = models.ImageField(upload_to='mascotas/', verbose_name="Foto de la mascota", blank=True, null=True)
    
    # Campos de control
    activo = models.BooleanField(default=True, verbose_name="Activo")
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")
    fecha_modificacion = models.DateTimeField(auto_now=True, verbose_name="Última modificación")
    
    class Meta:
        verbose_name = "Mascota"
        verbose_name_plural = "Mascotas"
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} - {self.tipo_animal.nombre} ({self.propietario_nombre})"
    
    def get_absolute_url(self):
        return reverse('mascota_detalle', kwargs={'pk': self.pk})


class Producto(models.Model):
    """
    Modelo para productos veterinarios (medicamentos, alimentos, servicios).
    Se gestiona a través de formularios CRUD en la aplicación web.
    """
    TIPO_PRODUCTO_CHOICES = [
        ('medicamento', 'Medicamento'),
        ('alimento', 'Alimento para mascotas'),
        ('servicio', 'Servicio veterinario'),
        ('accesorio', 'Accesorio para mascotas'),
        ('equipo', 'Equipo médico veterinario'),
    ]
    
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, verbose_name="Categoría")
    nombre = models.CharField(max_length=200, verbose_name="Nombre del producto")
    descripcion = models.TextField(verbose_name="Descripción detallada", blank=True)
    tipo_producto = models.CharField(max_length=20, choices=TIPO_PRODUCTO_CHOICES, verbose_name="Tipo de producto")
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio (CLP $)", blank=True, null=True)
    codigo = models.CharField(max_length=50, unique=True, verbose_name="Código del producto", blank=True)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True, verbose_name="Imagen del producto")
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock disponible", blank=True)
    activo = models.BooleanField(default=True, verbose_name="Producto activo")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    fecha_modificacion = models.DateTimeField(auto_now=True, verbose_name="Última modificación")
    
    # Campos específicos para medicamentos
    principio_activo = models.CharField(max_length=200, blank=True, verbose_name="Principio activo")
    concentracion = models.CharField(max_length=100, blank=True, verbose_name="Concentración")
    laboratorio = models.CharField(max_length=100, blank=True, verbose_name="Laboratorio")
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['nombre']
    
    def __str__(self):
        return f"{self.nombre} - {self.categoria.nombre}"
    
    def get_absolute_url(self):
        return reverse('producto_detalle', kwargs={'pk': self.pk})


class Cita(models.Model):
    """
    Modelo para las citas de atención veterinaria.
    Se gestiona a través de formularios CRUD en la aplicación web.
    """
    ESTADO_CHOICES = [
        ('programada', 'Programada'),
        ('confirmada', 'Confirmada'),
        ('en_curso', 'En Curso'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
        ('no_asistio', 'No Asistió'),
    ]
    
    TIPO_CITA_CHOICES = [
        ('consulta_general', 'Consulta General'),
        ('vacunacion', 'Vacunación'),
        ('cirugia', 'Cirugía'),
        ('control', 'Control'),
        ('emergencia', 'Emergencia'),
        ('estetica', 'Estética'),
        ('otros', 'Otros'),
    ]
    
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE, verbose_name="Mascota")
    fecha_hora = models.DateTimeField(verbose_name="Fecha y hora de la cita")
    tipo_cita = models.CharField(max_length=20, choices=TIPO_CITA_CHOICES, verbose_name="Tipo de cita")
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='programada', verbose_name="Estado")
    motivo = models.TextField(verbose_name="Motivo de la consulta")
    observaciones = models.TextField(verbose_name="Observaciones", blank=True)
    veterinario = models.CharField(max_length=200, verbose_name="Veterinario asignado", blank=True)
    precio_estimado = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio estimado (CLP $)", blank=True, null=True)
    
    # Campos de control
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    fecha_modificacion = models.DateTimeField(auto_now=True, verbose_name="Última modificación")
    
    class Meta:
        verbose_name = "Cita"
        verbose_name_plural = "Citas"
        ordering = ['fecha_hora']
        
    def __str__(self):
        return f"Cita {self.mascota.nombre} - {self.fecha_hora.strftime('%d/%m/%Y %H:%M')} ({self.get_estado_display()})"
    
    def get_absolute_url(self):
        return reverse('cita_detail', kwargs={'pk': self.pk})
    
    @property
    def es_pasada(self):
        """Verifica si la cita ya pasó"""
        return self.fecha_hora < timezone.now()
    
    @property
    def puede_modificarse(self):
        """Verifica si la cita puede modificarse (no está completada, cancelada o ya pasó)"""
        return self.estado not in ['completada', 'cancelada'] and not self.es_pasada
