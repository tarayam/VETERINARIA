from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.utils import timezone
import re
from decimal import Decimal

class FlexibleUsernameValidator:
    """
    Validador flexible para nombres de usuario que permite espacios
    """
    def __init__(self):
        self.regex = re.compile(r'^[\w\s@.+-]+$')
        
    def __call__(self, value):
        if not self.regex.match(value):
            raise ValidationError(
                _('Introduzca un nombre de usuario válido. Puede contener letras, números, espacios y los caracteres @/./+/-/_'),
                code='invalid_username',
            )
            
    def __eq__(self, other):
        return isinstance(other, self.__class__)
        
    def __hash__(self):
        return hash(self.__class__)

def validar_password_simple(password):
    """
    Validador simple de contraseña que permite letras y números
    """
    if len(password) < 4:
        raise ValidationError(
            _('La contraseña debe tener al menos 4 caracteres.'),
            code='password_too_short',
        )
    
    # Verificar que tenga al menos una letra o un número
    if not re.search(r'[a-zA-Z0-9]', password):
        raise ValidationError(
            _('La contraseña debe contener al menos una letra o número.'),
            code='password_invalid',
        )

# Validadores adicionales para el sistema veterinario

def validar_nombre_mascota(value):
    """Validar nombre de mascota"""
    if not value or len(value.strip()) < 2:
        raise ValidationError(_('El nombre debe tener al menos 2 caracteres.'))
    
    if len(value) > 50:
        raise ValidationError(_('El nombre es demasiado largo (máximo 50 caracteres).'))
    
    if not re.match(r'^[a-zA-ZáéíóúñüÁÉÍÓÚÑÜ\s\-\'\.]+$', value):
        raise ValidationError(_('El nombre solo puede contener letras, espacios, guiones y apostrofes.'))

def validar_peso_mascota(value):
    """Validar peso de mascota"""
    if value is not None:
        if value <= 0:
            raise ValidationError(_('El peso debe ser mayor a 0.'))
        if value > 200:
            raise ValidationError(_('El peso parece demasiado alto (máximo 200 kg).'))

def validar_edad_mascota(value):
    """Validar edad de mascota"""
    if value is not None:
        if value < 0:
            raise ValidationError(_('La edad no puede ser negativa.'))
        if value > 50:
            raise ValidationError(_('La edad parece demasiado alta (máximo 50 años).'))

def validar_telefono(value):
    """Validar formato de teléfono"""
    if value:
        # Limpiar espacios y caracteres especiales
        telefono_limpio = re.sub(r'[^\d\+\-\(\)\s]', '', value)
        
        # Validar formato básico
        if not re.match(r'^[\+]?[\d\-\(\)\s]{7,20}$', telefono_limpio):
            raise ValidationError(_('Formato de teléfono inválido.'))
        
        # Verificar longitud mínima de dígitos
        digitos = re.sub(r'[^\d]', '', telefono_limpio)
        if len(digitos) < 7:
            raise ValidationError(_('El teléfono debe tener al menos 7 dígitos.'))
        if len(digitos) > 15:
            raise ValidationError(_('El teléfono tiene demasiados dígitos.'))

def validar_email_propietario(value):
    """Validar email del propietario"""
    if value:
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
            raise ValidationError(_('Formato de email inválido.'))
        if len(value) > 100:
            raise ValidationError(_('El email es demasiado largo (máximo 100 caracteres).'))

def validar_codigo_producto(value):
    """Validar código de producto"""
    if value:
        value = value.strip().upper()
        if not re.match(r'^[A-Z0-9\-_]{3,20}$', value):
            raise ValidationError(_('El código debe tener entre 3-20 caracteres alfanuméricos.'))

def validar_precio_positivo(value):
    """Validar que el precio sea positivo"""
    if value is not None:
        if value < 0:
            raise ValidationError(_('El precio no puede ser negativo.'))
        if value == 0:
            raise ValidationError(_('El precio debe ser mayor a 0.'))
        if value > Decimal('10000000'):
            raise ValidationError(_('El precio es demasiado alto.'))

def validar_stock_producto(value):
    """Validar stock de producto"""
    if value is not None:
        if value < 0:
            raise ValidationError(_('El stock no puede ser negativo.'))
        if value > 100000:
            raise ValidationError(_('El stock es demasiado alto (máximo 100,000).'))

def validar_numero_chip(value):
    """Validar número de microchip"""
    if value:
        value = value.strip().upper()
        if not re.match(r'^[A-F0-9]{10,20}$', value):
            raise ValidationError(_('El número de chip debe tener entre 10-20 caracteres alfanuméricos.'))

def validar_fecha_cita_futura(value):
    """Validar que la fecha de cita sea futura"""
    if value and value <= timezone.now():
        raise ValidationError(_('La fecha y hora de la cita debe ser en el futuro.'))

def validar_horario_atencion(value):
    """Validar horario de atención"""
    if value:
        if value.hour < 8 or value.hour >= 20:
            raise ValidationError(_('Las citas deben programarse entre las 8:00 AM y las 8:00 PM.'))
        
        if value.weekday() == 6:  # Domingo = 6
            raise ValidationError(_('No se atiende los domingos.'))

def validar_nombre_propietario(value):
    """Validar nombre del propietario"""
    if not value or len(value.strip()) < 3:
        raise ValidationError(_('El nombre debe tener al menos 3 caracteres.'))
    
    if len(value) > 100:
        raise ValidationError(_('El nombre es demasiado largo (máximo 100 caracteres).'))
    
    if not re.match(r'^[a-zA-ZáéíóúñüÁÉÍÓÚÑÜ\s\-\'\.]+$', value):
        raise ValidationError(_('El nombre solo puede contener letras, espacios, guiones y apostrofes.'))

def validar_motivo_consulta(value):
    """Validar motivo de consulta"""
    if value:
        if len(value.strip()) < 10:
            raise ValidationError(_('El motivo debe tener al menos 10 caracteres.'))
        if len(value) > 500:
            raise ValidationError(_('El motivo es demasiado largo (máximo 500 caracteres).'))

def validar_descripcion_producto(value):
    """Validar descripción de producto"""
    if value:
        if len(value.strip()) < 10:
            raise ValidationError(_('La descripción debe tener al menos 10 caracteres.'))
        if len(value) > 1000:
            raise ValidationError(_('La descripción es demasiado larga (máximo 1000 caracteres).'))
