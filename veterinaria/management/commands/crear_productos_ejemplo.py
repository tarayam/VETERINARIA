from django.core.management.base import BaseCommand
from veterinaria.models import Categoria, Producto

class Command(BaseCommand):
    help = 'Crea productos de ejemplo con precios en pesos chilenos'

    def handle(self, *args, **options):
        # Obtener categorías
        try:
            medicamentos = Categoria.objects.get(nombre='Medicamentos')
            alimentos = Categoria.objects.get(nombre='Alimentos')
            accesorios = Categoria.objects.get(nombre='Accesorios')
            higiene = Categoria.objects.get(nombre='Higiene y Cuidado')
            servicios = Categoria.objects.get(nombre='Servicios Veterinarios')
        except Categoria.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('Error: Primero debes crear las categorías ejecutando: python manage.py crear_categorias')
            )
            return

        productos_ejemplo = [
            # Medicamentos
            {
                'categoria': medicamentos,
                'nombre': 'Antibiótico Amoxicilina',
                'descripcion': 'Antibiótico de amplio espectro para infecciones bacterianas',
                'tipo_producto': 'medicamento',
                'precio': 15990,
                'codigo': 'MED001',
                'stock': 25,
                'principio_activo': 'Amoxicilina',
                'concentracion': '500mg',
                'laboratorio': 'VetPharm Chile'
            },
            {
                'categoria': medicamentos,
                'nombre': 'Antiinflamatorio Meloxicam',
                'descripcion': 'Antiinflamatorio no esteroidal para dolor articular',
                'tipo_producto': 'medicamento',
                'precio': 23500,
                'codigo': 'MED002',
                'stock': 15,
                'principio_activo': 'Meloxicam',
                'concentracion': '20mg/ml',
                'laboratorio': 'VetSalud'
            },
            
            # Alimentos
            {
                'categoria': alimentos,
                'nombre': 'Alimento Premium Perro Adulto',
                'descripcion': 'Alimento balanceado para perros adultos de todas las razas',
                'tipo_producto': 'alimento',
                'precio': 35990,
                'codigo': 'ALI001',
                'stock': 50
            },
            {
                'categoria': alimentos,
                'nombre': 'Alimento Gato Castrado',
                'descripcion': 'Alimento especializado para gatos castrados control de peso',
                'tipo_producto': 'alimento',
                'precio': 28990,
                'codigo': 'ALI002',
                'stock': 30
            },
            
            # Accesorios
            {
                'categoria': accesorios,
                'nombre': 'Collar Antipulgas',
                'descripcion': 'Collar repelente de pulgas y garrapatas duración 8 meses',
                'tipo_producto': 'accesorio',
                'precio': 12990,
                'codigo': 'ACC001',
                'stock': 40
            },
            {
                'categoria': accesorios,
                'nombre': 'Juguete Interactivo',
                'descripcion': 'Juguete dispensador de premios para estimulación mental',
                'tipo_producto': 'accesorio',
                'precio': 8990,
                'codigo': 'ACC002',
                'stock': 20
            },
            
            # Higiene
            {
                'categoria': higiene,
                'nombre': 'Shampoo Antipulgas',
                'descripcion': 'Shampoo medicado contra pulgas y dermatitis',
                'tipo_producto': 'accesorio',
                'precio': 7990,
                'codigo': 'HIG001',
                'stock': 35
            },
            
            # Servicios
            {
                'categoria': servicios,
                'nombre': 'Consulta Veterinaria',
                'descripcion': 'Consulta médica general con examen físico completo',
                'tipo_producto': 'servicio',
                'precio': 25000,
                'codigo': 'SER001',
                'stock': 0
            },
            {
                'categoria': servicios,
                'nombre': 'Vacuna Antirrábica',
                'descripcion': 'Vacunación antirrábica anual obligatoria',
                'tipo_producto': 'servicio',
                'precio': 18000,
                'codigo': 'SER002',
                'stock': 0
            }
        ]

        created_count = 0
        
        for producto_data in productos_ejemplo:
            producto, created = Producto.objects.get_or_create(
                codigo=producto_data['codigo'],
                defaults=producto_data
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Creado: {producto.nombre} - ${producto.precio:,.0f} CLP')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'- Ya existe: {producto.nombre}')
                )
        
        if created_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f'\n¡Éxito! Se crearon {created_count} productos de ejemplo.')
            )
        else:
            self.stdout.write(
                self.style.WARNING('\nTodos los productos ya existían.')
            )
