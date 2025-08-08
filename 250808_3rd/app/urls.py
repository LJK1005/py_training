from django.urls import path
from . import views

urlpatterns = [
    path("csv/", views.show_csv, name="show_csv"),
]