from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Crear superusuario de forma automática'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@veterinaria.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Superusuario creado exitosamente'))
            self.stdout.write('Usuario: admin')
            self.stdout.write('Email: admin@veterinaria.com')
            self.stdout.write('Contraseña: admin123')
        else:
            self.stdout.write('El superusuario ya existe')
