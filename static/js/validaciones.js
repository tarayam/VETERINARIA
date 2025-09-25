// Validaciones en tiempo real para formularios del sistema veterinario

document.addEventListener('DOMContentLoaded', function() {
    // Validación de nombres (mascotas, propietarios)
    const nombreInputs = document.querySelectorAll('input[name*="nombre"]');
    nombreInputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateNombre(this);
        });
        input.addEventListener('input', function() {
            clearValidationMessage(this);
        });
    });

    // Validación de teléfonos
    const telefonoInputs = document.querySelectorAll('input[name*="telefono"]');
    telefonoInputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateTelefono(this);
        });
        input.addEventListener('input', function() {
            formatTelefono(this);
        });
    });

    // Validación de emails
    const emailInputs = document.querySelectorAll('input[type="email"]');
    emailInputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateEmail(this);
        });
    });

    // Validación de precios
    const precioInputs = document.querySelectorAll('input[name*="precio"]');
    precioInputs.forEach(input => {
        input.addEventListener('blur', function() {
            validatePrecio(this);
        });
    });

    // Validación de peso y edad
    const pesoInputs = document.querySelectorAll('input[name="peso"]');
    pesoInputs.forEach(input => {
        input.addEventListener('blur', function() {
            validatePeso(this);
        });
    });

    const edadInputs = document.querySelectorAll('input[name="edad"]');
    edadInputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateEdad(this);
        });
    });

    // Validación de fechas de citas
    const fechaCitaInputs = document.querySelectorAll('input[name="fecha_hora"]');
    fechaCitaInputs.forEach(input => {
        input.addEventListener('change', function() {
            validateFechaCita(this);
        });
    });

    // Validación de códigos de producto
    const codigoInputs = document.querySelectorAll('input[name="codigo"]');
    codigoInputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateCodigo(this);
        });
        input.addEventListener('input', function() {
            this.value = this.value.toUpperCase();
        });
    });

    // Validación de stock
    const stockInputs = document.querySelectorAll('input[name="stock"]');
    stockInputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateStock(this);
        });
    });
});

