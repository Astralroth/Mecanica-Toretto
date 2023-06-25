import json
import traceback

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages, auth
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from user.models import User, products, observaciones, Event,EventMember
from user.serializers import UserSerializer
from user.forms import RegistrationForm,EventForm,SignInForm,AddMemberForm
from user.mixins import SuperUserMixin
from django.views.generic import View
from django.utils.safestring import mark_safe
from datetime import timedelta, datetime, date
import calendar
from .utils import Calendar
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView

# Renderizado de Home del portal
def inicio(SuperUserMixin):
    return render(SuperUserMixin, 'index.html', {})

# Login (POST -para gestion login- y GET para renderizado del template)
def loginform(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            print(email)
        except:
            print('ERROR!')
        password = request.POST.get('password')
        print(password)
        user = authenticate(request, email = email, password = password)
        if user is not None:
            print('ok')
            form = login(request, user)
            messages.success(request, f' ¡Bienvenido! \n Ya puedes comenzar a utilizar la página')
            return redirect('web:inicio')
        else:
            print('no se reconoce user')
            messages.info(request, f'No existe el usuario o la contraseña es incorrecta')
            return redirect('web:loginform')
    elif request.method == 'GET':
        return render(request, 'login.html', {})

# Logout
@login_required
def logout(request):
    auth.logout(request)
    return redirect('web:inicio')

# Renderizado de Formulario de Registro de Usuario del portal
def registrousuario(request):
    # list
    if request.method == 'GET':
        return render(request, 'registro.html', {})
    
    # create
    elif request.method == 'POST':
        print(request.POST)
        data = request.POST
        form = RegistrationForm(data = data)
        print(form)
        # validation
        if form.is_valid():
            form.save()
            print('El usuario se ha creado!')
            messages.success(request, f' ¡El usuario se ha creado! Haz click en Login para ingresar con tu cuenta.')
            return redirect('web:loginform')
        else:
            print('El usuario NO se ha creado!')
            messages.success(request, f' ¡El usuario NO se ha creado! Revisa los campos requeridos o contraseña no coincide')
            return redirect('web:registrousuario')

# Renderizado de las vistas
def cliente(request):
    return render(request, 'client.html', {})

def empleado(request):
    return render(request, 'employee.html', {})

def agenda(request):
    return render(request, 'web/calendar.html', {})

def recepcionOrden(request):
    Productos = products.objects.all()
    return render(request, 'viewOrden.html', {'productos': Productos})
    
def listaCalendario(request):
    return render(request, 'web/listCalendar.html', {})

def running_events(request):
    return render(request, 'web:running_events', {})

def guardar_observacion(request):
    if request.method == 'POST':
        texto = request.POST.get('observacion')
        nueva_observacion = observaciones(observacion=texto)
        nueva_observacion.save()
        print("Observación guardada:", nueva_observacion)
        print("aa")
        return redirect('web:recepcionOrden')
    
#CALENDAR

from django.views import generic

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split("-"))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = "month=" + str(prev_month.year) + "-" + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = "month=" + str(next_month.year) + "-" + str(next_month.month)
    return month

class CalendarViewNew(LoginRequiredMixin, generic.View):
    login_url = "web:loginform"
    template_name = "web/calendar.html"
    form_class = EventForm

    def get(self, request, *args, **kwargs):
        forms = self.form_class()
        events = Event.objects.get_all_events(user=request.user)
        events_month = Event.objects.get_running_events(user=request.user)
        event_list = []
        # start: '2020-09-16T16:00:00'
        for event in events:
            event_list.append(
                {
                    "title": event.title,
                    "start": event.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "end": event.end_time.strftime("%Y-%m-%dT%H:%M:%S"),

                }
            )
        context = {"form": forms, "events": event_list,
                   "events_month": events_month}
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            form = forms.save(commit=False)
            form.user = request.user
            form.save()
            return redirect("web:calender")
        context = {"form": forms}
        return render(request, self.template_name, context)
    
class SignInView(View):
    """ User registration view """

    template_name = "login.html"
    form_class = SignInForm

    def get(self, request, *args, **kwargs):
        forms = self.form_class()
        context = {"form": forms}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            email = forms.cleaned_data["email"]
            password = forms.cleaned_data["password"]
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect("inicio")
        context = {"form": forms}
        return render(request, self.template_name, context)


class CalendarView(LoginRequiredMixin, generic.ListView):
    login_url = "web:loginform"
    model = Event
    template_name = "calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get("month", None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context["calendar"] = mark_safe(html_cal)
        context["prev_month"] = prev_month(d)
        context["next_month"] = next_month(d)
        return context

@login_required(login_url="loginform")
def create_event(request):
    form = EventForm(request.POST or None)
    if request.POST and form.is_valid():
        title = form.cleaned_data["title"]
        description = form.cleaned_data["description"]
        start_time = form.cleaned_data["start_time"]
        end_time = form.cleaned_data["end_time"]
        Event.objects.get_or_create(
            user=request.user,
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time,
        )
        return HttpResponseRedirect(reverse("web:calender"))
    return render(request, "event.html", {"form": form})

def add_eventmember(request, event_id):
    forms = AddMemberForm()
    if request.method == "POST":
        forms = AddMemberForm(request.POST)
        if forms.is_valid():
            member = EventMember.objects.filter(event=event_id)
            event = Event.objects.get(id=event_id)
            if member.count() <= 9:
                user = forms.cleaned_data["user"]
                EventMember.objects.create(event=event, user=user)
                return redirect("web:calender")
            else:
                print("--------------User limit exceed!-----------------")
    context = {"form": forms}
    return render(request, "add_member.html", context)

class AllEventsListView(ListView):
    """ All event list views """

    template_name = "web/events_list.html"
    model = Event

    def get_queryset(self):
        return Event.objects.get_all_events(user=self.request.user)

class RunningEventsListView(ListView):
    """ Running events list view """

    template_name = "web/events_list.html"
    model = Event

    def get_queryset(self):
        return Event.objects.get_running_events(user=self.request.user)

class EventEdit(generic.UpdateView):
    model = Event
    fields = ["title", "description", "start_time", "end_time"]
    template_name = "event.html"
    

@login_required(login_url="loginform")
def event_details(request, event_id):
    event = Event.objects.get(id=event_id)
    eventmember = EventMember.objects.filter(event=event)
    context = {"event": event, "eventmember": eventmember}
    return render(request, "event-details.html", context)


def add_eventmember(request, event_id):
    forms = AddMemberForm()
    if request.method == "POST":
        forms = AddMemberForm(request.POST)
        if forms.is_valid():
            member = EventMember.objects.filter(event=event_id)
            event = Event.objects.get(id=event_id)
            if member.count() <= 9:
                user = forms.cleaned_data["user"]
                EventMember.objects.create(event=event, user=user)
                return redirect("web:calender")
            else:
                print("--------------User limit exceed!-----------------")
    context = {"form": forms}
    return render(request, "add_member.html", context)

class EventMemberDeleteView(generic.DeleteView):
    model = EventMember
    template_name = "event_delete.html"
    success_url = reverse_lazy("web:calender")