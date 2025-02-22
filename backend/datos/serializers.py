from rest_framework import serializers
from .models import *

class RegistrosSerializer(serializers.ModelSerializer):
    usuario = serializers.SlugRelatedField(
        queryset=Usuarios.objects.all(),
        slug_field='nombre'
    )
    
    vehiculo = serializers.SlugRelatedField(
        queryset=Vehiculos.objects.all(),
        slug_field='placa'
    )

    rol = serializers.CharField(source="usuario.rol", read_only=True)

    class Meta:
        model = Registros
        fields = ('id','usuario','vehiculo','movimiento','fecha', 'rol')

    # usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    # vehiculo = models.ForeignKey(Vehiculos, on_delete=models.CASCADE)
    # movimiento = models.CharField(max_length=30)
    # fecha = models.DateTimeField(auto_now_add=True)
