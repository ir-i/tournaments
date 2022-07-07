
from django.urls import path, include

from . import views



urlpatterns = [
    path('', views.tournaments_list, name='tournaments'),
]