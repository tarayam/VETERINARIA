import os
from django.core.management.base import BaseCommand
from django.utils import translation

class Command(BaseCommand):
    help = 'Fuerza la configuración de idioma español'

    def handle(self, *args, **options):
        # Forzar el idioma español
        translation.activate('es')
        os.environ['LANGUAGE'] = 'es'
        os.environ['LC_ALL'] = 'es_ES.UTF-8'
        
        self.stdout.write(
            self.style.SUCCESS('Idioma configurado correctamente a español')
        )
