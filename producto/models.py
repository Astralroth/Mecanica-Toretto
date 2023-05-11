from django.db import models



estado_producto = [
    [0, "Nuevo"],
    [1, "Usado"],
    [2, "De fabrica"]
]


# Create your models here.
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, verbose_name= "Nombre Producto")
    descripcion = models.CharField(max_length=100, verbose_name= "Descripcion")
    provider = models.ForeignKey('Provider', on_delete=models.CASCADE)
    precio = models.IntegerField(verbose_name= "Precio Producto")
    estado = models.IntegerField(choices= estado_producto, verbose_name="Estado Producto")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.nombre}'

class Provider(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50, verbose_name= "Nombre Proveedor")
    descripcion = models.CharField(max_length=100, verbose_name= "Descripcion")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.nombre}'

class producto_boleta(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)     
    cantidad = models.PositiveIntegerField()     
    precio = models.DecimalField(max_digits=8, decimal_places=0)     
    fecha = models.DateField(auto_now_add=True)     
    cliente = models.CharField(max_length=100)     
    direccion = models.CharField(max_length=200)     
    subtotal = models.DecimalField(max_digits=8, decimal_places=0)     
    impuesto = models.DecimalField(max_digits=8, decimal_places=0)     
    total = models.DecimalField(max_digits=8, decimal_places=0)      

    def str(self):         
        return self.nombre




