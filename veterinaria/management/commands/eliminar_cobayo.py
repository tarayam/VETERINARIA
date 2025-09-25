from django.core.management.base import BaseCommand
from veterinaria.models import TipoAnimal

class Command(BaseCommand):
    help = 'Elimina el tipo de animal Cobayo'

    def handle(self, *args, **options):
        try:
            cobayo = TipoAnimal.objects.get(nombre='Cobayo')
            cobayo.delete()
            self.stdout.write(
                self.style.SUCCESS('✓ Cobayo eliminado exitosamente')
            )
        except TipoAnimal.DoesNotExist:
            self.stdout.write(
                self.style.WARNING('- Cobayo no encontrado (ya fue eliminado)')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error al eliminar Cobayo: {e}')
            )
