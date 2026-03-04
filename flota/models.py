from django.db import models
from django.utils import timezone


class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    # Para notificaciones push mencionadas en el PDF (HubSpot/App)
    acepta_notificaciones = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Vehiculo(models.Model):
    ESTADOS = [
        ('disponible', 'Disponible'),
        ('alquilado', 'Alquilado'),
        ('taller', 'En Mantenimiento'),
    ]

    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    matricula = models.CharField(max_length=15, unique=True)

    # --- INTEGRACIÓN OT (SENSORES) ---
    # RFID: Para el control de llaves y acceso (mencionado en Baz 1.3)
    rfid_tag = models.CharField(max_length=50, blank=True, null=True, help_text="ID del tag RFID de la llave")

    # OBD-II & GPS: Datos de telemática (mencionado en Baz 1.2)
    kilometraje = models.PositiveIntegerField(default=0)
    nivel_gasolina = models.FloatField(help_text="Porcentaje de 0 a 100")
    ubicacion_lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    ubicacion_lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    # TPMS: Sensor de presión de neumáticos (mencionado en Baz 1.2)
    alerta_presion_neumaticos = models.BooleanField(default=False,
                                                    help_text="True si el sensor TPMS detecta baja presión")

    # Estado general
    estado = models.CharField(max_length=20, choices=ESTADOS, default='disponible')

    def __str__(self):
        return f"{self.marca} {self.modelo} - {self.matricula}"


class Reserva(models.Model):
    TIPOS_SERVICIO = [
        ('vacaciones', 'Alquiler Vacacional'),
        ('traslado', 'Traslado Aeropuerto'),  # Mencionado en "Situación actual"
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='reservas')
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name='reservas')
    tipo_servicio = models.CharField(max_length=20, choices=TIPOS_SERVICIO)

    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()

    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo_servicio} - {self.cliente.nombre}"


class InspeccionIA(models.Model):
    """
    Este modelo simula el "Procés 2: Recollida i lliurança"
    donde usáis cámaras con IA para detectar daños.
    """
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    fecha_inspeccion = models.DateTimeField(default=timezone.now)

    # El sistema de IA marcaría esto automáticamente
    daños_detectados = models.BooleanField(default=False)
    reporte_ia = models.TextField(blank=True,
                                  help_text="Descripción del daño generado por la IA (ej: Rayón puerta derecha)")
    foto_evidencia = models.ImageField(upload_to='inspecciones/', blank=True, null=True)

    def __str__(self):
        return f"Inspección {self.reserva.id} - Daños: {self.daños_detectados}"