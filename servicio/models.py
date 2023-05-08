from django.db import models

class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=22, decimal_places=0)
    tiempo_estimado = models.IntegerField()
    productos_asociados = models.TextField()

    def __str__(self):
        return self.nombre
