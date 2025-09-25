from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from veterinaria.models import Cita, Mascota
import random

class Command(BaseCommand):
    help = 'Crear citas de ejemplo para probar el sistema'

    def handle(self, *args, **options):
        # Verificar que existan mascotas
        mascotas = list(Mascota.objects.filter(activo=True))
        if not mascotas:
            self.stdout.write(
                self.style.ERROR('No hay mascotas activas. Primero cree algunas mascotas.')
            )
            return

        # Datos de ejemplo para citas
        tipos_cita = ['consulta_general', 'vacunacion', 'control', 'cirugia', 'estetica']
        estados = ['programada', 'confirmada', 'completada']
        motivos = [
            'Control de rutina',
            'Vacunación anual',
            'Revisión post-operatoria',
            'Consulta por síntomas digestivos',
            'Chequeo general de salud',
            'Aplicación de vacunas',
            'Revisión dental',
            'Control de peso',
            'Consulta dermatológica',
            'Examen de sangre'
        ]
        veterinarios = [
            'Dr. García López',
            'Dra. María Rodríguez',
            'Dr. Carlos Mendoza',
            'Dra. Ana Pérez',
            'Dr. Luis Hernández'
        ]

        # Crear citas de ejemplo
        citas_creadas = 0
        for i in range(10):  # Crear 10 citas de ejemplo
            # Fecha aleatoria en los próximos 30 días
            fecha_base = timezone.now() + timedelta(days=random.randint(1, 30))
            hora = random.randint(9, 17)  # Entre 9 AM y 5 PM
            minuto = random.choice([0, 30])  # Solo en punto o media hora
            
            fecha_hora = fecha_base.replace(
                hour=hora, 
                minute=minuto, 
                second=0, 
                microsecond=0
            )
            
            cita = Cita.objects.create(
                mascota=random.choice(mascotas),
                fecha_hora=fecha_hora,
                tipo_cita=random.choice(tipos_cita),
                estado=random.choice(estados),
                motivo=random.choice(motivos),
                veterinario=random.choice(veterinarios),
                precio_estimado=random.randint(15000, 80000),
                observaciones=f'Cita de ejemplo creada automáticamente #{i+1}'
            )
            citas_creadas += 1

        self.stdout.write(
            self.style.SUCCESS(f'Se crearon {citas_creadas} citas de ejemplo exitosamente.')
        )