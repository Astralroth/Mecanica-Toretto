from django.db import models


# Create your models here.
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    json = models.JSONField(default={}, blank=True, null=True)
    state = models.CharField(max_length=100, default="Pendiente")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"


class Provider(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50, verbose_name="Nombre Proveedor")
    descripcion = models.CharField(max_length=100, verbose_name="Descripcion")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre}"


class Product(models.Model):
    estado_producto = [[0, "Nuevo"], [1, "Usado"], [2, "De fabrica"]]

    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, verbose_name="Nombre Producto")
    descripcion = models.CharField(max_length=100, verbose_name="Descripcion")
    provider = models.ForeignKey("Provider", on_delete=models.CASCADE)
    precio = models.IntegerField(verbose_name="Precio Producto")
    estado = models.IntegerField(
        choices=estado_producto, verbose_name="Estado Producto"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre}"

class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=22, decimal_places=0)
    tiempo_estimado = models.IntegerField()
    productos_asociados = models.TextField()

    def __str__(self):
        return self.nombre
    
class Boleta(models.Model):
    id = models.AutoField(primary_key=True)
    service = models.ForeignKey('Servicio', on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)     
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    run = models.CharField(max_length=8)
    subtotal = models.DecimalField(max_digits=8, decimal_places=0)     
    impuesto = models.DecimalField(max_digits=8, decimal_places=0)     
    total = models.DecimalField(max_digits=8, decimal_places=0)      

    def str(self):         
        return self.nombre