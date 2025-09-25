from django.core.management.base import BaseCommand
from veterinaria.models import TipoAnimal

class Command(BaseCommand):
    help = 'Crea tipos de animales por defecto para la veterinaria'

    def handle(self, *args, **options):
        animales_defecto = [
            {
                'nombre': 'Perro',
                'descripcion': 'Caninos domésticos de todas las razas y tamaños'
            },
            {
                'nombre': 'Gato',
                'descripcion': 'Felinos domésticos de todas las razas'
            },
            {
                'nombre': 'Conejo',
                'descripcion': 'Conejos domésticos y de granja'
            },
            {
                'nombre': 'Hámster',
                'descripcion': 'Roedores pequeños domésticos'
            },
            {
                'nombre': 'Cobayo',
                'descripcion': 'Cobayas o conejillos de indias'
            },
            {
                'nombre': 'Ave',
                'descripcion': 'Aves domésticas (loros, canarios, etc.)'
            },
            {
                'nombre': 'Pez',
                'descripcion': 'Peces ornamentales de acuario'
            },
            {
                'nombre': 'Reptil',
                'descripcion': 'Reptiles domésticos (iguanas, tortugas, etc.)'
            },
            {
                'nombre': 'Hurón',
                'descripcion': 'Hurones domésticos'
            },
            {
                'nombre': 'Chinchilla',
                'descripcion': 'Chinchillas domésticas'
            }
        ]

        created_count = 0
        
        for animal_data in animales_defecto:
            tipo_animal, created = TipoAnimal.objects.get_or_create(
                nombre=animal_data['nombre'],
                defaults={'descripcion': animal_data['descripcion']}
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Creado: {tipo_animal.nombre}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'- Ya existe: {tipo_animal.nombre}')
                )
        
        if created_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f'\n¡Éxito! Se crearon {created_count} tipos de animales.')
            )
        else:
            self.stdout.write(
                self.style.WARNING('\nTodos los tipos de animales ya existían.')
            )
