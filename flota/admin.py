from django.contrib import admin
from .models import Cliente, Vehiculo, Reserva, InspeccionIA

# Esto hace que en el panel se vea más profesional
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('marca', 'matricula', 'estado', 'nivel_gasolina', 'alerta_presion_neumaticos')
    list_filter = ('estado', 'alerta_presion_neumaticos')

class InspeccionAdmin(admin.ModelAdmin):
    list_display = ('reserva', 'fecha_inspeccion', 'daños_detectados')

admin.site.register(Cliente)
admin.site.register(Vehiculo, VehiculoAdmin)
admin.site.register(Reserva)
admin.site.register(InspeccionIA, InspeccionAdmin)