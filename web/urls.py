from django.contrib import admin
from . import views
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from core.views import DashboardView

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login/', views.loginform, name ='loginform'),
    path('logout/', views.logout, name='logout'),
    path('registro/', views.registrousuario, name='registrousuario'),
    path('client/', views.cliente, name='cliente'),
    path('employee/', views.empleado, name='empleado'),
    path('calendar/', views.agenda, name='agenda'),
    path('viewOrden/<int:pk>', views.recepcionOrden, name='recepcionOrden'),
    path('listCalendar/', views.listaCalendario, name='listaCalendario'),
    path('guardar_observacion/', views.guardar_observacion, name='guardar_observacion'),
    path('calender/', views.CalendarViewNew.as_view(), name='calender'),
    path("signin/", views.SignInView.as_view(), name="signin"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("calenders/", views.CalendarView.as_view(), name="calendars"),
    path("event/new/", views.create_event, name="event_new"),
    path("event/edit/<int:pk>/", views.EventEdit.as_view(), name="event_edit"),
    path("event/<int:event_id>/details/", views.event_details, name="event-detail"),
    path(
        "add_eventmember/<int:event_id>", views.add_eventmember, name="add_eventmember"
    ),
    path( 
        "event/<int:pk>/remove",
        views.EventMemberDeleteView.as_view(),
        name="remove_event",
    ),
    path("all-event-list/", views.AllEventsListView.as_view(), name="all_events"),
    path(
        "running-event-list/",
        views.RunningEventsListView.as_view(),
        name="running_events",
    ),
]