from django.core.management.base import BaseCommand
from veterinaria.models import Veterinario
from datetime import date

class Command(BaseCommand):
    help = 'Crear veterinarios de ejemplo para la clínica'

    def handle(self, *args, **options):
        veterinarios = [
            {
                'nombre': 'María González',
                'especialidad': 'Medicina General',
                'telefono': '+56912345678',
                'email': 'maria.gonzalez@veterinaria.com',
                'numero_colegiado': 'CV001',
                'fecha_ingreso': date(2020, 1, 15),
            },
            {
                'nombre': 'Carlos Rodríguez',
                'especialidad': 'Cirugía Veterinaria',
                'telefono': '+56912345679',
                'email': 'carlos.rodriguez@veterinaria.com',
                'numero_colegiado': 'CV002',
                'fecha_ingreso': date(2019, 3, 10),
            },
            {
                'nombre': 'Ana Martínez',
                'especialidad': 'Dermatología Veterinaria',
                'telefono': '+56912345680',
                'email': 'ana.martinez@veterinaria.com',
                'numero_colegiado': 'CV003',
                'fecha_ingreso': date(2021, 7, 20),
            },
            {
                'nombre': 'José Silva',
                'especialidad': 'Cardiología Veterinaria',
                'telefono': '+56912345681',
                'email': 'jose.silva@veterinaria.com',
                'numero_colegiado': 'CV004',
                'fecha_ingreso': date(2018, 11, 5),
            },
            {
                'nombre': 'Patricia López',
                'especialidad': 'Medicina Interna',
                'telefono': '+56912345682',
                'email': 'patricia.lopez@veterinaria.com',
                'numero_colegiado': 'CV005',
                'fecha_ingreso': date(2022, 2, 14),
            }
        ]

        created_count = 0
        for vet_data in veterinarios:
            veterinario, created = Veterinario.objects.get_or_create(
                nombre=vet_data['nombre'],
                defaults=vet_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Creado veterinario: Dr. {veterinario.nombre}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Veterinario ya existe: Dr. {veterinario.nombre}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Proceso completado. {created_count} veterinarios creados.')
        )