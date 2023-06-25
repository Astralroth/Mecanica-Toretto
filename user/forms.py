from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, EventMember


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form-control','type':'text','name': 'email'}),
        label="Email")
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control','type':'password', 'name':'password1'}),
        label="Contraseña")
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control','type':'password', 'name': 'password2'}),
        label="Contraseña (de nuevo)")
    name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control','type':'text','name': 'name'}),
        label="nombre")
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control','type':'text','name': 'last_name'}),
        label="apellido")
    telefono = forms.IntegerField(widget=forms.TextInput(
        attrs={'class': 'form-control','type':'text','name': 'telefono'}),
        label="telefono")
    region = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control','type':'text','name': 'region'}),
        label="region")
    comuna = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control','type':'text','name': 'comuna'}),
        label="comuna")
    direccion = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control','type':'text','name': 'direccion'}),
        label="direccion")

    '''added attributes so as to customise for styling, like bootstrap'''
    class Meta:
        model = User
        fields = ['email','password1','password2','name','last_name','telefono','region','comuna','direccion']
        field_order = ['email','password1','password2','name','last_name','telefono','region','comuna','direccion']

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Passwords don't match. Please try again!")
        return self.cleaned_data

    def save(self, commit=True):
        user = super(RegistrationForm,self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

#The save(commit=False) tells Django to save the new record, but dont commit it to the database yet

#CALENDAR
from django.forms import ModelForm, DateInput
from user.models import Event

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ["title", "description", "start_time", "end_time"]
        # datetime-local is a HTML5 input type
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter event title"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter event description",
                }
            ),
            "start_time": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
            "end_time": DateInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
        }
        exclude = ["user"]

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields["start_time"].input_formats = ("%Y-%m-%dT%H:%M",)
        self.fields["end_time"].input_formats = ("%Y-%m-%dT%H:%M",)


class SignInForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    password = forms.CharField(
    widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

class AddMemberForm(forms.ModelForm):
    class Meta:
        model = EventMember
        fields = ["user"]