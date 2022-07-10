
from django.urls import path, include

from . import views



app_name = 'reports'

urlpatterns = [
    path('', views.tournaments_list, name='tournaments'),
    path('<int:tournament_id>/register/', views.register, name='register'),
]