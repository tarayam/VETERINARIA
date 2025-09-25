from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
import re
from decimal import Decimal
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, HTML
from crispy_forms.bootstrap import Field
from .models import Producto, Categoria, Mascota, TipoAnimal, Cita, Veterinario

class ProductoForm(forms.ModelForm):
    """
    Formulario para crear y editar productos veterinarios.
    Utiliza crispy forms para un mejor diseño con Bootstrap.
    """
    
    class Meta:
        model = Producto
        fields = [
            'categoria', 'nombre', 'descripcion', 'tipo_producto', 
            'precio', 'codigo', 'imagen', 'stock', 
            'principio_activo', 'concentracion', 'laboratorio'
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
            'precio': forms.NumberInput(attrs={'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'min': '0'}),
        }
        labels = {
            'categoria': 'Categoría *',
            'nombre': 'Nombre del Producto *',
            'descripcion': 'Descripción (opcional)',
            'tipo_producto': 'Tipo de Producto *',
            'precio': 'Precio CLP $ (opcional)',
            'codigo': 'Código del Producto (opcional)',
            'imagen': 'Imagen (opcional)',
            'stock': 'Stock Disponible (opcional)',
            'principio_activo': 'Principio Activo (solo medicamentos)',
            'concentracion': 'Concentración (solo medicamentos)',
            'laboratorio': 'Laboratorio (solo medicamentos)',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        
        # Solo mostrar categorías activas
        self.fields['categoria'].queryset = Categoria.objects.filter(activo=True)
        
        # Configurar el layout del formulario
        self.helper.layout = Layout(
            HTML('<div class="card">'),
            HTML('<div class="card-header"><h5>Información Básica</h5></div>'),
            HTML('<div class="card-body">'),
            Row(
                Column('categoria', css_class='form-group col-md-6 mb-3'),
                Column('tipo_producto', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('nombre', css_class='form-group col-md-8 mb-3'),
                Column('codigo', css_class='form-group col-md-4 mb-3'),
            ),
            'descripcion',
            Row(
                Column('precio', css_class='form-group col-md-6 mb-3'),
                Column('stock', css_class='form-group col-md-6 mb-3'),
            ),
            'imagen',
            HTML('</div></div>'),
            
            HTML('<div class="card mt-3">'),
            HTML('<div class="card-header"><h5>Información Médica (Opcional)</h5></div>'),
            HTML('<div class="card-body">'),
            HTML('<p class="text-muted">Complete solo si es un medicamento</p>'),
            'principio_activo',
            Row(
                Column('concentracion', css_class='form-group col-md-6 mb-3'),
                Column('laboratorio', css_class='form-group col-md-6 mb-3'),
            ),
            HTML('</div></div>'),
            
            Div(
                Submit('submit', 'Guardar Producto', css_class='btn btn-primary me-2'),
                HTML('<a href="{% url "producto_list" %}" class="btn btn-secondary">Cancelar</a>'),
                css_class='mt-3 text-center'
            )
        )
    
    def clean_nombre(self):
        """Validar nombre del producto"""
        nombre = self.cleaned_data.get('nombre')
        if nombre:
            # Verificar longitud mínima
            if len(nombre.strip()) < 3:
                raise ValidationError('El nombre debe tener al menos 3 caracteres.')
            
            # Verificar que no sea solo números
            if nombre.strip().isdigit():
                raise ValidationError('El nombre no puede ser solo números.')
            
            # Verificar caracteres especiales excesivos
            if len(re.sub(r'[a-zA-Z0-9\s\-_áéíóúñüÁÉÍÓÚÑÜ]', '', nombre)) > 3:
                raise ValidationError('El nombre contiene demasiados caracteres especiales.')
        
        return nombre.strip() if nombre else nombre
    
    def clean_codigo(self):
        """Validar que el código sea único y tenga formato válido"""
        codigo = self.cleaned_data.get('codigo')
        if codigo:
            codigo = codigo.strip().upper()
            
            # Validar formato del código (letras, números, guiones)
            if not re.match(r'^[A-Z0-9\-_]{3,20}$', codigo):
                raise ValidationError('El código debe tener entre 3-20 caracteres y solo puede contener letras, números, guiones y guiones bajos.')
            
            # Verificar unicidad
            productos = Producto.objects.filter(codigo=codigo)
            if self.instance and self.instance.pk:
                productos = productos.exclude(pk=self.instance.pk)
            
            if productos.exists():
                raise ValidationError('Ya existe un producto con este código.')
        
        return codigo
    
    def clean_precio(self):
        """Validar que el precio sea positivo y razonable"""
        precio = self.cleaned_data.get('precio')
        if precio is not None:
            if precio < 0:
                raise ValidationError('El precio no puede ser negativo.')
            if precio == 0:
                raise ValidationError('El precio debe ser mayor a 0.')
            if precio > Decimal('10000000'):
                raise ValidationError('El precio es demasiado alto. Máximo: $10,000,000.')
        return precio
    
    def clean_stock(self):
        """Validar stock"""
        stock = self.cleaned_data.get('stock')
        if stock is not None:
            if stock < 0:
                raise ValidationError('El stock no puede ser negativo.')
            if stock > 100000:
                raise ValidationError('El stock es demasiado alto. Máximo: 100,000 unidades.')
        return stock
    
    def clean_descripcion(self):
        """Validar descripción"""
        descripcion = self.cleaned_data.get('descripcion')
        if descripcion:
            if len(descripcion.strip()) < 10:
                raise ValidationError('La descripción debe tener al menos 10 caracteres.')
            if len(descripcion) > 1000:
                raise ValidationError('La descripción es demasiado larga. Máximo 1000 caracteres.')
        return descripcion.strip() if descripcion else descripcion
    
    def clean_principio_activo(self):
        """Validar principio activo para medicamentos"""
        principio_activo = self.cleaned_data.get('principio_activo')
        tipo_producto = self.cleaned_data.get('tipo_producto')
        
        if tipo_producto == 'medicamento' and not principio_activo:
            raise ValidationError('El principio activo es obligatorio para medicamentos.')
        
        if principio_activo and len(principio_activo.strip()) < 3:
            raise ValidationError('El principio activo debe tener al menos 3 caracteres.')
            
        return principio_activo.strip() if principio_activo else principio_activo
    
    def clean_concentracion(self):
        """Validar concentración para medicamentos"""
        concentracion = self.cleaned_data.get('concentracion')
        tipo_producto = self.cleaned_data.get('tipo_producto')
        
        if tipo_producto == 'medicamento' and not concentracion:
            raise ValidationError('La concentración es obligatoria para medicamentos.')
            
        return concentracion.strip() if concentracion else concentracion
    
    def clean_laboratorio(self):
        """Validar laboratorio para medicamentos"""
        laboratorio = self.cleaned_data.get('laboratorio')
        tipo_producto = self.cleaned_data.get('tipo_producto')
        
        if tipo_producto == 'medicamento' and not laboratorio:
            raise ValidationError('El laboratorio es obligatorio para medicamentos.')
            
        return laboratorio.strip() if laboratorio else laboratorio


class BuscarProductoForm(forms.Form):
    """
    Formulario de búsqueda para filtrar productos.
    """
    buscar = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por nombre, descripción o código...',
        }),
        label='Buscar producto'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.form_class = 'form-inline mb-3'
        self.helper.layout = Layout(
            Row(
                Column('buscar', css_class='form-group col-md-8'),
                Column(
                    Submit('submit', 'Buscar', css_class='btn btn-primary'),
                    css_class='form-group col-md-4 d-flex align-items-end'
                ),
            )
        )


class MascotaForm(forms.ModelForm):
    """
    Formulario para crear y editar mascotas.
    Utiliza crispy forms para un mejor diseño con Bootstrap.
    """
    
    class Meta:
        model = Mascota
        fields = [
            'tipo_animal', 'nombre', 'raza', 'edad', 'sexo', 'tamaño', 
            'peso', 'color', 'propietario_nombre', 'propietario_telefono', 
            'propietario_email', 'propietario_direccion', 'veterinario_encargado',
            'numero_chip', 'observaciones', 'imagen'
        ]
        widgets = {
            'observaciones': forms.Textarea(attrs={'rows': 3}),
            'propietario_direccion': forms.Textarea(attrs={'rows': 2}),
            'peso': forms.NumberInput(attrs={'step': '0.1', 'min': '0'}),
            'edad': forms.NumberInput(attrs={'min': '0'}),
            'propietario_email': forms.EmailInput(),
        }
        labels = {
            'tipo_animal': 'Tipo de Animal *',
            'nombre': 'Nombre de la Mascota *',
            'raza': 'Raza (opcional)',
            'edad': 'Edad en años (opcional)',
            'sexo': 'Sexo *',
            'tamaño': 'Tamaño (opcional)',
            'peso': 'Peso en kg (opcional)',
            'color': 'Color (opcional)',
            'propietario_nombre': 'Nombre del Propietario *',
            'propietario_telefono': 'Teléfono del Propietario (opcional)',
            'propietario_email': 'Email del Propietario (opcional)',
            'propietario_direccion': 'Dirección del Propietario (opcional)',
            'veterinario_encargado': 'Veterinario Encargado (opcional)',
            'numero_chip': 'Microchip de Identificación (opcional)',
            'observaciones': 'Observaciones Médicas (opcional)',
            'imagen': 'Foto de la Mascota (opcional)',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        
        # Solo mostrar tipos de animal activos
        self.fields['tipo_animal'].queryset = TipoAnimal.objects.filter(activo=True)
        
        # Solo mostrar veterinarios activos
        self.fields['veterinario_encargado'].queryset = Veterinario.objects.filter(activo=True)
        
        # Configurar el layout del formulario
        self.helper.layout = Layout(
            HTML('<div class="card">'),
            HTML('<div class="card-header"><h5>Información de la Mascota</h5></div>'),
            HTML('<div class="card-body">'),
            Row(
                Column('tipo_animal', css_class='form-group col-md-6 mb-3'),
                Column('nombre', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('raza', css_class='form-group col-md-6 mb-3'),
                Column('color', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('edad', css_class='form-group col-md-4 mb-3'),
                Column('sexo', css_class='form-group col-md-4 mb-3'),
                Column('tamaño', css_class='form-group col-md-4 mb-3'),
            ),
            Row(
                Column('peso', css_class='form-group col-md-6 mb-3'),
                Column('numero_chip', css_class='form-group col-md-6 mb-3'),
            ),
            'imagen',
            HTML('</div></div>'),
            
            HTML('<div class="card mt-3">'),
            HTML('<div class="card-header"><h5>Información del Propietario</h5></div>'),
            HTML('<div class="card-body">'),
            Row(
                Column('propietario_nombre', css_class='form-group col-md-6 mb-3'),
                Column('propietario_telefono', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('propietario_email', css_class='form-group col-md-6 mb-3'),
                Column('propietario_direccion', css_class='form-group col-md-6 mb-3'),
            ),
            HTML('</div></div>'),
            
            HTML('<div class="card mt-3">'),
            HTML('<div class="card-header"><h5>Información Médica</h5></div>'),
            HTML('<div class="card-body">'),
            'veterinario_encargado',
            'observaciones',
            HTML('</div></div>'),
            
            Div(
                Submit('submit', 'Guardar Mascota', css_class='btn btn-primary me-2'),
                HTML('<a href="{% url "mascota_list" %}" class="btn btn-secondary">Cancelar</a>'),
                css_class='mt-3 text-center'
            )
        )
    
    def clean_nombre(self):
        """Validar nombre de la mascota"""
        nombre = self.cleaned_data.get('nombre')
        if nombre:
            if len(nombre.strip()) < 2:
                raise ValidationError('El nombre debe tener al menos 2 caracteres.')
            if len(nombre) > 50:
                raise ValidationError('El nombre es demasiado largo. Máximo 50 caracteres.')
            # Solo letras, espacios y algunos caracteres especiales
            if not re.match(r'^[a-zA-ZáéíóúñüÁÉÍÓÚÑÜ\s\-\'\.]+$', nombre):
                raise ValidationError('El nombre solo puede contener letras, espacios, guiones y apostrofes.')
        return nombre.strip() if nombre else nombre
    
    def clean_peso(self):
        """Validar peso de la mascota"""
        peso = self.cleaned_data.get('peso')
        tipo_animal = self.cleaned_data.get('tipo_animal')
        
        if peso is not None:
            if peso <= 0:
                raise ValidationError('El peso debe ser mayor a 0.')
            if peso > 200:
                raise ValidationError('El peso parece demasiado alto. Máximo 200 kg.')
            
            # Validaciones específicas por tipo de animal
            if tipo_animal:
                if tipo_animal.nombre.lower() == 'gato' and peso > 15:
                    raise ValidationError('El peso para un gato parece muy alto (máximo recomendado: 15 kg).')
                elif tipo_animal.nombre.lower() == 'perro' and peso > 100:
                    raise ValidationError('El peso para un perro parece muy alto (máximo recomendado: 100 kg).')
                elif tipo_animal.nombre.lower() in ['ave', 'pájaro'] and peso > 5:
                    raise ValidationError('El peso para un ave parece muy alto (máximo recomendado: 5 kg).')
        
        return peso
    
    def clean_edad(self):
        """Validar edad de la mascota"""
        edad = self.cleaned_data.get('edad')
        tipo_animal = self.cleaned_data.get('tipo_animal')
        
        if edad is not None:
            if edad < 0:
                raise ValidationError('La edad no puede ser negativa.')
            if edad > 50:
                raise ValidationError('La edad parece demasiado alta. Máximo 50 años.')
            
            # Validaciones específicas por tipo de animal
            if tipo_animal:
                if tipo_animal.nombre.lower() == 'gato' and edad > 25:
                    raise ValidationError('La edad para un gato parece muy alta (máximo típico: 25 años).')
                elif tipo_animal.nombre.lower() == 'perro' and edad > 20:
                    raise ValidationError('La edad para un perro parece muy alta (máximo típico: 20 años).')
        
        return edad
    
    def clean_propietario_nombre(self):
        """Validar nombre del propietario"""
        nombre = self.cleaned_data.get('propietario_nombre')
        if nombre:
            if len(nombre.strip()) < 3:
                raise ValidationError('El nombre del propietario debe tener al menos 3 caracteres.')
            if len(nombre) > 100:
                raise ValidationError('El nombre es demasiado largo. Máximo 100 caracteres.')
            # Solo letras, espacios y algunos caracteres especiales
            if not re.match(r'^[a-zA-ZáéíóúñüÁÉÍÓÚÑÜ\s\-\'\.]+$', nombre):
                raise ValidationError('El nombre solo puede contener letras, espacios, guiones y apostrofes.')
        return nombre.strip() if nombre else nombre
    
    def clean_propietario_telefono(self):
        """Validar teléfono del propietario"""
        telefono = self.cleaned_data.get('propietario_telefono')
        if telefono:
            # Limpiar espacios y caracteres especiales
            telefono_limpio = re.sub(r'[^\d\+\-\(\)\s]', '', telefono)
            
            # Validar formato básico
            if not re.match(r'^[\+]?[\d\-\(\)\s]{7,20}$', telefono_limpio):
                raise ValidationError('Formato de teléfono inválido. Use solo números, +, -, ( ) y espacios.')
            
            # Verificar longitud mínima de dígitos
            digitos = re.sub(r'[^\d]', '', telefono_limpio)
            if len(digitos) < 7:
                raise ValidationError('El teléfono debe tener al menos 7 dígitos.')
            if len(digitos) > 15:
                raise ValidationError('El teléfono tiene demasiados dígitos.')
                
        return telefono
    
    def clean_propietario_email(self):
        """Validar email del propietario"""
        email = self.cleaned_data.get('propietario_email')
        if email:
            # Validar formato básico
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                raise ValidationError('Formato de email inválido.')
            if len(email) > 100:
                raise ValidationError('El email es demasiado largo. Máximo 100 caracteres.')
        return email.lower() if email else email
    
    def clean_numero_chip(self):
        """Validar número de chip"""
        numero_chip = self.cleaned_data.get('numero_chip')
        if numero_chip:
            numero_chip = numero_chip.strip().upper()
            
            # Validar formato (15 dígitos hexadecimales típicamente)
            if not re.match(r'^[A-F0-9]{10,20}$', numero_chip):
                raise ValidationError('El número de chip debe tener entre 10-20 caracteres alfanuméricos.')
            
            # Verificar unicidad
            mascotas = Mascota.objects.filter(numero_chip=numero_chip)
            if self.instance and self.instance.pk:
                mascotas = mascotas.exclude(pk=self.instance.pk)
            
            if mascotas.exists():
                raise ValidationError('Ya existe una mascota con este número de chip.')
        
        return numero_chip


class CitaForm(forms.ModelForm):
    """
    Formulario para crear y editar citas veterinarias.
    Utiliza crispy forms para un mejor diseño con Bootstrap.
    """
    
    class Meta:
        model = Cita
        fields = [
            'mascota', 'fecha_hora', 'tipo_cita', 'estado', 
            'motivo', 'observaciones', 'veterinario', 'precio_estimado'
        ]
        widgets = {
            'fecha_hora': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'motivo': forms.Textarea(attrs={'rows': 3}),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
            'precio_estimado': forms.NumberInput(attrs={'step': '0.01'}),
        }
        labels = {
            'mascota': 'Mascota *',
            'fecha_hora': 'Fecha y Hora *',
            'tipo_cita': 'Tipo de Cita *',
            'estado': 'Estado *',
            'motivo': 'Motivo de la Consulta *',
            'observaciones': 'Observaciones (opcional)',
            'veterinario': 'Veterinario Asignado (opcional)',
            'precio_estimado': 'Precio Estimado CLP $ (opcional)',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        
        # Solo mostrar mascotas activas
        self.fields['mascota'].queryset = Mascota.objects.filter(activo=True).order_by('nombre')
        
        # Configurar el layout del formulario
        self.helper.layout = Layout(
            HTML('<div class="card">'),
            HTML('<div class="card-header"><h5>Información de la Cita</h5></div>'),
            HTML('<div class="card-body">'),
            Row(
                Column('mascota', css_class='form-group col-md-6 mb-3'),
                Column('fecha_hora', css_class='form-group col-md-6 mb-3'),
            ),
            Row(
                Column('tipo_cita', css_class='form-group col-md-6 mb-3'),
                Column('estado', css_class='form-group col-md-6 mb-3'),
            ),
            'motivo',
            HTML('</div></div>'),
            
            HTML('<div class="card mt-3">'),
            HTML('<div class="card-header"><h5>Detalles Adicionales</h5></div>'),
            HTML('<div class="card-body">'),
            Row(
                Column('veterinario', css_class='form-group col-md-6 mb-3'),
                Column('precio_estimado', css_class='form-group col-md-6 mb-3'),
            ),
            'observaciones',
            HTML('</div></div>'),
            
            Div(
                Submit('submit', 'Guardar Cita', css_class='btn btn-primary me-2'),
                HTML('<a href="{% url "cita_list" %}" class="btn btn-secondary">Cancelar</a>'),
                css_class='mt-3 text-center'
            )
        )
    
    def clean_fecha_hora(self):
        """Validar fecha y hora de la cita"""
        fecha_hora = self.cleaned_data.get('fecha_hora')
        if fecha_hora:
            ahora = timezone.now()
            
            # Solo validar fecha futura para citas nuevas (no edición)
            if not self.instance.pk and fecha_hora <= ahora:
                raise ValidationError('La fecha y hora de la cita debe ser en el futuro.')
            
            # Validar que no sea demasiado lejana (máximo 1 año)
            if fecha_hora > ahora.replace(year=ahora.year + 1):
                raise ValidationError('No se pueden programar citas con más de 1 año de anticipación.')
            
            # Validar horario de atención (8 AM - 8 PM)
            if fecha_hora.hour < 8 or fecha_hora.hour >= 20:
                raise ValidationError('Las citas deben programarse entre las 8:00 AM y las 8:00 PM.')
            
            # Validar que no sea domingo
            if fecha_hora.weekday() == 6:  # Domingo = 6
                raise ValidationError('No se atiende los domingos.')
            
            # Verificar conflictos de horario (opcional - solo para citas confirmadas)
            estado = self.cleaned_data.get('estado')
            if estado in ['confirmada', 'en_curso']:
                # Buscar citas en la misma hora ±30 minutos
                inicio = fecha_hora - timezone.timedelta(minutes=30)
                fin = fecha_hora + timezone.timedelta(minutes=30)
                
                citas_conflicto = Cita.objects.filter(
                    fecha_hora__range=(inicio, fin),
                    estado__in=['confirmada', 'en_curso']
                )
                
                if self.instance.pk:
                    citas_conflicto = citas_conflicto.exclude(pk=self.instance.pk)
                
                if citas_conflicto.exists():
                    raise ValidationError('Ya existe una cita confirmada en este horario (±30 minutos).')
        
        return fecha_hora
    
    def clean_motivo(self):
        """Validar motivo de la consulta"""
        motivo = self.cleaned_data.get('motivo')
        if motivo:
            if len(motivo.strip()) < 10:
                raise ValidationError('El motivo debe tener al menos 10 caracteres.')
            if len(motivo) > 500:
                raise ValidationError('El motivo es demasiado largo. Máximo 500 caracteres.')
        return motivo.strip() if motivo else motivo
    
    def clean_veterinario(self):
        """Validar nombre del veterinario"""
        veterinario = self.cleaned_data.get('veterinario')
        if veterinario:
            if len(veterinario.strip()) < 3:
                raise ValidationError('El nombre del veterinario debe tener al menos 3 caracteres.')
            if not re.match(r'^[a-zA-ZáéíóúñüÁÉÍÓÚÑÜ\s\-\'\.]+$', veterinario):
                raise ValidationError('El nombre del veterinario solo puede contener letras, espacios, guiones y apostrofes.')
        return veterinario.strip() if veterinario else veterinario
    
    def clean_precio_estimado(self):
        """Validar precio estimado"""
        precio = self.cleaned_data.get('precio_estimado')
        if precio is not None:
            if precio < 0:
                raise ValidationError('El precio no puede ser negativo.')
            if precio == 0:
                raise ValidationError('El precio debe ser mayor a 0.')
            if precio > Decimal('1000000'):
                raise ValidationError('El precio estimado es demasiado alto. Máximo: $1,000,000.')
        return precio
    
    def clean(self):
        """Validaciones que involucran múltiples campos"""
        cleaned_data = super().clean()
        estado = cleaned_data.get('estado')
        fecha_hora = cleaned_data.get('fecha_hora')
        tipo_cita = cleaned_data.get('tipo_cita')
        precio_estimado = cleaned_data.get('precio_estimado')
        
        # Validar coherencia entre estado y fecha
        if estado == 'completada' and fecha_hora:
            if fecha_hora > timezone.now():
                raise ValidationError('Una cita no puede estar completada si es en el futuro.')
        
        # Para emergencias, recomendar precio
        if tipo_cita == 'emergencia' and not precio_estimado:
            self.add_error('precio_estimado', 'Se recomienda establecer un precio estimado para emergencias.')
        
        # Para cirugías, requerir veterinario
        if tipo_cita == 'cirugia' and not cleaned_data.get('veterinario'):
            self.add_error('veterinario', 'Es obligatorio asignar un veterinario para cirugías.')
        
        return cleaned_data
