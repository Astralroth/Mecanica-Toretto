from django.urls import path

from web import views

app_name = "user"


urlpatterns = [
    # path("signup/", views.SignUpView.as_view(), name="signup"),
    path("loginform/", views.SignInView.as_view(), name="loginform"),
    # path("signout/", views.signout, name="signout"),
]
