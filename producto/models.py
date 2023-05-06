from django.db import models


estado_producto = [
    [0, "Nuevo"],
    [1, "Usado"],
    [3, "De fabrica"]
]


# Create your models here.
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, verbose_name= "Nombre Producto")
    descripcion = models.CharField(max_length=100, verbose_name= "Descripcion")
    marca = models.CharField(max_length=50, verbose_name= "Marca Producto")
    precio = models.IntegerField(verbose_name= "Precio Producto")
    estado = models.IntegerField(choices= estado_producto, verbose_name="Estado Producto")
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name="Fecha Registro")
    data_update = models.DateTimeField(auto_now_add=True, verbose_name="Actualizacion Registro")

    def __str__(self):
        return f'{self.name}'
    