// Función para validar nombres
function validateNombre(input) {
    const value = input.value.trim();
    const minLength = input.name.includes('propietario') ? 3 : 2;
    
    clearValidationMessage(input);
    
    if (value.length > 0 && value.length < minLength) {
        showValidationMessage(input, `El nombre debe tener al menos ${minLength} caracteres.`, 'error');
        return false;
    }
    
    if (value.length > 100) {
        showValidationMessage(input, 'El nombre es demasiado largo (máximo 100 caracteres).', 'error');
        return false;
    }
    
    const regex = /^[a-zA-ZáéíóúñüÁÉÍÓÚÑÜ\s\-'\.]+$/;
    if (value.length > 0 && !regex.test(value)) {
        showValidationMessage(input, 'El nombre solo puede contener letras, espacios, guiones y apostrofes.', 'error');
        return false;
    }
    
    if (value.length >= minLength) {
        showValidationMessage(input, 'Nombre válido.', 'success');
        return true;
    }
    
    return true;
}

// Función para validar teléfonos
function validateTelefono(input) {
    const value = input.value.trim();
    
    clearValidationMessage(input);
    
    if (value.length === 0) return true; // Campo opcional
    
    const digitos = value.replace(/[^\d]/g, '');
    
    if (digitos.length < 7) {
        showValidationMessage(input, 'El teléfono debe tener al menos 7 dígitos.', 'error');
        return false;
    }
    
    if (digitos.length > 15) {
        showValidationMessage(input, 'El teléfono tiene demasiados dígitos.', 'error');
        return false;
    }
    
    const regex = /^[\+]?[\d\-\(\)\s]{7,20}$/;
    if (!regex.test(value)) {
        showValidationMessage(input, 'Formato de teléfono inválido.', 'error');
        return false;
    }
    
    showValidationMessage(input, 'Teléfono válido.', 'success');
    return true;
}

// Función para formatear teléfonos automáticamente
function formatTelefono(input) {
    let value = input.value.replace(/[^\d\+\-\(\)\s]/g, '');
    input.value = value;
}

// Función para validar emails
function validateEmail(input) {
    const value = input.value.trim();
    
    clearValidationMessage(input);
    
    if (value.length === 0) return true; // Campo opcional
    
    const regex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    if (!regex.test(value)) {
        showValidationMessage(input, 'Formato de email inválido.', 'error');
        return false;
    }
    
    if (value.length > 100) {
        showValidationMessage(input, 'El email es demasiado largo (máximo 100 caracteres).', 'error');
        return false;
    }
    
    showValidationMessage(input, 'Email válido.', 'success');
    return true;
}

// Función para validar precios
function validatePrecio(input) {
    const value = parseFloat(input.value);
    
    clearValidationMessage(input);
    
    if (isNaN(value)) return true; // Campo opcional
    
    if (value < 0) {
        showValidationMessage(input, 'El precio no puede ser negativo.', 'error');
        return false;
    }
    
    if (value === 0) {
        showValidationMessage(input, 'El precio debe ser mayor a 0.', 'error');
        return false;
    }
    
    const maxPrecio = input.name.includes('estimado') ? 1000000 : 10000000;
    if (value > maxPrecio) {
        showValidationMessage(input, `El precio es demasiado alto (máximo: $${maxPrecio.toLocaleString()}).`, 'error');
        return false;
    }
    
    showValidationMessage(input, 'Precio válido.', 'success');
    return true;
}

// Función para validar peso
function validatePeso(input) {
    const value = parseFloat(input.value);
    
    clearValidationMessage(input);
    
    if (isNaN(value)) return true; // Campo opcional
    
    if (value <= 0) {
        showValidationMessage(input, 'El peso debe ser mayor a 0.', 'error');
        return false;
    }
    
    if (value > 200) {
        showValidationMessage(input, 'El peso parece demasiado alto (máximo 200 kg).', 'error');
        return false;
    }
    
    // Advertencias basadas en rangos típicos
    if (value > 100) {
        showValidationMessage(input, 'Peso alto. Verifique que sea correcto.', 'warning');
    } else {
        showValidationMessage(input, 'Peso válido.', 'success');
    }
    
    return true;
}

// Función para validar edad
function validateEdad(input) {
    const value = parseInt(input.value);
    
    clearValidationMessage(input);
    
    if (isNaN(value)) return true; // Campo opcional
    
    if (value < 0) {
        showValidationMessage(input, 'La edad no puede ser negativa.', 'error');
        return false;
    }
    
    if (value > 50) {
        showValidationMessage(input, 'La edad parece demasiado alta (máximo 50 años).', 'error');
        return false;
    }
    
    // Advertencias basadas en rangos típicos
    if (value > 25) {
        showValidationMessage(input, 'Edad alta. Verifique que sea correcta.', 'warning');
    } else {
        showValidationMessage(input, 'Edad válida.', 'success');
    }
    
    return true;
}

// Función para validar fechas de citas
function validateFechaCita(input) {
    const value = new Date(input.value);
    const now = new Date();
    
    clearValidationMessage(input);
    
    if (isNaN(value.getTime())) return true;
    
    if (value <= now) {
        showValidationMessage(input, 'La fecha debe ser en el futuro.', 'error');
        return false;
    }
    
    const unAnoAdelante = new Date();
    unAnoAdelante.setFullYear(unAnoAdelante.getFullYear() + 1);
    
    if (value > unAnoAdelante) {
        showValidationMessage(input, 'No se pueden programar citas con más de 1 año de anticipación.', 'error');
        return false;
    }
    
    if (value.getHours() < 8 || value.getHours() >= 20) {
        showValidationMessage(input, 'Las citas deben ser entre 8:00 AM y 8:00 PM.', 'error');
        return false;
    }
    
    if (value.getDay() === 0) { // Domingo
        showValidationMessage(input, 'No se atiende los domingos.', 'error');
        return false;
    }
    
    showValidationMessage(input, 'Fecha válida.', 'success');
    return true;
}

// Función para validar códigos de producto
function validateCodigo(input) {
    const value = input.value.trim();
    
    clearValidationMessage(input);
    
    if (value.length === 0) return true; // Campo opcional
    
    if (value.length < 3 || value.length > 20) {
        showValidationMessage(input, 'El código debe tener entre 3-20 caracteres.', 'error');
        return false;
    }
    
    const regex = /^[A-Z0-9\-_]+$/;
    if (!regex.test(value)) {
        showValidationMessage(input, 'El código solo puede contener letras, números, guiones y guiones bajos.', 'error');
        return false;
    }
    
    showValidationMessage(input, 'Código válido.', 'success');
    return true;
}

// Función para validar stock
function validateStock(input) {
    const value = parseInt(input.value);
    
    clearValidationMessage(input);
    
    if (isNaN(value)) return true; // Campo opcional
    
    if (value < 0) {
        showValidationMessage(input, 'El stock no puede ser negativo.', 'error');
        return false;
    }
    
    if (value > 100000) {
        showValidationMessage(input, 'El stock es demasiado alto (máximo 100,000).', 'error');
        return false;
    }
    
    showValidationMessage(input, 'Stock válido.', 'success');
    return true;
}

// Función para mostrar mensajes de validación
function showValidationMessage(input, message, type) {
    clearValidationMessage(input);
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `validation-message ${type}`;
    messageDiv.textContent = message;
    
    // Agregar icono según el tipo
    const icon = document.createElement('i');
    if (type === 'error') {
        icon.className = 'fas fa-exclamation-circle';
        input.classList.add('is-invalid');
        input.classList.remove('is-valid');
    } else if (type === 'success') {
        icon.className = 'fas fa-check-circle';
        input.classList.add('is-valid');
        input.classList.remove('is-invalid');
    } else if (type === 'warning') {
        icon.className = 'fas fa-exclamation-triangle';
        input.classList.remove('is-invalid', 'is-valid');
    }
    
    messageDiv.insertBefore(icon, messageDiv.firstChild);
    
    // Insertar después del input
    input.parentNode.insertBefore(messageDiv, input.nextSibling);
}

// Función para limpiar mensajes de validación
function clearValidationMessage(input) {
    input.classList.remove('is-invalid', 'is-valid');
    
    const nextSibling = input.nextSibling;
    if (nextSibling && nextSibling.classList && nextSibling.classList.contains('validation-message')) {
        nextSibling.remove();
    }
}

// Validación general del formulario antes del envío
function validateForm(form) {
    let isValid = true;
    
    // Validar todos los campos
    const inputs = form.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        if (input.name.includes('nombre')) {
            if (!validateNombre(input)) isValid = false;
        } else if (input.name.includes('telefono')) {
            if (!validateTelefono(input)) isValid = false;
        } else if (input.type === 'email') {
            if (!validateEmail(input)) isValid = false;
        } else if (input.name.includes('precio')) {
            if (!validatePrecio(input)) isValid = false;
        } else if (input.name === 'peso') {
            if (!validatePeso(input)) isValid = false;
        } else if (input.name === 'edad') {
            if (!validateEdad(input)) isValid = false;
        } else if (input.name === 'fecha_hora') {
            if (!validateFechaCita(input)) isValid = false;
        } else if (input.name === 'codigo') {
            if (!validateCodigo(input)) isValid = false;
        } else if (input.name === 'stock') {
            if (!validateStock(input)) isValid = false;
        }
    });
    
    return isValid;
}

// Interceptar envío de formularios para validación
document.addEventListener('submit', function(e) {
    const form = e.target;
    if (form.tagName === 'FORM' && form.method.toLowerCase() === 'post') {
        if (!validateForm(form)) {
            e.preventDefault();
            
            // Mostrar alerta general
            const alert = document.createElement('div');
            alert.className = 'form-alert form-alert-danger';
            alert.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Por favor, corrija los errores antes de continuar.';
            
            form.insertBefore(alert, form.firstChild);
            
            // Scroll al primer error
            const firstError = form.querySelector('.is-invalid');
            if (firstError) {
                firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                firstError.focus();
            }
            
            // Remover alerta después de 5 segundos
            setTimeout(() => {
                if (alert.parentNode) {
                    alert.remove();
                }
            }, 5000);
        }
    }
});