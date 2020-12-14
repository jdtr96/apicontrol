from django.db import models

# Create your models here.


class Producto(models.Model):

    nombre = models.CharField(max_length=100)
    cantidad = models.IntegerField(default=0)
    p_conpra = models.FloatField(default=0.0)
    p_venta = models.FloatField(default=0.0)
    cantidad_vendidos = models.IntegerField(default=0)
    user = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='usuario', default=0)

    def __str__(self):
        return self.nombre
