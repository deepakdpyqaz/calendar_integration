from django.urls import path, include
from . import views

urlpatterns = [
    path("init", views.GoogleCalendarInitView, name="init"),
    path("redirect", views.GoogleCalendarRedirectView, name="redirect"),
]
