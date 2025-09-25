from django.core.management.base import BaseCommand
from veterinaria.models import Categoria

class Command(BaseCommand):
    help = 'Crea categorías por defecto para productos veterinarios'

    def handle(self, *args, **options):
        categorias_defecto = [
            {
                'nombre': 'Medicamentos',
                'descripcion': 'Medicamentos y fármacos para tratamiento veterinario'
            },
            {
                'nombre': 'Alimentos',
                'descripcion': 'Alimentos balanceados y suplementos nutricionales para mascotas'
            },
            {
                'nombre': 'Accesorios',
                'descripcion': 'Collares, correas, juguetes y accesorios para mascotas'
            },
            {
                'nombre': 'Higiene y Cuidado',
                'descripcion': 'Productos de higiene, shampoos y cuidado personal para mascotas'
            },
            {
                'nombre': 'Servicios Veterinarios',
                'descripcion': 'Consultas, vacunaciones y procedimientos médicos'
            },
            {
                'nombre': 'Equipos Médicos',
                'descripcion': 'Instrumental y equipos médicos veterinarios'
            }
        ]

        created_count = 0
        
        for categoria_data in categorias_defecto:
            categoria, created = Categoria.objects.get_or_create(
                nombre=categoria_data['nombre'],
                defaults={'descripcion': categoria_data['descripcion']}
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Creada: {categoria.nombre}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'- Ya existe: {categoria.nombre}')
                )
        
        if created_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f'\n¡Éxito! Se crearon {created_count} categorías.')
            )
        else:
            self.stdout.write(
                self.style.WARNING('\nTodas las categorías ya existían.')
            )
