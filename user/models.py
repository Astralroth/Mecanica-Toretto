from django.db import models
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from datetime import datetime
from django.urls import reverse
# from django.contrib.auth.models import AbstractUser, BaseUserManager

# Opciones Perfil usuario
PERFIL_USUARIO = (
    (0,'Cliente no registrado'),
    (1,'Cliente'),
    (2,'Administrador'),
    (3,'Empleado'),
)

class UserManager(BaseUserManager):
    def _create_user(self, email, name,last_name, password, perfil, is_staff, is_superuser, **extra_fields):
        user = self.model(
            email = email,
            name = name,
            last_name = last_name,
            perfil = perfil,
            is_staff = is_staff,
            is_superuser = is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, email, name,last_name, is_staff, password=None, **extra_fields):
        return self._create_user( email, name,last_name,password, is_staff, False, **extra_fields)

    def create_superuser(self, email, name,last_name, password=None, **extra_fields):
        return self._create_user( email, name,last_name, password, 2,True, True, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Correo Electrónico',max_length = 255, unique = True,)
    name = models.CharField('Nombres', max_length = 255, blank = True, null = True)
    last_name = models.CharField('Apellidos', max_length = 255, blank = True, null = True)
    telefono = models.IntegerField('Teléfono', blank = True, null = True)
    region = models.CharField('Region', max_length = 255, blank = True, null = True)
    comuna = models.CharField('Comuna', max_length = 255, blank = True, null = True)
    direccion = models.CharField('Direccion', max_length = 400, blank = True, null = True)
    perfil = models.IntegerField(default=1, choices=PERFIL_USUARIO, verbose_name="Perfil de Usuario")
    created_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default = True)
    is_staff = models.BooleanField(default = False)
    objects = UserManager()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','last_name', 'telefono']

    def __str__(self):
        return f'{self.email} - {PERFIL_USUARIO[self.perfil][1]}'
    

class products(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_producto = models.CharField(max_length=100, null=False)
    cantidad = models.IntegerField(null=False)
    precio = models.IntegerField(null=False)

    def __str__(self):
        return self.nombre_producto
class observaciones(models.Model):
    observacion = models.TextField(null=False)
    fecha = models.DateTimeField(auto_now_add=True, null=False)

#CALENDAR
class EventManager(models.Manager):
    """ Event manager """

    def get_all_events(self, user):
        events = Event.objects.filter(user=user, is_active=True, is_deleted=False)
        return events

    def get_running_events(self, user):
        running_events = Event.objects.filter(
            user=user,
            is_active=True,
            is_deleted=False,
            end_time__gte=datetime.now().date(),
        ).order_by("start_time")
        return running_events


#CALENDAR

class EventAbstract(models.Model):
    """ Event abstract model """

    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Event(EventAbstract):
    """ Event model """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    objects = EventManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("event-detail", args=(self.id,))

    @property
    def get_html_url(self):
        url = reverse("event-detail", args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'

class EventAbstract(models.Model):
    """ Event abstract model """

    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class EventMember(EventAbstract):
    """ Event member model """

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="events")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="event_members"
    )

    class Meta:
        unique_together = ["event", "user"]

    def __str__(self):
        return str(self.user)