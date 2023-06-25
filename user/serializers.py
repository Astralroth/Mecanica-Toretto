from rest_framework import serializers
from .models import User, UserManager


# Serializador de tokens de usuario
class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email','name','last_name')

# Serializador de modelo usuarios
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserManager
        fields = '__all__'

    def create(self,validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def update(self,instance,validated_data):
        updated_user = super().update(instance,validated_data)
        updated_user.set_password(validated_data['password'])
        updated_user.save()
        return updated_user

# Serializador de modelo usuarios
class UserCheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'email', 'name', 'last_name', 'telefono', 'region', 'comuna', 'direccion']